#!/usr/bin/env python3
"""
Airtable Master - Full Test Orchestrator

Usage:
    python run_full_tests.py              # Quick tests (default)
    python run_full_tests.py --unit       # Unit tests only
    python run_full_tests.py --integration # Integration tests
    python run_full_tests.py --live       # Live API tests
    python run_full_tests.py --full       # All tests
    python run_full_tests.py --verbose    # Verbose output
"""

import os
import sys
import json
import time
import argparse
import subprocess
import io
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def find_nexus_root():
    current = Path(__file__).parent
    while current != current.parent:
        if (current / 'CLAUDE.md').exists():
            return current
        current = current.parent
    return None


NEXUS_ROOT = find_nexus_root()
TESTS_DIR = Path(__file__).parent
SCRIPTS_DIR = NEXUS_ROOT / '00-system' / 'skills' / 'notion' / 'airtable-master' / 'scripts'


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    @classmethod
    def disable(cls):
        cls.GREEN = cls.RED = cls.YELLOW = cls.CYAN = cls.BOLD = cls.RESET = ''


class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ''):
        self.name = name
        self.passed = passed
        self.message = message


class TestSuite:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[TestResult] = []
        self.start_time = time.time()

    def _log(self, status: str, message: str):
        if status == 'PASS':
            icon = f"{Colors.GREEN}[PASS]{Colors.RESET}"
        elif status == 'FAIL':
            icon = f"{Colors.RED}[FAIL]{Colors.RESET}"
        elif status == 'SKIP':
            icon = f"{Colors.YELLOW}[SKIP]{Colors.RESET}"
        else:
            icon = f"{Colors.CYAN}[INFO]{Colors.RESET}"
        print(f"  {icon} {message}")

    def _run_script(self, script_name: str, args: List[str] = None, timeout: int = 60) -> Tuple[int, str, str]:
        script_path = SCRIPTS_DIR / script_name
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)

        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                cwd=str(NEXUS_ROOT), env=env, encoding='utf-8', errors='replace'
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, '', 'Timeout expired'
        except Exception as e:
            return -1, '', str(e)

    def _test(self, name: str, condition: bool, message: str = '') -> bool:
        result = TestResult(name, condition, message)
        self.results.append(result)
        if condition:
            self._log('PASS', name + (f' - {message}' if message else ''))
        else:
            self._log('FAIL', name + (f' - {message}' if message else ''))
        return condition

    def run_syntax_validation(self):
        print(f"\n{Colors.CYAN}=== Syntax Validation ==={Colors.RESET}\n")

        scripts = ['check_airtable_config.py', 'discover_bases.py',
                   'query_records.py', 'manage_records.py']

        for script_name in scripts:
            script_path = SCRIPTS_DIR / script_name
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), str(script_path), 'exec')
                self._test(f'{script_name} syntax', True)
            except SyntaxError as e:
                self._test(f'{script_name} syntax', False, str(e))
            except FileNotFoundError:
                self._test(f'{script_name} exists', False, 'File not found')

    def run_unit_tests(self):
        print(f"\n{Colors.CYAN}=== Unit Tests ==={Colors.RESET}\n")

        try:
            import pytest
        except ImportError:
            self._log('SKIP', 'pytest not installed')
            return

        test_file = TESTS_DIR / 'test_unit.py'
        if not test_file.exists():
            self._log('SKIP', 'test_unit.py not found')
            return

        cmd = [sys.executable, '-m', 'pytest', str(test_file), '-v', '--tb=short']
        if not self.verbose:
            cmd.append('-q')

        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120,
                cwd=str(NEXUS_ROOT), env=env, encoding='utf-8', errors='replace'
            )

            if self.verbose:
                print(result.stdout)

            if result.returncode == 0:
                self._test('Unit tests', True, 'All passed')
            else:
                failures = result.stdout.count(' FAILED')
                passed = result.stdout.count(' PASSED')
                self._test('Unit tests', False, f'{passed} passed, {failures} failed')
                if self.verbose:
                    print(result.stderr)

        except subprocess.TimeoutExpired:
            self._test('Unit tests', False, 'Timeout')
        except Exception as e:
            self._test('Unit tests', False, str(e))

    def run_integration_tests(self):
        print(f"\n{Colors.CYAN}=== Integration Tests ==={Colors.RESET}\n")

        # Config check
        code, stdout, stderr = self._run_script('check_airtable_config.py')
        self._test('Config check runs', code in [0, 1, 2], f'Exit code: {code}')

        # Discovery
        code, stdout, stderr = self._run_script('discover_bases.py', ['--json'])
        if code == 0:
            try:
                data = json.loads(stdout)
                self._test('Discovery JSON output', 'bases' in data,
                          f"Found {len(data.get('bases', []))} bases")
            except json.JSONDecodeError:
                self._test('Discovery JSON output', False, 'Invalid JSON')
        else:
            self._test('Discovery runs', code == 0, stderr[:100])

        # Help commands
        code, _, _ = self._run_script('query_records.py', ['--help'])
        self._test('Query help', code == 0, 'Help displayed')

        code, _, _ = self._run_script('manage_records.py', ['--help'])
        self._test('Manage help', code == 0, 'Help displayed')

    def run_live_tests(self):
        print(f"\n{Colors.CYAN}=== Live API Tests ==={Colors.RESET}\n")

        # Load API key from .env if needed
        if not os.environ.get('AIRTABLE_API_KEY'):
            env_path = NEXUS_ROOT / '.env'
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('AIRTABLE_API_KEY='):
                            key = line.split('=', 1)[1].strip().strip('"\'')
                            os.environ['AIRTABLE_API_KEY'] = key
                            break

        if not os.environ.get('AIRTABLE_API_KEY'):
            self._log('SKIP', 'No AIRTABLE_API_KEY - skipping live tests')
            return

        test_file = TESTS_DIR / 'test_live_api.py'
        if not test_file.exists():
            self._log('SKIP', 'test_live_api.py not found')
            return

        try:
            import pytest
            cmd = [sys.executable, '-m', 'pytest', str(test_file), '-v', '--tb=short']
            if not self.verbose:
                cmd.append('-q')

            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300,
                cwd=str(NEXUS_ROOT), env=env, encoding='utf-8', errors='replace'
            )

            if self.verbose:
                print(result.stdout)

            if result.returncode == 0:
                self._test('Live API tests', True, 'All passed')
            else:
                failures = result.stdout.count(' FAILED')
                passed = result.stdout.count(' PASSED')
                skipped = result.stdout.count(' SKIPPED')
                self._test('Live API tests', False,
                          f'{passed} passed, {failures} failed, {skipped} skipped')

        except ImportError:
            self._log('SKIP', 'pytest not installed')
        except subprocess.TimeoutExpired:
            self._test('Live API tests', False, 'Timeout')
        except Exception as e:
            self._test('Live API tests', False, str(e))

    def print_summary(self):
        duration = time.time() - self.start_time
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"\n{Colors.BOLD}{'=' * 50}{Colors.RESET}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.RESET}")
        print(f"{'=' * 50}")
        print(f"Duration: {duration:.2f}s")
        print(f"Total:    {total}")
        print(f"{Colors.GREEN}Passed:   {passed}{Colors.RESET}")
        if failed > 0:
            print(f"{Colors.RED}Failed:   {failed}{Colors.RESET}")
        print(f"{'=' * 50}")

        if failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.RESET}")
            return 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed.{Colors.RESET}")
            return 1


def main():
    parser = argparse.ArgumentParser(description='Airtable Master Full Test Suite')
    parser.add_argument('--quick', action='store_true', help='Quick syntax validation')
    parser.add_argument('--unit', action='store_true', help='Run unit tests')
    parser.add_argument('--integration', action='store_true', help='Run integration tests')
    parser.add_argument('--live', action='store_true', help='Run live API tests')
    parser.add_argument('--full', action='store_true', help='Run all tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--no-color', action='store_true', help='Disable colors')
    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    print(f"\n{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.BOLD}AIRTABLE MASTER - FULL TEST SUITE{Colors.RESET}")
    print(f"{'=' * 50}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    suite = TestSuite(verbose=args.verbose)

    run_quick = args.quick or (not any([args.unit, args.integration, args.live, args.full]))
    run_unit = args.unit or args.full
    run_integration = args.integration or args.full
    run_live = args.live or args.full

    if run_quick or run_unit or run_integration or run_live:
        suite.run_syntax_validation()

    if run_unit:
        suite.run_unit_tests()

    if run_integration:
        suite.run_integration_tests()

    if run_live:
        suite.run_live_tests()

    exit_code = suite.print_summary()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
