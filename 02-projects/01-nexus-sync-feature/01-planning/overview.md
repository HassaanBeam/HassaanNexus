---
id: 01-nexus-sync-feature
name: Nexus Sync Feature
status: IN_PROGRESS
description: Add update-nexus skill and --sync/--check-update commands for pulling upstream updates while protecting user data
created: 2025-12-12
updated: 2025-12-12
---

# Nexus Sync Feature

## Problem Statement

Users who create their own Nexus from the template need a way to get system updates without:
- Learning git complexity (remotes, fetch, merge strategies)
- Risking their personal data (01-memory/, 02-projects/, 03-skills/, 04-workspace/)
- Dealing with merge conflicts

## Solution

A **skill-based approach** where users say "update nexus" and the system handles everything:

```
User: "update nexus"
  ↓
Triggers: update-nexus skill
  ↓
Skill calls: nexus-loader.py --sync
  ↓
Result: System files updated, user data untouched
```

## How It Works

### Distribution Model

1. **Your repo** (github.com/beamanalytica/Nexus-v4) = source of truth
2. **User clicks "Use this template"** → creates their own copy
3. **User clones their copy** → full Nexus with all folders visible
4. **User commits their data** → to their own repo
5. **User says "update nexus"** → pulls your system updates only

### What Syncs vs What's Protected

| Syncs (from you) | Protected (user's data) |
|------------------|------------------------|
| `00-system/` | `01-memory/` |
| `CLAUDE.md` | `02-projects/` |
| `README.md` | `03-skills/` |
| | `04-workspace/` |
| | `.env`, `.claude/` |

### Technical Mechanism

```bash
# The magic: selective git checkout
git fetch upstream
git checkout upstream/main -- 00-system/ CLAUDE.md README.md
```

This only updates specified paths. User's folders are never mentioned, so git doesn't touch them.

## Components

### 1. nexus-loader.py enhancements (DONE)
- `--check-update` - Fast check if updates available
- `--sync` - Perform the sync with backup
- `--dry-run` - Preview what would change
- `--force` - Skip uncommitted changes warning

### 2. update-nexus skill (TODO)
- Triggered by "update nexus", "sync nexus", "get updates"
- Provides UX: shows changes, confirms, displays results
- Calls nexus-loader.py internally

### 3. Startup integration (TODO)
- `--startup` optionally checks for updates
- Returns `update_available` in stats
- Menu shows notice when update available

### 4. Menu update notice (TODO)
- orchestrator.md template shows update notice
- "⚡ UPDATE AVAILABLE: v0.81 → v0.82"

## Success Criteria

- [ ] User says "update nexus" → skill handles everything
- [ ] Personal folders NEVER touched
- [ ] Works on Windows, Mac, Linux
- [ ] Automatic upstream remote setup (first time)
- [ ] Clear before/after display (version, changed files)
- [ ] Backup before overwriting system files
- [ ] Graceful errors (no git? no internet? uncommitted changes?)
- [ ] Menu shows update notice when available

## Current State

**Implemented:**
- VERSION file (0.82.0)
- Sync functions in nexus-loader.py
- Argparse for --sync, --check-update, --dry-run, --force
- main() now calls sync functions
- update-nexus skill created
- Startup checks for updates (with --skip-update-check option)
- Menu shows update notice when available
- README explains "Getting Nexus" and "Getting Updates"
- CHANGELOG.md created

**Not Implemented:**
- GitHub Template Repository setup (manual step)
- End-to-end testing with real upstream

## Version

Current: **0.82.0**
