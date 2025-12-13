# Implementation Steps

## Phase 1: Setup Master Skill
- [x] Create `hubspot-master/` directory structure
- [x] Generate `hubspot_client.py` API client
- [x] Generate `check_hubspot_config.py` validator
- [x] Generate `setup_hubspot.py` wizard
- [x] Create `references/setup-guide.md`
- [x] Create `references/api-reference.md` (copy from project)
- [x] Create `references/error-handling.md` (copy from project)
- [x] Create `references/authentication.md` (copy from project)

## Phase 2: Setup Connect Skill
- [x] Create `hubspot-connect/` directory
- [x] Generate `SKILL.md` with routing table
- [x] Map trigger phrases to operations

## Phase 3: Create Contact Skills
- [x] Create `hubspot-list-contacts/` skill
- [x] Create `hubspot-create-contact/` skill
- [x] Create `hubspot-update-contact/` skill
- [x] Create `hubspot-search-contacts/` skill

## Phase 4: Create Company Skills
- [x] Create `hubspot-list-companies/` skill
- [x] Create `hubspot-create-company/` skill
- [x] Create `hubspot-search-companies/` skill

## Phase 5: Create Deal Skills
- [x] Create `hubspot-list-deals/` skill
- [x] Create `hubspot-create-deal/` skill
- [x] Create `hubspot-update-deal/` skill
- [x] Create `hubspot-search-deals/` skill

## Phase 6: Create Association Skill
- [x] Create `hubspot-get-associations/` skill

## Phase 7: Create Engagement Skills (Read)
- [x] Create `hubspot-list-emails/` skill
- [x] Create `hubspot-list-calls/` skill
- [x] Create `hubspot-list-notes/` skill
- [x] Create `hubspot-list-meetings/` skill

## Phase 8: Create Engagement Skills (Write)
- [x] Create `hubspot-log-email/` skill
- [x] Create `hubspot-log-call/` skill
- [x] Create `hubspot-create-note/` skill
- [x] Create `hubspot-create-meeting/` skill

## Phase 9: Test & Validate
- [x] Set up `HUBSPOT_ACCESS_TOKEN` environment variable
- [x] Run config check script
- [x] Test authentication flow
- [x] Test list contacts endpoint
- [x] Test create contact endpoint
- [x] Test search contacts endpoint
- [x] Test deals endpoints
- [x] Test engagement endpoints
- [x] Verify error handling

## Phase 10: Documentation & Registration
- [x] Update `hubspot-master/SKILL.md` with all skills
- [x] Add hubspot to configured_integrations
- [x] Document any HubSpot-specific quirks
- [x] Add usage examples to connect skill

## HubSpot-Specific Quirks (Documented)
- **Token format**: EU accounts use `pat-eu1-...`, US accounts use `pat-na1-...`
- **Scope changes**: When adding new scopes to Private App, the access token regenerates - must update .env
- **Search API**: Uses `CONTAINS_TOKEN` operator for partial name matches, not `CONTAINS`
- **Engagement URLs**: Emails/notes/meetings use filter-based URLs, not direct record URLs
- **Rate limits**: 100 requests/10 seconds, 500,000/day
