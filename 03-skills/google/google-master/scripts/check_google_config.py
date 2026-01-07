#!/usr/bin/env python3
"""
Google Configuration Check

Quick pre-flight check for Google integration.
Returns structured output for AI consumption.
"""

import sys
import json
import argparse
from pathlib import Path

# Find Nexus root
def find_nexus_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()

NEXUS_ROOT = find_nexus_root()
TOKEN_PATH = NEXUS_ROOT / "01-memory" / "integrations" / "google-token.json"
CREDENTIALS_PATH = NEXUS_ROOT / "00-system" / "google-credentials.json"

def check_dependencies():
    """Check if required packages are installed."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        return True
    except ImportError:
        return False

def check_config(json_output=False):
    """Check Google configuration status."""
    deps_ok = check_dependencies()
    creds_ok = CREDENTIALS_PATH.exists()
    token_ok = TOKEN_PATH.exists()

    # Determine status and action
    if not deps_ok:
        status = "not_configured"
        ai_action = "install_dependencies"
        message = "Missing Python dependencies"
        fix = "pip install google-auth google-auth-oauthlib google-api-python-client"
        exit_code = 2
    elif not creds_ok:
        status = "not_configured"
        ai_action = "need_credentials"
        message = "OAuth credentials not found"
        fix = "Download credentials from Google Cloud Console"
        exit_code = 2
    elif not token_ok:
        status = "partial"
        ai_action = "need_login"
        message = "Credentials found, but not authenticated"
        fix = "python 00-system/skills/google/google-master/scripts/google_auth.py --login"
        exit_code = 1
    else:
        # Try to validate token
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request

            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
            if creds and creds.valid:
                status = "configured"
                ai_action = "proceed"
                message = "Ready to use Google services"
                fix = None
                exit_code = 0
            elif creds and creds.expired and creds.refresh_token:
                # Try refresh
                try:
                    creds.refresh(Request())
                    # Save refreshed token
                    with open(TOKEN_PATH, 'w') as f:
                        f.write(creds.to_json())
                    status = "configured"
                    ai_action = "proceed"
                    message = "Token refreshed, ready to use"
                    fix = None
                    exit_code = 0
                except:
                    status = "partial"
                    ai_action = "need_login"
                    message = "Token expired and refresh failed"
                    fix = "python 00-system/skills/google/google-master/scripts/google_auth.py --login"
                    exit_code = 1
            else:
                status = "partial"
                ai_action = "need_login"
                message = "Token invalid or expired"
                fix = "python 00-system/skills/google/google-master/scripts/google_auth.py --login"
                exit_code = 1
        except Exception as e:
            status = "partial"
            ai_action = "need_login"
            message = f"Token validation failed: {str(e)}"
            fix = "python 00-system/skills/google/google-master/scripts/google_auth.py --login"
            exit_code = 1

    result = {
        "status": status,
        "exit_code": exit_code,
        "ai_action": ai_action,
        "message": message,
        "checks": {
            "dependencies": deps_ok,
            "credentials_file": creds_ok,
            "token_file": token_ok
        },
        "paths": {
            "credentials": str(CREDENTIALS_PATH),
            "token": str(TOKEN_PATH)
        }
    }

    if fix:
        result["fix"] = fix

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        if exit_code == 0:
            print("ALL CHECKS PASSED")
            print("Ready to use Google services (Gmail, Docs, Sheets, Calendar)")
        else:
            print(f"STATUS: {status.upper()}")
            print(f"Issue: {message}")
            if fix:
                print(f"Fix: {fix}")

    sys.exit(exit_code)

def main():
    parser = argparse.ArgumentParser(description="Check Google configuration")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    check_config(json_output=args.json)

if __name__ == "__main__":
    main()
