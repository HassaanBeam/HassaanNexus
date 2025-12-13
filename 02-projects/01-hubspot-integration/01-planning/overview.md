---
id: 01-hubspot-integration
name: HubSpot Integration
status: COMPLETE
description: Load when user mentions 'hubspot integration', 'implement hubspot', 'build hubspot skills'
created: 2025-12-13
updated: 2025-12-13
---

# HubSpot Integration

Build complete HubSpot integration following the master/connect/specialized pattern.

## Scope

- **Service**: HubSpot
- **Base URL**: https://api.hubapi.com
- **Auth Type**: Private App Access Token (Bearer)
- **Env Variable**: `HUBSPOT_ACCESS_TOKEN`
- **Endpoints**: 20 selected

## Selected Endpoints

### CRM (12 endpoints)
| Category | Operations |
|----------|------------|
| Contacts | List, Create, Update, Search |
| Companies | List, Create, Search |
| Deals | List, Create, Update, Search |
| Associations | Get |

### Engagements (8 endpoints)
| Type | Operations |
|------|------------|
| Emails | List, Log |
| Calls | List, Log |
| Notes | List, Create |
| Meetings | List, Create |

## Architecture

Will create:
- `hubspot-master/` - Shared resources & API client
- `hubspot-connect/` - Meta-skill entry point
- 20 operation skills (one per endpoint)

## API Documentation

Located in `02-resources/api-documentation/`:
- `authentication.md` - Private App setup
- `api-reference.md` - Endpoint reference
- `rate-limits.md` - 100/10sec, 500k/day
- `error-handling.md` - Error codes & handling

## References

- [HubSpot API Docs](https://developers.hubspot.com/docs/api-reference/overview)
- [Private Apps](https://developers.hubspot.com/docs/api/private-apps)
- Pattern: See 00-system/skills/system/add-integration/references/integration-architecture.md
