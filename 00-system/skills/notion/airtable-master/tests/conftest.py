#!/usr/bin/env python3
"""
Pytest Configuration and Fixtures for Airtable Master Tests
"""

import os
import sys
import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

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

sys.path.insert(0, str(SCRIPTS_DIR))

# Mock response data
MOCK_BASES = {
    'bases': [
        {'id': 'appTEST001', 'name': 'Test Base 1', 'permissionLevel': 'create'},
        {'id': 'appTEST002', 'name': 'Test Base 2', 'permissionLevel': 'edit'},
    ]
}

MOCK_WHOAMI = {
    'id': 'usrTEST123',
    'email': 'test@example.com',
    'scopes': ['data.records:read', 'data.records:write', 'schema.bases:read']
}

MOCK_RECORDS = {
    'records': [
        {'id': 'recTEST001', 'createdTime': '2025-01-01T00:00:00.000Z',
         'fields': {'Name': 'John Doe', 'Email': 'john@example.com'}},
        {'id': 'recTEST002', 'createdTime': '2025-01-02T00:00:00.000Z',
         'fields': {'Name': 'Jane Smith', 'Email': 'jane@example.com'}},
    ]
}

@pytest.fixture
def nexus_root():
    return NEXUS_ROOT

@pytest.fixture
def scripts_dir():
    return SCRIPTS_DIR

@pytest.fixture
def mock_env():
    with patch.dict(os.environ, {'AIRTABLE_API_KEY': 'patTEST123.fake'}):
        yield

def run_script(script_name, args=None, env=None, cwd=None, timeout=30):
    """Run a script and capture output."""
    import subprocess

    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    test_env = os.environ.copy()
    test_env['PYTHONIOENCODING'] = 'utf-8'
    if env:
        test_env.update(env)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd or str(NEXUS_ROOT),
        env=test_env,
        encoding='utf-8',
        errors='replace'
    )

    return result.returncode, result.stdout, result.stderr

@pytest.fixture
def script_runner():
    return run_script
