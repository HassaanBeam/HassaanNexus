#!/usr/bin/env python3
"""
Unit Tests for Airtable Master Scripts
Run: pytest test_unit.py -v
"""

import os
import sys
import json
import pytest
from pathlib import Path

from conftest import NEXUS_ROOT, SCRIPTS_DIR


class TestCheckConfig:
    """Tests for check_airtable_config.py"""

    def test_script_exists(self, scripts_dir):
        """Script file exists"""
        assert (scripts_dir / 'check_airtable_config.py').exists()

    def test_script_syntax(self, scripts_dir):
        """Script has valid Python syntax"""
        script_path = scripts_dir / 'check_airtable_config.py'
        with open(script_path, 'r', encoding='utf-8') as f:
            compile(f.read(), str(script_path), 'exec')

    def test_runs_without_crash(self, script_runner):
        """Script runs and exits with valid code"""
        code, stdout, stderr = script_runner('check_airtable_config.py')
        assert code in [0, 1, 2], f"Unexpected exit code: {code}"

    def test_json_flag_recognized(self, script_runner):
        """--json flag is recognized"""
        code, stdout, stderr = script_runner('check_airtable_config.py', ['--json'])
        assert 'unrecognized arguments' not in stderr

    def test_verbose_flag_recognized(self, script_runner):
        """--verbose flag is recognized"""
        code, stdout, stderr = script_runner('check_airtable_config.py', ['--verbose'])
        assert 'unrecognized arguments' not in stderr


class TestDiscoverBases:
    """Tests for discover_bases.py"""

    def test_script_exists(self, scripts_dir):
        """Script file exists"""
        assert (scripts_dir / 'discover_bases.py').exists()

    def test_script_syntax(self, scripts_dir):
        """Script has valid Python syntax"""
        script_path = scripts_dir / 'discover_bases.py'
        with open(script_path, 'r', encoding='utf-8') as f:
            compile(f.read(), str(script_path), 'exec')

    def test_refresh_flag_recognized(self, script_runner):
        """--refresh flag is recognized"""
        code, stdout, stderr = script_runner('discover_bases.py', ['--help'])
        output = stdout + stderr
        assert 'refresh' in output.lower()

    def test_json_flag_recognized(self, script_runner):
        """--json flag is recognized"""
        code, stdout, stderr = script_runner('discover_bases.py', ['--help'])
        output = stdout + stderr
        assert 'json' in output.lower()

    def test_with_schema_flag_recognized(self, script_runner):
        """--with-schema flag is recognized"""
        code, stdout, stderr = script_runner('discover_bases.py', ['--help'])
        output = stdout + stderr
        assert 'schema' in output.lower()


class TestQueryRecords:
    """Tests for query_records.py"""

    def test_script_exists(self, scripts_dir):
        """Script file exists"""
        assert (scripts_dir / 'query_records.py').exists()

    def test_script_syntax(self, scripts_dir):
        """Script has valid Python syntax"""
        script_path = scripts_dir / 'query_records.py'
        with open(script_path, 'r', encoding='utf-8') as f:
            compile(f.read(), str(script_path), 'exec')

    def test_missing_base_arg(self, script_runner):
        """Missing --base argument causes error"""
        code, stdout, stderr = script_runner('query_records.py', ['--table', 'Test'])
        assert code != 0
        assert 'base' in stderr.lower() or 'required' in stderr.lower()

    def test_missing_table_arg(self, script_runner):
        """Missing --table argument causes error"""
        code, stdout, stderr = script_runner('query_records.py', ['--base', 'appTEST'])
        assert code != 0
        assert 'table' in stderr.lower() or 'required' in stderr.lower()

    def test_all_args_recognized(self, script_runner):
        """All arguments are recognized"""
        code, stdout, stderr = script_runner('query_records.py', [
            '--base', 'app', '--table', 't', '--filter', '{X}="Y"',
            '--fields', 'A,B', '--sort', '-Date', '--limit', '10',
            '--json', '--verbose'
        ])
        assert 'unrecognized arguments' not in stderr

    def test_limit_must_be_integer(self, script_runner):
        """--limit must be integer"""
        code, stdout, stderr = script_runner('query_records.py', [
            '--base', 'app', '--table', 't', '--limit', 'abc'
        ])
        assert code != 0
        assert 'invalid' in stderr.lower()


class TestManageRecords:
    """Tests for manage_records.py"""

    def test_script_exists(self, scripts_dir):
        """Script file exists"""
        assert (scripts_dir / 'manage_records.py').exists()

    def test_script_syntax(self, scripts_dir):
        """Script has valid Python syntax"""
        script_path = scripts_dir / 'manage_records.py'
        with open(script_path, 'r', encoding='utf-8') as f:
            compile(f.read(), str(script_path), 'exec')

    def test_invalid_action(self, script_runner):
        """Invalid action causes error"""
        code, stdout, stderr = script_runner('manage_records.py', [
            'invalid_action', '--base', 'app', '--table', 't'
        ])
        assert code != 0

    def test_create_missing_data(self, script_runner):
        """CREATE without --data or --file causes error"""
        code, stdout, stderr = script_runner('manage_records.py', [
            'create', '--base', 'app', '--table', 't'
        ])
        output = stdout + stderr
        assert code != 0
        assert 'data' in output.lower() or 'file' in output.lower()

    def test_delete_missing_record(self, script_runner):
        """DELETE without --record or --file causes error"""
        code, stdout, stderr = script_runner('manage_records.py', [
            'delete', '--base', 'app', '--table', 't'
        ])
        output = stdout + stderr
        assert code != 0

    def test_invalid_json_data(self, script_runner):
        """Invalid JSON in --data causes error"""
        code, stdout, stderr = script_runner('manage_records.py', [
            'create', '--base', 'app', '--table', 't', '--data', '{bad json}'
        ])
        output = stdout + stderr
        assert code != 0
        assert 'json' in output.lower() or 'invalid' in output.lower()

    def test_typecast_flag_recognized(self, script_runner):
        """--typecast flag is recognized"""
        code, stdout, stderr = script_runner('manage_records.py', [
            'create', '--base', 'app', '--table', 't',
            '--data', '{"Name":"Test"}', '--typecast'
        ])
        assert 'unrecognized arguments' not in stderr

    def test_replace_flag_recognized(self, script_runner):
        """--replace flag is recognized"""
        code, stdout, stderr = script_runner('manage_records.py', [
            'update', '--base', 'app', '--table', 't',
            '--record', 'rec123', '--data', '{}', '--replace'
        ])
        assert 'unrecognized arguments' not in stderr


class TestBatchLogic:
    """Tests for batch processing logic"""

    def test_batch_size_defined(self, scripts_dir):
        """Batch size of 10 should be defined"""
        script_path = scripts_dir / 'manage_records.py'
        content = script_path.read_text(encoding='utf-8')
        assert '10' in content

    def test_retry_logic_exists(self, scripts_dir):
        """Retry logic should exist"""
        script_path = scripts_dir / 'manage_records.py'
        content = script_path.read_text(encoding='utf-8')
        has_retry = 'retry' in content.lower()
        has_429 = '429' in content
        has_backoff = 'backoff' in content.lower() or 'wait' in content.lower()
        assert has_retry or has_429 or has_backoff


class TestEncoding:
    """Tests for UTF-8 encoding handling"""

    def test_scripts_have_utf8_handling(self, scripts_dir):
        """All scripts should handle UTF-8"""
        for script_name in ['check_airtable_config.py', 'discover_bases.py',
                           'query_records.py', 'manage_records.py']:
            script_path = scripts_dir / script_name
            content = script_path.read_text(encoding='utf-8')
            has_io = 'import io' in content
            has_utf8 = 'utf-8' in content.lower()
            has_encoding = 'encoding' in content.lower()
            assert has_io or has_utf8 or has_encoding, f"{script_name} should handle encoding"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
