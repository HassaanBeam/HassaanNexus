#!/usr/bin/env python3
"""
Get Fathom Meeting Transcript

Fetches the full speaker-attributed transcript for a Fathom recording.

Usage:
    python get_transcript.py --recording-id abc123-def456
    python get_transcript.py --recording-id abc123 --json
    python get_transcript.py --recording-id abc123 --output transcript.txt
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from fathom_client import get_client, FathomError


def format_transcript(transcript_data):
    """Format transcript for readable display."""
    output = []

    # Get recording metadata if available
    recording = transcript_data.get('recording', {})
    if recording:
        output.append(f"Meeting: {recording.get('title', 'Unknown')}")
        output.append(f"Date: {recording.get('created_at', '')[:10]}")
        output.append("")

    output.append("=" * 60)
    output.append("TRANSCRIPT")
    output.append("=" * 60)
    output.append("")

    # Format transcript segments
    segments = transcript_data.get('transcript', [])
    if not segments:
        # Try alternate structure
        segments = transcript_data.get('segments', [])

    if not segments:
        output.append("No transcript segments found")
        return "\n".join(output)

    current_speaker = None
    for segment in segments:
        speaker = segment.get('speaker', segment.get('speaker_name', 'Unknown'))
        text = segment.get('text', segment.get('content', ''))
        timestamp = segment.get('start', segment.get('timestamp', ''))

        # Format timestamp if numeric
        if isinstance(timestamp, (int, float)):
            mins = int(timestamp // 60)
            secs = int(timestamp % 60)
            timestamp = f"[{mins:02d}:{secs:02d}]"
        elif timestamp:
            timestamp = f"[{timestamp}]"

        # Only show speaker name when it changes
        if speaker != current_speaker:
            output.append(f"\n{speaker}:")
            current_speaker = speaker

        if timestamp:
            output.append(f"  {timestamp} {text}")
        else:
            output.append(f"  {text}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Get Fathom meeting transcript')
    parser.add_argument('--recording-id', '-r', required=True, help='Recording UUID from Fathom')
    parser.add_argument('--json', '-j', action='store_true', help='Output raw JSON')
    parser.add_argument('--output', '-o', help='Save transcript to file')
    parser.add_argument('--include-metadata', '-m', action='store_true', help='Include recording metadata')

    args = parser.parse_args()

    try:
        client = get_client()

        # Fetch transcript
        transcript = client.get_transcript(args.recording_id)

        # Optionally get recording metadata
        if args.include_metadata:
            try:
                recording = client.get_recording(args.recording_id)
                transcript['recording'] = recording
            except FathomError:
                pass  # Metadata is optional

        # Output
        if args.json:
            output = json.dumps(transcript, indent=2)
        else:
            output = format_transcript(transcript)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Transcript saved to: {args.output}")
        else:
            print(output)

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("Run: python fathom_client.py to test your setup", file=sys.stderr)
        sys.exit(1)
    except FathomError as e:
        if e.status_code == 404:
            print(f"Recording not found: {args.recording_id}", file=sys.stderr)
            print("Use list_meetings.py to find valid recording IDs", file=sys.stderr)
        else:
            print(f"API error ({e.status_code}): {e.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
