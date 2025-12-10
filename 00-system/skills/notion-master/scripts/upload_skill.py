#!/usr/bin/env python3
"""
Upload Skill to Notion - Creates database entry with file attachment using 3-step upload API

Usage:
    python upload_skill.py <skill_path> --team TEAM [--integration INT1,INT2]

Examples:
    python upload_skill.py 03-skills/my-skill --team General
    python upload_skill.py 03-skills/beam-agents --team Solutions --integration "Beam AI"

Returns:
    Exit code 0 if successful, 1 if error
"""

import sys
import os
import json
import argparse
import re
from pathlib import Path
from datetime import date

try:
    import requests
    import yaml
except ImportError:
    print("[ERROR] Missing dependencies")
    print("Install with: pip install requests pyyaml")
    sys.exit(1)


def find_nexus_root():
    """Find Nexus root directory"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def load_env_file(env_path):
    """Load .env file"""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")

    return env_vars


def load_user_config(config_path):
    """Load user-config.yaml"""
    if not config_path.exists():
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Handle YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            yaml_content = parts[1] if len(parts) >= 2 else content
        else:
            yaml_content = content

        try:
            return yaml.safe_load(yaml_content) or {}
        except yaml.YAMLError:
            return {}


def read_skill_md(skill_path):
    """
    Read and parse SKILL.md file

    Returns:
        Dict with {name, description, purpose, content}
    """
    skill_md = skill_path / 'SKILL.md'

    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}", file=sys.stderr)
        return None

    content = skill_md.read_text(encoding='utf-8')

    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print("[ERROR] Invalid SKILL.md format (missing YAML frontmatter)", file=sys.stderr)
        return None

    frontmatter_text = match.group(1)
    body = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        print(f"[ERROR] Invalid YAML frontmatter: {e}", file=sys.stderr)
        return None

    # Extract Purpose section
    purpose_match = re.search(r'^## Purpose\s*\n\n(.+?)(?=\n##|\Z)', body, re.MULTILINE | re.DOTALL)
    purpose = purpose_match.group(1).strip() if purpose_match else ""

    return {
        "name": frontmatter.get("name", ""),
        "description": frontmatter.get("description", ""),
        "purpose": purpose,
        "content": content
    }


def create_file_upload(api_key):
    """
    Step 1: Create file upload object

    Returns:
        file_upload_id or None
    """
    url = "https://api.notion.com/v1/file_uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json={}, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data.get("id")
        else:
            print(f"[ERROR] Failed to create upload: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def upload_file_content(api_key, file_upload_id, file_path):
    """
    Step 2: Upload file content

    Returns:
        True if successful
    """
    url = f"https://api.notion.com/v1/file_uploads/{file_upload_id}/send"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f)}
            response = requests.post(url, headers=headers, files=files, timeout=60)

        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            if status == "uploaded":
                return True
            else:
                print(f"[ERROR] Upload status: {status}", file=sys.stderr)
                return False
        else:
            print(f"[ERROR] File upload failed: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return False


def create_database_entry(api_key, database_id, skill_data, file_upload_id, file_name, user_id):
    """
    Step 3: Create database entry with file attachment

    Returns:
        Created page object or None
    """
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # Build properties
    properties = {
        "Skill Name": {
            "title": [{"text": {"content": skill_data["name"]}}]
        },
        "Description": {
            "rich_text": [{"text": {"content": skill_data["description"]}}]
        },
        "Team": {
            "select": {"name": skill_data["team"]}
        },
        "Created": {
            "date": {"start": str(date.today())}
        },
        "Skill": {
            "files": [{
                "type": "file_upload",
                "file_upload": {"id": file_upload_id},
                "name": file_name
            }]
        }
    }

    # Add optional properties
    if skill_data.get("purpose"):
        properties["Purpose"] = {
            "rich_text": [{"text": {"content": skill_data["purpose"]}}]
        }

    if skill_data.get("integrations"):
        properties["Integration"] = {
            "multi_select": [{"name": integ} for integ in skill_data["integrations"]]
        }

    if user_id:
        properties["Owner"] = {
            "people": [{"id": user_id}]
        }

    body = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Failed to create page: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Upload skill to Notion database with file attachment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python upload_skill.py 03-skills/my-skill --team General
  python upload_skill.py 03-skills/beam-agents --team Solutions --integration "Beam AI,Linear"
        """
    )
    parser.add_argument("skill_path", help="Path to skill folder")
    parser.add_argument("--team", required=True, help="Team (General, Solutions, Engineering, Sales)")
    parser.add_argument("--integration", help="Comma-separated integrations (e.g., 'Beam AI,Linear')")
    parser.add_argument("--file", help="Skill file to upload (default: auto-package to .skill)")

    args = parser.parse_args()

    # Validate skill path
    skill_path = Path(args.skill_path).resolve()
    if not skill_path.exists() or not skill_path.is_dir():
        print(f"[ERROR] Skill folder not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Read skill metadata
    print(f"[INFO] Reading skill: {skill_path.name}", file=sys.stderr)
    skill_data = read_skill_md(skill_path)

    if not skill_data:
        sys.exit(1)

    skill_data["team"] = args.team

    if args.integration:
        skill_data["integrations"] = [i.strip() for i in args.integration.split(',')]

    # Find Nexus root and load config
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    config_path = root / '01-memory' / 'user-config.yaml'
    user_config = load_user_config(config_path)

    # Get credentials
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')
    database_id = env_vars.get('NOTION_SKILLS_DB_ID') or env_vars.get('NOTION_DATABASE_ID')
    user_id = user_config.get('integrations', {}).get('notion', {}).get('user_id')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    if not database_id:
        print("[ERROR] NOTION_SKILLS_DB_ID not found", file=sys.stderr)
        sys.exit(1)

    if not user_id:
        print("[WARN] notion_user_id not set in user-config.yaml", file=sys.stderr)
        print("[WARN] Owner field will not be set", file=sys.stderr)

    # Determine file to upload
    if args.file:
        file_path = Path(args.file)
    else:
        # Use SKILL.md directly (upload as .txt)
        skill_md = skill_path / 'SKILL.md'
        file_path = skill_md

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    file_name = f"{skill_data['name']}.txt" if file_path.name == 'SKILL.md' else file_path.name

    print(f"\n[UPLOAD] Skill: {skill_data['name']}", file=sys.stderr)
    print(f"[UPLOAD] Team: {skill_data['team']}", file=sys.stderr)
    print(f"[UPLOAD] File: {file_name} ({file_path.stat().st_size:,} bytes)", file=sys.stderr)
    print()

    # Step 1: Create upload object
    print("[1/3] Creating upload object...", file=sys.stderr)
    file_upload_id = create_file_upload(api_key)

    if not file_upload_id:
        sys.exit(1)

    print(f"[OK] Upload ID: {file_upload_id[:8]}...", file=sys.stderr)

    # Step 2: Upload file
    print("[2/3] Uploading file...", file=sys.stderr)
    success = upload_file_content(api_key, file_upload_id, file_path)

    if not success:
        sys.exit(1)

    print("[OK] File uploaded", file=sys.stderr)

    # Step 3: Create page
    print("[3/3] Creating database entry...", file=sys.stderr)
    page = create_database_entry(api_key, database_id, skill_data, file_upload_id, file_name, user_id)

    if not page:
        sys.exit(1)

    page_url = page.get("url")
    print(f"\n[SUCCESS] Skill uploaded to Notion!", file=sys.stderr)
    print(f"[SUCCESS] URL: {page_url}", file=sys.stderr)

    # Output JSON for programmatic use
    print(json.dumps({"page_id": page.get("id"), "url": page_url}, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
