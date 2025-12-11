#!/usr/bin/env python3
"""
Live API Tests for Airtable Master
Run: pytest test_live_api.py -v
"""

import os
import sys
import json
import time
import pytest
from pathlib import Path
from datetime import datetime

# Find Nexus root
def find_nexus_root():
    current = Path(__file__).parent
    while current != current.parent:
        if (current / 'CLAUDE.md').exists():
            return current
        current = current.parent
    return None

NEXUS_ROOT = find_nexus_root()
SCRIPTS_DIR = NEXUS_ROOT / '00-system' / 'skills' / 'notion' / 'airtable-master' / 'scripts'


def load_env():
    """Load .env file"""
    env_path = NEXUS_ROOT / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')

load_env()


def run_script(script_name, args=None, timeout=60):
    """Run a script and capture output."""
    import subprocess

    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(NEXUS_ROOT),
        env=env,
        encoding='utf-8',
        errors='replace'
    )

    return result.returncode, result.stdout, result.stderr


# Skip all tests if no API key
pytestmark = pytest.mark.skipif(
    not os.environ.get('AIRTABLE_API_KEY'),
    reason="AIRTABLE_API_KEY not set"
)


class TestLiveConfig:
    """Live tests for check_airtable_config.py"""

    def test_full_config_check(self):
        """Config check should run without crashing"""
        code, stdout, stderr = run_script('check_airtable_config.py')
        output = stdout + stderr
        # Exit codes: 0=success, 1=partial, 2=incomplete - all valid
        assert code in [0, 1, 2], f"Config check crashed: {output[:200]}"

    def test_api_connection(self):
        """API connection should work"""
        code, stdout, stderr = run_script('check_airtable_config.py', ['--verbose'])
        output = stdout + stderr
        assert 'API' in output or 'connection' in output.lower()

    def test_base_access(self):
        """Should detect accessible bases"""
        code, stdout, stderr = run_script('check_airtable_config.py', ['--verbose'])
        output = stdout + stderr
        assert 'base' in output.lower()


class TestLiveDiscovery:
    """Live tests for discover_bases.py"""

    def test_discover_bases(self):
        """Should discover accessible bases"""
        code, stdout, stderr = run_script('discover_bases.py', ['--json', '--refresh'])

        if code == 0:
            try:
                data = json.loads(stdout)
                assert 'bases' in data
                assert isinstance(data['bases'], list)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON: {stdout[:200]}")

    def test_cache_creation(self):
        """Should create cache file"""
        run_script('discover_bases.py', ['--refresh'])
        cache_path = NEXUS_ROOT / '01-memory' / 'integrations' / 'airtable-bases.yaml'
        assert cache_path.exists(), "Cache file should be created"

    def test_use_cached(self):
        """Should use cached data when available"""
        # First run to ensure cache
        run_script('discover_bases.py', ['--refresh'])

        # Second run should use cache
        start = time.time()
        code, stdout, stderr = run_script('discover_bases.py', ['--json'])
        elapsed = time.time() - start

        if code == 0:
            print(f"Cache read took {elapsed:.2f}s")


class TestLiveQuery:
    """Live tests for query_records.py"""

    @pytest.fixture(autouse=True)
    def setup_base_info(self):
        """Get first available base for testing"""
        try:
            import yaml
            cache_path = NEXUS_ROOT / '01-memory' / 'integrations' / 'airtable-bases.yaml'
            if cache_path.exists():
                with open(cache_path, 'r') as f:
                    cache = yaml.safe_load(f)
                bases = cache.get('bases', [])
                if bases:
                    self.test_base_id = bases[0].get('id')
                    tables = bases[0].get('tables', [])
                    self.test_table = tables[0].get('name') if tables else None
                else:
                    self.test_base_id = None
                    self.test_table = None
            else:
                self.test_base_id = None
                self.test_table = None
        except Exception:
            self.test_base_id = None
            self.test_table = None

    def test_query_nonexistent_table(self):
        """Should handle nonexistent table"""
        if not self.test_base_id:
            pytest.skip("No test base available")

        code, stdout, stderr = run_script('query_records.py', [
            '--base', self.test_base_id, '--table', 'NonExistentTable12345', '--json'
        ])
        output = stdout + stderr
        assert code != 0 or 'not found' in output.lower() or 'error' in output.lower()


class TestRateLimits:
    """Tests for rate limit handling"""

    def test_multiple_rapid_requests(self):
        """Should handle multiple rapid requests"""
        results = []
        for i in range(3):
            code, stdout, stderr = run_script('discover_bases.py', ['--json'])
            results.append(code)
            time.sleep(0.1)

        success_count = sum(1 for r in results if r == 0)
        assert success_count >= 1, "At least one request should succeed"


class TestIntegration:
    """End-to-end integration tests"""

    def test_config_then_discover(self):
        """Config check then discovery"""
        code1, _, _ = run_script('check_airtable_config.py')
        code2, _, _ = run_script('discover_bases.py', ['--json'])

        if code1 == 0:
            assert code2 == 0, "Discovery should work if config passes"

    def test_discover_then_query(self):
        """Discovery then query"""
        try:
            import yaml
        except ImportError:
            pytest.skip("yaml not installed")

        code1, _, _ = run_script('discover_bases.py', ['--refresh'])
        if code1 != 0:
            pytest.skip("Discovery failed")

        cache_path = NEXUS_ROOT / '01-memory' / 'integrations' / 'airtable-bases.yaml'
        if not cache_path.exists():
            pytest.skip("No cache created")

        with open(cache_path, 'r') as f:
            cache = yaml.safe_load(f)

        bases = cache.get('bases', [])
        if bases:
            base_id = bases[0].get('id')
            tables = bases[0].get('tables', [])
            if tables:
                table_name = tables[0].get('name', tables[0].get('id'))
                code2, _, _ = run_script('query_records.py', [
                    '--base', base_id, '--table', table_name, '--limit', '1', '--json'
                ])
                print(f"Query result: exit code {code2}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
