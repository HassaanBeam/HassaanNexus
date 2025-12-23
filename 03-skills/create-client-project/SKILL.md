---
name: create-client-project
description: Create a new client project folder with complete structure and templates. Load when user says "create client project", "new client", "add client [name]", "onboard new client", "setup client folder", or "create project for [client]". Creates folder structure with documentation templates based on provided information.
---

# Create Client Project

Create a new client project folder with complete structure.

## Workflow

### Step 1: Gather Information

**Required**:
- Client name

**Optional** (improves templates):
- GTM documentation / scope
- Primary contact info
- Project description
- Email domain (for Fathom filtering)

```
What's the client name?
> Acme Corporation

Do you have any documentation to include? (paste, file path, or 'skip')
```

### Step 2: Normalize Name

Convert to folder-safe format:
- Lowercase
- Replace spaces with hyphens
- Remove special characters

`"Acme Corporation"` → `acme-corporation`

### Step 3: Create Structure

**Base Location**: User specifies or use default project location

```
[location]/[client-name]/
├── PROJECT_CONTEXT.md         # Chronological update log
├── project-state.json         # Structured state data
├── README.md                  # Project overview
│
├── docs/
│   ├── SCOPE_OF_WORK.md       # Deliverables & timeline
│   ├── SOLUTION_WORKFLOW.md   # Operational procedures
│   ├── TECHNICAL_ARCHITECTURE.md  # System design
│   ├── LINEAR_TICKETS.md      # Ticket tracking
│   └── SLACK_CHANNELS_SETUP.md    # Communication
│
├── meetings/
│   └── transcripts/           # Raw transcripts
│
├── communications/            # Sent messages
│
└── weekly-updates/            # Status reports
```

### Step 4: Populate Templates

**PROJECT_CONTEXT.md**:
```markdown
# [Client Name] Project Context

> Quick-reference log of project changes. Newest at top.

---

## [Today's Date]

**Project Created**
- Initial setup and folder structure

**Links:**
- [Scope of Work](docs/SCOPE_OF_WORK.md)
```

**project-state.json**:
```json
{
  "lastUpdated": "[timestamp]",
  "clientName": "[Client Name]",
  "currentPhase": "DISCOVERY",
  "recentActivity": [{
    "date": "[today]",
    "type": "onboarding",
    "summary": "Project created"
  }],
  "nextSteps": [
    "Complete kickoff meeting",
    "Define scope of work",
    "Set up communication channels"
  ],
  "openIssues": [],
  "blockers": [],
  "team": { "internal": [], "client": [] }
}
```

**README.md**:
```markdown
# [Client Name]

## Overview
[Description from GTM docs or placeholder]

## Quick Links
- [Scope of Work](docs/SCOPE_OF_WORK.md)
- [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)
- Linear Project: TBD
- Slack Channel: TBD

## Team
**Internal**: TBD
**Client**: [Contact info if provided]

## Status
- **Phase**: Discovery
- **Created**: [Date]
```

### Step 5: Extract from GTM Docs

If documentation provided, extract:
- Scope → `SCOPE_OF_WORK.md`
- Contacts → `README.md`
- Requirements → `TECHNICAL_ARCHITECTURE.md`
- Timeline → `SCOPE_OF_WORK.md`

### Step 6: Report Success

```
✅ Client project created: [Client Name]

📁 Location: [path]

📝 Files Created:
- PROJECT_CONTEXT.md
- project-state.json
- README.md
- docs/SCOPE_OF_WORK.md
- docs/SOLUTION_WORKFLOW.md
- docs/TECHNICAL_ARCHITECTURE.md
- docs/LINEAR_TICKETS.md
- docs/SLACK_CHANNELS_SETUP.md

📋 Next Steps:
1. Review and complete SCOPE_OF_WORK.md
2. Create Linear project
3. Set up Slack channels
4. Schedule kickoff meeting
```

---

## Template Files

Templates in `templates/` subdirectory can be customized.

---

## Related Skills

- `process-client-meeting` - Use after kickoff
- `update-project-context` - Keep context current
- `create-weekly-update` - Start weekly reporting
