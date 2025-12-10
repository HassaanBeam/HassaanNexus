#!/usr/bin/env python3
"""
Query Notion Database - Search and filter the Beam Nexus Skills database

Usage:
    python query_db.py [--team TEAM] [--integration INTEGRATION] [--owner OWNER_ID] [--name NAME]

Examples:
    python query_db.py --team General
    python query_db.py --integration "Beam AI"
    python query_db.py --name notion
    python query_db.py --team Solutions --integration "Beam AI"

Returns:
    JSON array of matching skills with metadata
"""

import sys
import os
import json
import argparse
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed")
    print("Install with: pip install requests")
    sys.exit(1)


def find_nexus_root():
    """Find Nexus root directory (contains CLAUDE.md)"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def load_env_file(env_path):
    """Load .env file and return as dict"""
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


def query_notion_database(api_key, database_id, filters=None, sorts=None, page_size=100):
    """
    Query Notion database with optional filters and sorts

    Args:
        api_key: Notion API key
        database_id: Database ID to query
        filters: Dict of filter conditions (optional)
        sorts: List of sort conditions (optional)
        page_size: Number of results per page (default 100, max 100)

    Returns:
        List of database entries (pages)
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {}
    if filters:
        body["filter"] = filters
    if sorts:
        body["sorts"] = sorts
    if page_size:
        body["page_size"] = min(page_size, 100)

    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        if start_cursor:
            body["start_cursor"] = start_cursor

        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)

            if response.status_code == 200:
                data = response.json()
                all_results.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
            elif response.status_code == 401:
                print("[ERROR] 401 Unauthorized - Invalid API key", file=sys.stderr)
                return None
            elif response.status_code == 404:
                print(f"[ERROR] 404 Not Found - Database not accessible: {database_id}", file=sys.stderr)
                return None
            else:
                print(f"[ERROR] Query failed: {response.status_code}", file=sys.stderr)
                print(f"Response: {response.text}", file=sys.stderr)
                return None

        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out", file=sys.stderr)
            return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network error: {e}", file=sys.stderr)
            return None

    return all_results


def extract_property_value(prop):
    """Extract value from Notion property object"""
    if not prop:
        return None

    prop_type = prop.get("type")

    if prop_type == "title":
        text_objects = prop.get("title", [])
        return " ".join([t.get("plain_text", "") for t in text_objects])

    elif prop_type == "rich_text":
        text_objects = prop.get("rich_text", [])
        return " ".join([t.get("plain_text", "") for t in text_objects])

    elif prop_type == "select":
        select = prop.get("select")
        return select.get("name") if select else None

    elif prop_type == "multi_select":
        items = prop.get("multi_select", [])
        return [item.get("name") for item in items]

    elif prop_type == "people":
        people = prop.get("people", [])
        return [p.get("name", p.get("id")) for p in people]

    elif prop_type == "date":
        date_obj = prop.get("date")
        return date_obj.get("start") if date_obj else None

    elif prop_type == "files":
        files = prop.get("files", [])
        return [f.get("name") for f in files]

    return None


def format_result(page):
    """Format a Notion page result into readable dict"""
    props = page.get("properties", {})

    return {
        "id": page.get("id"),
        "url": page.get("url"),
        "skill_name": extract_property_value(props.get("Skill Name")),
        "description": extract_property_value(props.get("Description")),
        "purpose": extract_property_value(props.get("Purpose")),
        "team": extract_property_value(props.get("Team")),
        "integrations": extract_property_value(props.get("Integration")),
        "owner": extract_property_value(props.get("Owner")),
        "created": extract_property_value(props.get("Created")),
        "files": extract_property_value(props.get("Skill"))
    }


def build_filters(args):
    """Build Notion API filter object from command-line arguments"""
    conditions = []

    if args.team:
        conditions.append({
            "property": "Team",
            "select": {"equals": args.team}
        })

    if args.integration:
        conditions.append({
            "property": "Integration",
            "multi_select": {"contains": args.integration}
        })

    if args.owner:
        conditions.append({
            "property": "Owner",
            "people": {"contains": args.owner}
        })

    if args.name:
        conditions.append({
            "property": "Skill Name",
            "title": {"contains": args.name.lower()}
        })

    if len(conditions) == 0:
        return None
    elif len(conditions) == 1:
        return conditions[0]
    else:
        return {"and": conditions}


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Query Beam Nexus Skills database in Notion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query_db.py --team General
  python query_db.py --integration "Beam AI"
  python query_db.py --name notion
  python query_db.py --team Solutions --integration Linear
        """
    )
    parser.add_argument("--team", help="Filter by team (General, Solutions, Engineering, Sales)")
    parser.add_argument("--integration", help="Filter by integration (Beam AI, Linear, Notion, etc.)")
    parser.add_argument("--owner", help="Filter by owner user ID")
    parser.add_argument("--name", help="Filter by skill name (partial match)")
    parser.add_argument("--sort", choices=["created", "name"], default="created", help="Sort results by (default: created)")
    parser.add_argument("--limit", type=int, help="Limit number of results")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    # Find Nexus root and load config
    root = find_nexus_root()
    env_path = root / '.env'
    env_vars = load_env_file(env_path)

    # Get API credentials
    api_key = env_vars.get('NOTION_API_KEY') or os.getenv('NOTION_API_KEY')
    database_id = env_vars.get('NOTION_SKILLS_DB_ID') or env_vars.get('NOTION_DATABASE_ID') or os.getenv('NOTION_DATABASE_ID')

    if not api_key:
        print("[ERROR] NOTION_API_KEY not found in .env or environment", file=sys.stderr)
        print("Add to .env: NOTION_API_KEY=secret_xxxxx", file=sys.stderr)
        sys.exit(1)

    if not database_id:
        print("[ERROR] NOTION_SKILLS_DB_ID not found in .env or environment", file=sys.stderr)
        print("Add to .env: NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e", file=sys.stderr)
        sys.exit(1)

    # Build filter and sort
    filters = build_filters(args)

    sorts = []
    if args.sort == "created":
        sorts = [{"property": "Created", "direction": "descending"}]
    elif args.sort == "name":
        sorts = [{"property": "Skill Name", "direction": "ascending"}]

    # Query database
    print(f"[INFO] Querying Notion database...", file=sys.stderr)
    if filters:
        print(f"[INFO] Filters: {json.dumps(filters, indent=2)}", file=sys.stderr)

    results = query_notion_database(api_key, database_id, filters, sorts)

    if results is None:
        sys.exit(1)

    # Format results
    formatted = [format_result(page) for page in results]

    # Apply limit
    if args.limit and args.limit > 0:
        formatted = formatted[:args.limit]

    # Output
    if args.json:
        print(json.dumps(formatted, indent=2))
    else:
        print(f"\n[RESULTS] Found {len(formatted)} skills\n", file=sys.stderr)
        for i, skill in enumerate(formatted, 1):
            print(f"{i}. {skill['skill_name']}")
            print(f"   Team: {skill['team']}")
            print(f"   Description: {skill['description'][:80]}...")
            if skill['integrations']:
                print(f"   Integrations: {', '.join(skill['integrations'])}")
            print(f"   Created: {skill['created']}")
            print(f"   URL: {skill['url']}")
            print()

    sys.exit(0)


if __name__ == "__main__":
    main()
