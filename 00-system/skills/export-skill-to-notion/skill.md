---
name: export-skill-to-notion
description: Push a local skill to the Notion skills database. Load when user mentions "export skill", "push to notion", "share skill", "add skill to database", or after creating a new skill with create-skill.
---

# Export Skill to Notion

Push a local skill's metadata and file to the Beam Nexus Skills database in Notion.

## Purpose

This skill takes a local skill from `03-skills/` and creates a new entry in the company's Notion skills database. It handles:

- Reading SKILL.md to extract metadata
- **Automatically uploading the SKILL.md file** via Notion File Upload API
- Mapping fields to Notion properties
- **MANDATORY user confirmation before pushing**
- Setting Owner from user-config.yaml
- Inferring appropriate Team (or creating new one)
- Creating the database entry with file attachment

**Typically used after `create-skill`** to share new skills with the company.

---

## CRITICAL RULES

1. **ALWAYS confirm with user before pushing** - Never auto-push
2. **ALWAYS set Owner** - Use notion_user_id from user-config.yaml
3. **ALWAYS upload the skill file** - Use Notion File Upload API (see Step 5)
4. **INFER appropriate Team** - Don't default to Solutions. Think about scope:
   - "General" for company-wide utility skills
   - "Solutions" for client-facing/implementation skills
   - "Engineering" for dev tools
   - Create new team if needed
5. **ALWAYS check for duplicates first** - Prevent accidental overwrites
6. **NEVER delete skills from Notion** - Deletion must be done manually in Notion UI
7. **Collaborative editing allowed** - Can update others' skills (builds shared knowledge)

---

## Safeguards

### Pre-Flight Check (ALWAYS Run First)

Before ANY export operation, verify Notion setup:

```bash
python ../../notion-master/scripts/check_notion_config.py
```

**If configuration missing:**
- Option A: Run setup wizard: `python ../../notion-master/scripts/setup_notion.py`
- Option B: See [../../notion-master/references/setup-guide.md](../../notion-master/references/setup-guide.md)

**Expected output if configured:**
```
✅ ALL CHECKS PASSED
You're ready to use Notion skills
```

### Smart Duplicate Detection

**3-tier check before pushing:**

1. **Name match** → Query Notion for exact skill name
2. **If name exists** → Compare descriptions
3. **If both match** → Compare file content

```
Duplicate detected: "{skill-name}"

Options:
1. Update existing (if you own it)
2. Cancel
3. Create with different name

⚠️ Cannot create duplicate with same name.
```

### Collaborative Updates

Skills can be updated by anyone (collaborative knowledge building):
```
Updating existing skill...
Owner: {owner-name}

Note: You're updating a skill owned by {owner-name}.
This is allowed for collaborative improvement.

Proceed with update? (yes/no)
```

### Prohibited Operations

| Operation | Status | Notes |
|-----------|--------|-------|
| Create new skill | ✅ Allowed | With confirmation |
| Update own skill | ✅ Allowed | Standard flow |
| Update others' skill | ✅ Allowed | Collaborative editing |
| Delete any skill | ❌ Blocked | Must use Notion UI |
| Bulk push | ❌ Blocked | One at a time only |


---

## Workflow

### Step 1: Read Local Skill

```bash
# Get skill metadata from SKILL.md
cat 03-skills/{skill-name}/SKILL.md
```

**Extract from YAML header:**
- `name` → Skill Name
- `description` → Description

**Extract from content:**
- Purpose section → Purpose field

### Step 2: Prepare Skill File for Upload

```bash
# Copy SKILL.md to .txt format (Notion doesn't support .md or .zip uploads)
cp 03-skills/{skill-name}/SKILL.md /tmp/{skill-name}-SKILL.txt
```

**Note**: Notion File Upload API only supports these formats: `.txt`, `.json`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, plus images/audio/video. We use `.txt` for maximum compatibility.

### Step 3: Infer Team and Gather Info

**AI should infer the Team based on skill purpose:**
- **General**: Utility skills usable by anyone (query tools, import/export, etc.)
- **Solutions**: Client implementation, onboarding, customer-facing
- **Engineering**: Developer tools, CI/CD, testing
- **Sales**: Sales-specific workflows
- **Other**: Ask user if unclear

**Present inference to user for confirmation:**
```
Based on the skill's purpose, I suggest Team: "General"
(This is a utility skill for querying Notion databases)

Is this correct, or would you prefer a different team?
```

### Step 4: Preview Before Push (MANDATORY)

```
📤 Ready to push skill to Notion:

Skill Name:    {skill-name}
Description:   {description}
Purpose:       {purpose}
Team:          {inferred-team}
Integration:   {integrations}
Owner:         {name from user-config.yaml}
Skill File:    {skill-name}.zip ({size} bytes)
Created:       {today's date}

Do you want to push this to Notion? (yes/no/edit)
```

**WAIT FOR USER CONFIRMATION BEFORE PROCEEDING**

### Step 5: Create Notion Entry with File

**Use the upload script:**
```bash
python ../../notion-master/scripts/upload_skill.py 03-skills/{skill-name} --team General
```

**Optional parameters:**
```bash
# With integrations
python ../../notion-master/scripts/upload_skill.py 03-skills/my-skill --team General --integration "Beam AI,Linear"

# With custom file
python ../../notion-master/scripts/upload_skill.py 03-skills/my-skill --team General --file /path/to/custom.txt
```

**Manual upload (if needed):**

See [../../notion-master/references/api-reference.md](../../notion-master/references/api-reference.md) for the 3-step file upload API process.

**The script handles:**
1. Reading SKILL.md metadata
2. Creating file upload object
3. Uploading file content
4. Creating database entry with attachment

### Step 6: Confirm Success

```
✅ Skill pushed to Notion!

📄 Skill Name: {skill-name}
🔗 Notion URL: {url}
👥 Owner: {owner-name}
📁 Team: {team}
📎 File: {skill-name}-SKILL.txt (auto-attached)

The skill is now discoverable by anyone at Beam AI.
```

---

## Field Mapping

**See complete database schema:**
- [../../notion-master/references/database-schema.md](../../notion-master/references/database-schema.md)

**Quick reference:**

| Local (SKILL.md) | Notion Property | Type | Required | Notes |
|------------------|-----------------|------|----------|-------|
| `name:` in YAML | Skill Name | title | Yes | |
| `description:` in YAML | Description | rich_text | Yes | |
| Purpose section | Purpose | rich_text | No | Extract from ## Purpose |
| AI infers + user confirms | Team | select | Yes | Create if doesn't exist |
| AI infers from content | Integration | multi_select | No | Beam AI, Linear, Notion, etc. |
| user-config.yaml | Owner | people | Yes | notion_user_id |
| Today's date | Created | date | Yes | Auto-set |
| SKILL.md as .txt | Skill | files | Yes | Auto-uploaded via File Upload API |

---

## Configuration

**From `.env`:**
- `NOTION_API_KEY` - Your Notion integration token
- `NOTION_SKILLS_DB_ID` - Database ID: `2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e`

**From `user-config.yaml`:**
- `notion_user_id` - Your Notion user ID for Owner field
- `notion_user_name` - Display name

**Available Teams** (can create new):
- General (for utility/company-wide skills)
- Solutions (for client-facing skills)
- Engineering (for dev tools)
- Sales (for sales workflows)

**Available Integrations:**
- Beam AI
- Linear
- Notion

---

## Team Inference Rules

| Skill Type | Suggested Team | Reasoning |
|------------|----------------|-----------|
| Query/import/export tools | General | Used by everyone |
| Notion/Linear integrations | General | Cross-functional |
| Client onboarding | Solutions | Client-facing |
| Agent building/testing | Solutions | Implementation work |
| CI/CD, testing tools | Engineering | Dev-focused |
| Proposal generators | Sales | Sales-specific |
| Unknown | Ask user | When unclear |

---

## Example Usage

### Export a General Utility Skill

```
User: "Push query-notion-db to Notion"

AI: [Reads 03-skills/query-notion-db/SKILL.md]
    [Zips the folder]

    Based on the skill's purpose (querying Notion databases for any use),
    I suggest Team: "General"

    This is a utility skill that anyone at Beam AI could use.
    Is this correct? (yes/no/specify different)

User: "yes"

AI: 📤 Ready to push skill to Notion:

    Skill Name:    query-notion-db
    Description:   Query any Notion database and return results...
    Purpose:       Query any Notion database using the API...
    Team:          General
    Integration:   Notion
    Owner:         Fredrik Falk
    Skill File:    query-notion-db.zip (4.2 KB)
    Created:       2025-12-09

    Do you want to push this to Notion? (yes/no/edit)

User: "yes"

AI: ✅ Skill pushed to Notion!
    📄 Skill Name: query-notion-db
    🔗 https://notion.so/query-notion-db-abc123
    👥 Owner: Fredrik Falk
    📁 Team: General
    📎 File: query-notion-db-SKILL.txt (auto-attached)
```

---

## Error Handling

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check NOTION_API_KEY in .env |
| 400 Bad Request | Invalid property format | Check field mapping |
| Skill already exists | Duplicate in Notion | Ask: Update or skip? |
| Missing notion_user_id | Not in user-config.yaml | Prompt to add it |
| Missing SKILL.md | Invalid skill path | Verify path |

**For detailed troubleshooting:**
- See [../../notion-master/references/error-handling.md](../../notion-master/references/error-handling.md)

### Check for Duplicates FIRST

Before any push, use the query script to check if skill exists:
```bash
python ../../notion-master/scripts/query_db.py --name {skill-name}
```

---

## Notes

- **File upload**: Uses Notion's File Upload API (3-step process: create upload object → send file → attach to page). Supported formats: `.txt`, `.json`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, images, audio, video. We use `.txt` for SKILL.md files.
- **New teams auto-create**: If you specify a team that doesn't exist, Notion will create it automatically.
- **Owner is mandatory**: Always set from user-config.yaml to maintain audit trail.
- **Always confirm**: Never push without explicit user approval.

---

## Additional References

**For more details:**
- [../../notion-master/references/setup-guide.md](../../notion-master/references/setup-guide.md) - Initial setup
- [../../notion-master/references/api-reference.md](../../notion-master/references/api-reference.md) - File upload API
- [../../notion-master/references/database-schema.md](../../notion-master/references/database-schema.md) - Complete schema
- [../../notion-master/references/error-handling.md](../../notion-master/references/error-handling.md) - Troubleshooting
