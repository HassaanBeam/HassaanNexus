# Airtable Master - Comprehensive Test Suite

## Quick Start

```bash
# Quick syntax validation
python run_full_tests.py --quick

# Full test suite (all tests)
python run_full_tests.py --full

# Individual modes
python run_full_tests.py --unit         # Unit tests only
python run_full_tests.py --integration  # Integration tests
python run_full_tests.py --live         # Live API tests
```

## Test Architecture

```
tests/
├── run_tests.py        # Quick validation (11 tests)
├── run_full_tests.py   # Full orchestrator
├── conftest.py         # Pytest fixtures
├── test_unit.py        # Unit tests (25 tests)
└── test_live_api.py    # Live API tests (10 tests)
```

## Prerequisites

1. **Python 3.8+**
2. **Dependencies**:
   ```bash
   pip install requests pyyaml pytest
   ```
3. **API Key** (for live tests):
   ```
   # .env
   AIRTABLE_API_KEY=pat.xxxxx
   ```

## Expected Output

```
==================================================
AIRTABLE MASTER - FULL TEST SUITE
==================================================

=== Syntax Validation ===
  [PASS] check_airtable_config.py syntax
  [PASS] discover_bases.py syntax
  [PASS] query_records.py syntax
  [PASS] manage_records.py syntax

=== Unit Tests ===
  [PASS] Unit tests - All passed

=== Integration Tests ===
  [PASS] Config check runs
  [PASS] Discovery JSON output - Found 96 bases
  [PASS] Query help
  [PASS] Manage help

=== Live API Tests ===
  [PASS] Live API tests - All passed

==================================================
TEST SUMMARY
==================================================
Duration: 34.68s
Total:    10
Passed:   10
==================================================

All tests passed!
```

## Test Files

| File | Tests | Network | Description |
|------|-------|---------|-------------|
| `run_tests.py` | 11 | Yes | Quick validation |
| `test_unit.py` | 25 | No | Syntax, args, error handling |
| `test_live_api.py` | 10 | Yes | Real API validation |

## Troubleshooting

### "pytest not installed"
```bash
pip install pytest
```

### "AIRTABLE_API_KEY not set"
Add PAT to `.env` at Nexus root.

### "Rate limited (429)"
Wait 30 seconds. Scripts have exponential backoff.

### Tests timeout
Increase timeout or use `--quick` for faster runs.
