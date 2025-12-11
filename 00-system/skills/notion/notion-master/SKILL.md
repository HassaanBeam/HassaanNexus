---
name: notion-master
description: Shared resource library for Notion integration skills. DO NOT load directly - this provides common references (setup, API docs, error handling, database schema) and scripts used by notion-connect, query-notion-db, import-skill-to-nexus, and export-skill-to-notion.
---

# Notion Master

**This is NOT a user-facing skill.** It's a shared resource library referenced by Notion integration skills.

## Purpose

Provides shared resources to eliminate duplication across:
- `notion-connect` - Meta-skill for complete Notion workspace integration (NEW)
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

**[filter-syntax.md](references/filter-syntax.md)** - Query filter syntax
- Operators by property type
- Common filter patterns
- Sorting options

**[property-types.md](references/property-types.md)** - Property type reference
- All 20+ property types
- Read and write formats
- Validation rules

**[block-types.md](references/block-types.md)** - Block type reference
- All 50+ block types
- Block schemas and examples
- Rich text formatting

### scripts/

**[check_notion_config.py](scripts/check_notion_config.py)** - Pre-flight validation
- Checks .env for required variables
- Tests API connection
- Validates user-config.yaml
- Returns actionable errors
- **Supports `--json` flag** for structured AI-consumable output

**[discover_databases.py](scripts/discover_databases.py)** - Database discovery
- Finds all accessible databases
- Extracts property schemas
- Saves to context file

**[search_skill_database.py](scripts/search_skill_database.py)** - Unified database querying
- General mode: `--db "Database Name"` with fuzzy matching
- Skills mode: `--skills` preset for Beam Nexus Skills (supports AND filters)
- Filter parsing with multiple operators
- Formatted or JSON output

**[create_page.py](scripts/create_page.py)** - Page creation
- Property validation
- Schema-aware input
- Interactive mode

**[manage_page.py](scripts/manage_page.py)** - Page management
- Get, update, delete pages
- Property type handling

**[manage_database.py](scripts/manage_database.py)** - Database management
- Create databases
- Update schemas

**[manage_blocks.py](scripts/manage_blocks.py)** - Block operations
- List, append, update, delete blocks
- Simple block builder

**[manage_users.py](scripts/manage_users.py)** - User management
- List workspace users
- Get user details
- Save for @mentions

**[manage_comments.py](scripts/manage_comments.py)** - Comment operations
- List and create comments
- Reply to discussions
- Note: Requires "Insert comments" capability in integration settings

**[rate_limiter.py](scripts/rate_limiter.py)** - Rate limit handling
- Exponential backoff with jitter
- Respects Retry-After header
- Automatic retry on 429/5xx errors
- Usage: `from rate_limiter import make_request_with_retry`

**[setup_notion.py](scripts/setup_notion.py)** - Interactive setup wizard
- Guides through API key setup
- Tests connection
- Saves configuration to `.env`
- Gets user's Notion ID
- Auto-runs database discovery

---

## Intelligent Error Detection Flow

When a Notion skill fails due to missing configuration, the AI should:

### Step 1: Run Config Check with JSON Output

```bash
python 00-system/skills/notion/notion-master/scripts/check_notion_config.py --json
```

### Step 2: Parse the `ai_action` Field

The JSON output includes an `ai_action` field that tells the AI what to do:

| ai_action | What to Do |
|-----------|------------|
| `proceed_with_operation` | Config OK, continue with the original operation |
| `proceed_with_warning` | Partial config (can query/import but not export) |
| `prompt_for_api_key` | Ask user: "I need your Notion API key. Get one at https://www.notion.so/my-integrations" |
| `create_env_file` | Create `.env` file and ask user for API key |
| `run_setup_wizard` | Run: `python 00-system/skills/notion/notion-master/scripts/setup_notion.py` |

### Step 3: Help User Fix Issues

If `ai_action` is `prompt_for_api_key`:

1. Tell user: "Notion integration needs setup. I need your API key."
2. Show them: "Get one at: https://www.notion.so/my-integrations"
3. Ask: "Paste your Notion API key here:"
4. Once they provide it, **write directly to `.env`**:
   ```
   # Edit .env file to add:
   NOTION_API_KEY=secret_their_key_here
   NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e
   ```
5. Re-run config check to verify

### JSON Output Structure

```json
{
  "status": "not_configured",
  "exit_code": 2,
  "ai_action": "prompt_for_api_key",
  "missing": [
    {"item": "NOTION_API_KEY", "required": true, "location": ".env"}
  ],
  "fix_instructions": [...],
  "env_template": "NOTION_API_KEY=secret_YOUR_API_KEY_HERE\nNOTION_SKILLS_DB_ID=...",
  "setup_wizard": "python 00-system/skills/notion/notion-master/scripts/setup_notion.py"
}
```

---

## How Skills Reference This

Each skill loads shared resources **only when needed** (progressive disclosure):

**notion-connect** uses:
- All discovery and query scripts
- All page, block, user, and comment management scripts
- All references (filter-syntax, property-types, block-types)

**query-notion-db** uses:
- `check_notion_config.py` (validate before query)
- `api-reference.md` (query patterns)
- `error-handling.md` (troubleshooting)

**import-skill-to-nexus** uses:
- `check_notion_config.py` (validate before import)
- `api-reference.md` (file download API)
- `error-handling.md` (troubleshooting)

**export-skill-to-notion** uses:
- `check_notion_config.py` (validate before export)
- `api-reference.md` (file upload API)
- `database-schema.md` (field mapping)
- `error-handling.md` (troubleshooting)

---

## Usage Example

**User says:** "query my Projects database"

**What happens:**
1. AI loads `notion-connect` skill (NOT notion-master)
2. `notion-connect` SKILL.md says: "Run check_notion_config.py first"
3. AI executes: `python notion-master/scripts/check_notion_config.py`
4. AI executes: `python notion-master/scripts/search_skill_database.py --db "Projects"`
5. If errors occur, AI loads: `notion-master/references/error-handling.md`

**notion-master is NEVER loaded directly** - it's just a resource library.

---

**Version**: 2.4
**Created**: 2025-12-10
**Updated**: 2025-12-11
**Status**: Production Ready

**Changelog**:
- v2.4: Added Intelligent Error Detection Flow with `--json` support for AI-guided setup
- v2.3: Renamed `query_database.py` to `search_skill_database.py` for clarity
