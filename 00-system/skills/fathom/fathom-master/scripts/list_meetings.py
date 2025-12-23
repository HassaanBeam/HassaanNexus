#!/usr/bin/env python3
"""
List Fathom Meetings

Lists meetings from Fathom with optional filtering by domain, date range,
and includes AI-generated summaries and action items.

Usage:
    python list_meetings.py                          # List recent meetings
    python list_meetings.py --domain smartly.io     # Filter by attendee domain
    python list_meetings.py --days 7                # Last 7 days only
    python list_meetings.py --json                  # Output as JSON
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from fathom_client import get_client, FathomError


def format_meeting(meeting, verbose=False):
    """Format a single meeting for display."""
    title = meeting.get('title', 'Untitled')
    created = meeting.get('created_at', '')[:10]
    recording_id = meeting.get('recording_id', 'N/A')

    # Get attendees
    attendees = meeting.get('attendees', [])
    attendee_names = [a.get('name', a.get('email', 'Unknown')) for a in attendees[:3]]
    attendee_str = ', '.join(attendee_names)
    if len(attendees) > 3:
        attendee_str += f' +{len(attendees) - 3} more'

    output = f"\n{title}"
    output += f"\n  Date: {created}"
    output += f"\n  Recording ID: {recording_id}"
    output += f"\n  Attendees: {attendee_str}"

    if verbose:
        # Include summary if available
        summary = meeting.get('summary', {})
        if summary:
            output += f"\n  Summary: {summary.get('short_summary', 'N/A')[:200]}"

        # Include action items if available
        action_items = meeting.get('action_items', [])
        if action_items:
            output += f"\n  Action Items: {len(action_items)}"
            for item in action_items[:3]:
                output += f"\n    - {item.get('text', '')[:80]}"

    return output


def main():
    parser = argparse.ArgumentParser(description='List Fathom meetings')
    parser.add_argument('--domain', '-d', help='Filter by attendee email domain (e.g., smartly.io)')
    parser.add_argument('--days', '-D', type=int, help='Only show meetings from last N days')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Maximum meetings to return (default: 20)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Include summaries and action items')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--no-summary', action='store_true', help='Exclude AI summaries (faster)')
    parser.add_argument('--no-actions', action='store_true', help='Exclude action items (faster)')

    args = parser.parse_args()

    try:
        client = get_client()

        # Calculate date filter
        created_after = None
        if args.days:
            created_after = (datetime.now() - timedelta(days=args.days)).isoformat()

        # Fetch meetings
        result = client.list_meetings(
            domain=args.domain,
            include_summary=not args.no_summary,
            include_action_items=not args.no_actions,
            created_after=created_after,
            limit=args.limit
        )

        meetings = result.get('meetings', [])

        if args.json:
            print(json.dumps(meetings, indent=2))
            return

        # Display results
        if not meetings:
            print("No meetings found matching criteria")
            return

        print(f"Found {len(meetings)} meeting(s)")
        if args.domain:
            print(f"Filtered by domain: {args.domain}")
        if args.days:
            print(f"From last {args.days} days")

        print("-" * 50)

        for meeting in meetings:
            print(format_meeting(meeting, verbose=args.verbose))

        print("\n" + "-" * 50)
        print(f"Use --json for full data or get_transcript.py --recording-id <ID> for transcript")

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("Run: python fathom_client.py to test your setup", file=sys.stderr)
        sys.exit(1)
    except FathomError as e:
        print(f"API error ({e.status_code}): {e.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
