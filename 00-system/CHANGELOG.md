# Changelog

All notable changes to Nexus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.82.0] - 2025-12-12

### Added

- **Nexus Sync Feature**: Update system files from upstream while protecting user data
  - New `update-nexus` skill - say "update nexus" to pull latest changes
  - `--check-update` command in nexus-loader.py to check for available updates
  - `--sync` command in nexus-loader.py to perform the sync
  - `--dry-run` flag to preview changes without applying
  - `--force` flag to skip uncommitted changes warning
  - `--skip-update-check` flag for faster startup (skip network check)
  - Automatic backup before sync (saved to `.sync-backup/`)
  - Menu shows update notice when updates are available

- **Startup Update Check**: Automatically checks for updates on startup
  - Non-blocking: network errors won't fail startup
  - `update_available` and `update_info` added to stats
  - Configurable via `--skip-update-check` flag

- **VERSION file**: Added `00-system/VERSION` for tracking releases

### Changed

- `nexus-loader.py` now handles sync commands in `main()`
- `orchestrator.md` menu template includes update notice section
- `README.md` updated with "Getting Nexus" and "Getting Updates" sections

### Protected Paths (Never Touched by Sync)

These folders are always safe during updates:
- `01-memory/` - Your goals, config, learnings
- `02-projects/` - Your projects
- `03-skills/` - Your custom skills
- `04-workspace/` - Your files
- `.env`, `.claude/` - Your secrets and settings

---

## [0.81.0] - 2025-12-11

### Added

- Integrations onboarding section in menu
- `add-integration` skill workflow improvements

### Changed

- Improved skill loading order for add-integration workflow

---

## [0.8.0] - 2025-12-10

### Added

- Major performance and UX overhaul
- Optional onboarding (Quick Start Mode)
- Smart defaults for immediate system use
- Learning tracker in user-config.yaml

### Changed

- System now works immediately without setup
- Onboarding skills are optional, not required
- Menu redesigned for clarity

---

## [0.7.0] - Previous

Initial public release with core features:
- Memory persistence system
- Project management
- Skill creation and execution
- Notion and Airtable integrations
- Learning skills for onboarding
