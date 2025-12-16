# Release Notes

## v0.10.0 - HubSpot Integration (2025-12-13)

### New Integration: HubSpot CRM

Complete HubSpot CRM integration following the master/connect/specialized pattern.

#### Features

**CRM Operations (12 endpoints)**
- **Contacts**: List, Create, Update, Search
- **Companies**: List, Create, Search
- **Deals**: List, Create, Update, Search
- **Associations**: Get linked records between objects

**Engagement Operations (8 endpoints)**
- **Emails**: List, Log
- **Calls**: List, Log
- **Notes**: List, Create
- **Meetings**: List, Create

#### Architecture

```
00-system/skills/hubspot/
├── hubspot-master/          # Shared resources
│   ├── scripts/             # 20 Python scripts
│   │   ├── hubspot_client.py
│   │   ├── check_hubspot_config.py
│   │   ├── list_contacts.py
│   │   ├── create_contact.py
│   │   └── ... (16 more)
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       ├── error-handling.md
│       └── authentication.md
└── hubspot-connect/         # User entry point
    └── SKILL.md             # Meta-skill with routing
```

#### Usage

Say any of these to trigger HubSpot operations:
- "hubspot" / "list contacts" / "show companies"
- "create contact john@example.com"
- "search deals enterprise"
- "list meetings" / "log call"

#### Setup

1. Create HubSpot Private App (Settings → Integrations → Private Apps)
2. Add required scopes (crm.objects.contacts.read/write, etc.)
3. Copy access token to `.env` as `HUBSPOT_ACCESS_TOKEN`

#### Technical Notes

- Token format: EU accounts use `pat-eu1-...`, US use `pat-na1-...`
- Rate limits: 100 requests/10 seconds, 500,000/day
- Scope changes regenerate access tokens

### Other Changes

- Added `hubspot` to integration auto-detection in nexus-loader.py
- Added `pending_onboarding` stats for proactive skill suggestions
- Minor updates to learning skills and orchestrator

---

## Previous Releases

### v0.9.0 (2025-12-11)
- Dynamic integrations menu
- Improved integration detection
- README updates
