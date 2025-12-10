---
name: notion-master
description: Shared resource library for Notion integration skills. DO NOT load directly - this provides common references (setup, API docs, error handling, database schema) and scripts used by query-notion-db, import-skill-to-nexus, and export-skill-to-notion.
---

# Notion Master

**This is NOT a user-facing skill.** It's a shared resource library referenced by the 3 Notion integration skills.

## Purpose

Provides shared resources to eliminate duplication across:
- `query-notion-db` - Browse and search Notion skills database
- `import-skill-to-nexus` - Download skills from Notion to local Nexus
- `export-skill-to-notion` - Push skills to Notion for team sharing

**Instead of loading this skill**, users directly invoke the specific skill they need above.

---

## Architecture: DRY Principle

**Problem solved:** The 3 Notion skills had 950 lines of duplicated content (setup wizard 3x, API docs 3x, error tables 3x).

**Solution:** Extract shared content into `notion-master/references/` and `notion-master/scripts/`, then reference from each skill.

**Result:** 60% context reduction (950 → 370 lines in SKILL.md files)

---

## Shared Resources

All 3 Notion skills reference these resources (progressive disclosure).

### references/

**[setup-guide.md](references/setup-guide.md)** - Complete setup wizard
- Getting Notion API key
- Finding database ID
- Configuring .env and user-config.yaml
- Getting user's Notion ID

**[api-reference.md](references/api-reference.md)** - Notion API patterns
- Database query API
- File upload API (3-step process)
- File download API (3-step process)
- Common curl examples

**[error-handling.md](references/error-handling.md)** - Troubleshooting
- Common errors and solutions
- API error codes
- Configuration issues
- Network and timeout handling

**[database-schema.md](references/database-schema.md)** - Beam Nexus Skills database
- Property types and descriptions
- Available Teams and Integrations
- Field mapping table
- Example entries

### scripts/

**[check_notion_config.py](scripts/check_notion_config.py)** - Pre-flight validation
- Checks .env for required variables
- Tests API connection
- Validates user-config.yaml
- Returns actionable errors

**[setup_notion.py](scripts/setup_notion.py)** - Interactive setup wizard (to be created)
- Guides through API key setup
- Tests connection
- Saves configuration
- Gets user's Notion ID

---

## How Skills Reference This

Each skill loads shared resources **only when needed** (progressive disclosure):

**query-notion-db** uses:
- `../../notion-master/scripts/check_notion_config.py` (validate before query)
- `../../notion-master/references/api-reference.md` (query patterns)
- `../../notion-master/references/error-handling.md` (troubleshooting)

**import-skill-to-nexus** uses:
- `../../notion-master/scripts/check_notion_config.py` (validate before import)
- `../../notion-master/references/api-reference.md` (file download API)
- `../../notion-master/references/error-handling.md` (troubleshooting)

**export-skill-to-notion** uses:
- `../../notion-master/scripts/check_notion_config.py` (validate before export)
- `../../notion-master/references/api-reference.md` (file upload API)
- `../../notion-master/references/database-schema.md` (field mapping)
- `../../notion-master/references/error-handling.md` (troubleshooting)

---

## Usage Example

**User says:** "query notion for beam skills"

**What happens:**
1. AI loads `query-notion-db` skill (NOT notion-master)
2. `query-notion-db` SKILL.md says: "Run check_notion_config.py first"
3. AI executes: `python ../../notion-master/scripts/check_notion_config.py`
4. If errors occur, AI loads: `../../notion-master/references/error-handling.md`
5. AI executes query workflow from `query-notion-db` SKILL.md

**notion-master is NEVER loaded directly** - it's just a resource library.

---

**Version**: 1.0
**Created**: 2025-12-10
**Status**: Production Ready
