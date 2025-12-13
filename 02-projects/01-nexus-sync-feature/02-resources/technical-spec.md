# Technical Specification

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER EXPERIENCE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User says: "update nexus"                                  │
│       ↓                                                     │
│  Smart routing triggers: update-nexus skill                 │
│       ↓                                                     │
│  Skill runs: nexus-loader.py --check-update                 │
│       ↓                                                     │
│  Skill displays: changes preview, asks confirmation         │
│       ↓                                                     │
│  Skill runs: nexus-loader.py --sync --force                 │
│       ↓                                                     │
│  Skill displays: success, backup location, next steps       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Command Interface

```bash
# Check if updates available (fast, read-only)
python 00-system/core/nexus-loader.py --check-update

# Perform sync (modifies files)
python 00-system/core/nexus-loader.py --sync

# Preview changes without applying
python 00-system/core/nexus-loader.py --sync --dry-run

# Skip uncommitted changes warning
python 00-system/core/nexus-loader.py --sync --force
```

## JSON Output Schemas

### --check-update Response

```json
{
  "checked": true,
  "update_available": true,
  "local_version": "0.81.0",
  "upstream_version": "0.82.0",
  "upstream_url": "https://github.com/beamanalytica/Nexus-v4.git",
  "changed_files": [
    "00-system/core/nexus-loader.py",
    "00-system/skills/system/new-skill/SKILL.md",
    "CLAUDE.md"
  ],
  "changes_count": 3,
  "error": null
}
```

**Error case:**
```json
{
  "checked": false,
  "update_available": false,
  "local_version": "0.81.0",
  "upstream_version": null,
  "error": "Could not reach upstream: network timeout"
}
```

### --sync Response

**Success:**
```json
{
  "success": true,
  "dry_run": false,
  "local_version": "0.81.0",
  "upstream_version": "0.82.0",
  "files_updated": ["00-system/", "CLAUDE.md", "README.md"],
  "backup_path": ".sync-backup/2025-12-12-143052/",
  "message": "Updated 3 paths from upstream",
  "error": null
}
```

**Dry run:**
```json
{
  "success": true,
  "dry_run": true,
  "local_version": "0.81.0",
  "upstream_version": "0.82.0",
  "files_to_update": [
    "00-system/core/nexus-loader.py",
    "CLAUDE.md"
  ],
  "message": "Would update 2 files",
  "error": null
}
```

**Already up-to-date:**
```json
{
  "success": true,
  "local_version": "0.82.0",
  "upstream_version": "0.82.0",
  "message": "Already up-to-date",
  "error": null
}
```

**Error (uncommitted changes):**
```json
{
  "success": false,
  "error": "Uncommitted changes detected. Commit first or use --force.",
  "uncommitted_changes": [
    "M 01-memory/goals.md",
    "?? 03-skills/my-skill/"
  ]
}
```

## Configuration

### Default Upstream URL

Defined in `nexus-loader.py`:
```python
DEFAULT_UPSTREAM_URL = "https://github.com/beamanalytica/Nexus-v4.git"
```

### User Override (Optional)

In `01-memory/user-config.yaml`:
```yaml
sync:
  upstream_url: "https://github.com/custom/Nexus-v4.git"
```

### Sync Paths

```python
SYNC_PATHS = [
    "00-system/",
    "CLAUDE.md",
    "README.md",
]
```

### Protected Paths (Never Touched)

```python
PROTECTED_PATHS = [
    "01-memory/",
    "02-projects/",
    "03-skills/",
    "04-workspace/",
    ".env",
    ".claude/",
    ".sync-backup/",
]
```

## Git Operations

### First-Time Setup (Automatic)

```bash
# Check if upstream remote exists
git remote get-url upstream
# If not found, add it:
git remote add upstream https://github.com/beamanalytica/Nexus-v4.git
```

### Check for Updates

```bash
# Fetch upstream refs (fast)
git fetch upstream --quiet

# Compare 00-system/ hashes
git rev-parse HEAD:00-system
git rev-parse upstream/main:00-system

# Get changed files list
git diff --name-only HEAD upstream/main -- 00-system/ CLAUDE.md README.md
```

### Perform Sync

```bash
# Fetch upstream
git fetch upstream

# Selective checkout (the magic - only touches specified paths)
git checkout upstream/main -- 00-system/
git checkout upstream/main -- CLAUDE.md
git checkout upstream/main -- README.md
```

## Backup System

**Location:** `.sync-backup/YYYY-MM-DD-HHMMSS/`

**Process:**
1. Before any checkout, copy existing files that will be overwritten
2. Preserve directory structure in backup
3. Only backup files that exist locally AND will change

**Example backup structure:**
```
.sync-backup/
└── 2025-12-12-143052/
    ├── 00-system/
    │   └── core/
    │       └── nexus-loader.py
    └── CLAUDE.md
```

## update-nexus Skill

### Trigger Phrases

```yaml
description: Load when user says "update nexus", "sync nexus", "get updates", "upgrade nexus", "pull updates", or asks "is there an update".
```

### Workflow Output

**Step 1: Check**
```
Checking for updates...
```

**Step 2: Preview (if updates available)**
```
════════════════════════════════════════════════════════════
                   UPDATE AVAILABLE
════════════════════════════════════════════════════════════

Current version:  0.81.0
Available:        0.82.0

Files to update:
  • 00-system/core/nexus-loader.py
  • 00-system/skills/system/update-nexus/SKILL.md
  • CLAUDE.md

Protected (will NOT be touched):
  01-memory/  02-projects/  03-skills/  04-workspace/

════════════════════════════════════════════════════════════
```

**Step 3: Confirm**
```
Proceed with update? (yes/no)
```

**Step 4: Success**
```
════════════════════════════════════════════════════════════
✅ UPDATE COMPLETE

Updated: 0.81.0 → 0.82.0

Backup saved to: .sync-backup/2025-12-12-143052/

To commit this update:
  git add . && git commit -m "Update Nexus to v0.82.0"
════════════════════════════════════════════════════════════
```

**Already up-to-date:**
```
════════════════════════════════════════════════════════════
✓ Already up-to-date (v0.82.0)
════════════════════════════════════════════════════════════
```

## Startup Integration (Optional)

### Stats Addition

```json
{
  "stats": {
    "update_available": true,
    "update_info": {
      "local_version": "0.81.0",
      "upstream_version": "0.82.0",
      "changes_count": 5
    }
  }
}
```

### Menu Notice

```
⚡ UPDATE AVAILABLE: v0.81.0 → v0.82.0
   Say 'update nexus' to get latest improvements
```

## Error Handling

| Scenario | Response |
|----------|----------|
| Git not installed | `"error": "Git is not installed"` |
| Not a git repo | `"error": "Not a git repository"` |
| Network failure | `"error": "Could not reach upstream: ..."` |
| Uncommitted changes | `"error": "Uncommitted changes detected..."` + list |
| Backup failed | `"error": "Backup failed: ..."` |
| Checkout failed | Continue with other paths, report partial success |

## Version File

**Location:** `00-system/VERSION`

**Format:** Semantic versioning
```
0.82.0
```

**Read by:** `get_local_version()` function
