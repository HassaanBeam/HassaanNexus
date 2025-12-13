# Nexus Sync Feature - Implementation Plan

## Summary

Enable users to update their Nexus system files from the upstream template while protecting their personal data.

**User experience:** Say "update nexus" → system handles everything.

---

## What We're Building

```
┌─────────────────────────────────────────────────────┐
│  User: "update nexus"                               │
│       ↓                                             │
│  update-nexus skill (UX layer)                      │
│       ↓                                             │
│  nexus-loader.py --check-update (check)             │
│  nexus-loader.py --sync --force (apply)             │
│       ↓                                             │
│  Result: 00-system/ updated, user data untouched    │
└─────────────────────────────────────────────────────┘
```

---

## Components

| Component | Status | Description |
|-----------|--------|-------------|
| VERSION file | ✅ Done | `00-system/VERSION` = 0.82.0 |
| Sync functions | ✅ Done | In nexus-loader.py (not connected to main yet) |
| main() integration | ❌ TODO | Connect --sync and --check-update to functions |
| update-nexus skill | ❌ TODO | User-facing skill with UX |
| Startup integration | ❌ TODO | Check for updates on --startup |
| Menu notice | ❌ TODO | Show "Update available" in menu |
| Documentation | ❌ TODO | README, CHANGELOG |

---

## Implementation Order

### Phase 1: Make Commands Work
1. Connect `--check-update` → `check_for_updates()` in main()
2. Connect `--sync` → `sync_from_upstream()` in main()
3. Test both commands work

### Phase 2: Create Skill
1. Create `00-system/skills/system/update-nexus/SKILL.md`
2. Workflow: check → preview → confirm → sync → display results
3. Test skill triggers on "update nexus"

### Phase 3: Startup Integration (Optional)
1. Add update check to `--startup` output
2. Update orchestrator.md menu template
3. Show notice when update available

### Phase 4: Documentation
1. Update README with setup and update instructions
2. Create CHANGELOG.md
3. Mark repo as GitHub Template

---

## Key Design Decisions

### Why Skill-Based (not raw command)?
- Users interact naturally: "update nexus"
- Skill provides UX: preview, confirm, explain
- Consistent with Nexus philosophy

### Why Selective Checkout?
```bash
git checkout upstream/main -- 00-system/ CLAUDE.md README.md
```
- Only touches specified paths
- User folders never mentioned = never touched
- No merge conflicts possible
- Safe and predictable

### Why Backup?
- Before overwriting, copy existing files to `.sync-backup/`
- User can recover if needed
- Shows we care about their work

---

## Protected Folders (NEVER touched)

```
01-memory/      ← User's goals, learnings, config
02-projects/    ← User's projects
03-skills/      ← User's custom skills
04-workspace/   ← User's workspace files
.env            ← User's API keys
.claude/        ← User's Claude settings
```

---

## Synced Paths (Updated from upstream)

```
00-system/      ← System skills, core, documentation
CLAUDE.md       ← Entry point instructions
README.md       ← Repository documentation
```

---

## Files

| File | Purpose |
|------|---------|
| [overview.md](overview.md) | Problem, solution, components |
| [steps.md](steps.md) | Detailed implementation checklist |
| [technical-spec.md](../02-resources/technical-spec.md) | JSON schemas, git commands, UX examples |

---

## Version

**Current:** 0.82.0

**Next steps:** Complete Phase 1 (connect main()), then Phase 2 (create skill).
