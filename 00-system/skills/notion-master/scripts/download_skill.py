#!/usr/bin/env python3
"""
Download Skill from Notion - Downloads skill file from Notion database entry

Usage:
    python download_skill.py <page_id> [--output-dir DIR]

Examples:
    python download_skill.py abc123-page-id
    python download_skill.py abc123-page-id --output-dir /tmp

Returns:
    Exit code 0 if successful, 1 if error
"""

import sys
import os
import json
import argparse
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed")
    print("Install with: pip install requests")
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


def get_page_properties(api_key, page_id):
    """
    Get Notion page properties

    Returns:
        Dict with page metadata or None if error
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"[ERROR] Page not found: {page_id}", file=sys.stderr)
            return None
        elif response.status_code == 401:
            print("[ERROR] Unauthorized - invalid API key", file=sys.stderr)
            return None
        else:
            print(f"[ERROR] Failed to get page: {response.status_code}", file=sys.stderr)
            print(f"Response: {response.text}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}", file=sys.stderr)
        return None


def extract_file_url(page_data):
    """
    Extract file URL from Notion page properties

    Returns:
        Tuple of (file_url, file_name) or (None, None) if no file
    """
    props = page_data.get("properties", {})
    skill_prop = props.get("Skill", {})

    files = skill_prop.get("files", [])
    if not files:
        return None, None

    # Get first file
    file_obj = files[0]
    file_type = file_obj.get("type")

    if file_type == "external":
        url = file_obj.get("external", {}).get("url")
    elif file_type == "file":
        url = file_obj.get("file", {}).get("url")
    else:
        return None, None

    name = file_obj.get("name", "skill-file.txt")

    return url, name


def download_file(url, output_path):
    """
    Download file from URL to output path

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[INFO] Downloading: {output_path.name}", file=sys.stderr)

        response = requests.get(url, timeout=60, stream=True)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            file_size = output_path.stat().st_size
            print(f"[OK] Downloaded: {file_size:,} bytes", file=sys.stderr)
            return True
        else:
            print(f"[ERROR] Download failed: {response.status_code}", file=sys.stderr)
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Download failed: {e}", file=sys.stderr)
        return False


def extract_skill_metadata(page_data):
    """Extract skill metadata from Notion page"""
    props = page_data.get("properties", {})

    def get_text(prop):
        if not prop:
            return ""
        prop_type = prop.get("type")
        if prop_type == "title":
            return " ".join([t.get("plain_text", "") for t in prop.get("title", [])])
        elif prop_type == "rich_text":
            return " ".join([t.get("plain_text", "") for t in prop.get("rich_text", [])])
        return ""

    def get_select(prop):
        if not prop:
            return None
        select = prop.get("select")
        return select.get("name") if select else None

    return {
        "skill_name": get_text(props.get("Skill Name")),
        "description": get_text(props.get("Description")),
        "purpose": get_text(props.get("Purpose")),
        "team": get_select(props.get("Team")),
        "url": page_data.get("url")
    }


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Download skill file from Notion page",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python download_skill.py abc123-page-id
  python download_skill.py abc123-page-id --output-dir /tmp
        """
    )
    parser.add_argument("page_id", help="Notion page ID")
    parser.add_argument("--output-dir", help="Output directory (default: current directory)")
    parser.add_argument("--metadata", action="store_true", help="Also output metadata JSON")

    args = parser.parse_args()

    # Find Nexus root and load config
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    # Get API key
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found in .env or environment", file=sys.stderr)
        sys.exit(1)

    # Get page data
    print(f"[INFO] Fetching page: {args.page_id}", file=sys.stderr)
    page_data = get_page_properties(api_key, args.page_id)

    if not page_data:
        sys.exit(1)

    # Extract file URL
    file_url, file_name = extract_file_url(page_data)

    if not file_url:
        print("[ERROR] No file attached to this page", file=sys.stderr)
        print("[HINT] Check the 'Skill' property has a file attachment", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd()

    output_path = output_dir / file_name

    # Download file
    success = download_file(file_url, output_path)

    if not success:
        sys.exit(1)

    # Output metadata if requested
    if args.metadata:
        metadata = extract_skill_metadata(page_data)
        metadata["downloaded_file"] = str(output_path)
        metadata["file_name"] = file_name
        print(json.dumps(metadata, indent=2))
    else:
        print(f"\n[SUCCESS] Skill downloaded to: {output_path}")

    sys.exit(0)


if __name__ == "__main__":
    main()
