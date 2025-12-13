# HubSpot Error Handling

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| `200` | Success | Process response |
| `201` | Created | Record created successfully |
| `204` | No Content | Delete successful |
| `400` | Bad Request | Check request body/params |
| `401` | Unauthorized | Invalid/expired token |
| `403` | Forbidden | Missing scope |
| `404` | Not Found | Record doesn't exist |
| `409` | Conflict | Duplicate record |
| `429` | Rate Limited | Retry after delay |
| `500` | Server Error | Retry later |
| `502` | Bad Gateway | Retry later |
| `503` | Service Unavailable | Retry later |

---

## Error Response Format

```json
{
  "status": "error",
  "message": "Property values were not valid: [{\"isValid\":false,\"message\":\"Email is invalid\",\"error\":\"INVALID_EMAIL\",\"name\":\"email\"}]",
  "correlationId": "abc123-def456",
  "category": "VALIDATION_ERROR",
  "errors": [
    {
      "message": "Email is invalid",
      "error": "INVALID_EMAIL",
      "name": "email"
    }
  ]
}
```

---

## Common Errors

### Authentication Errors

**401 - Invalid Token**
```json
{
  "status": "error",
  "message": "Authentication credentials not found",
  "category": "INVALID_AUTHENTICATION"
}
```
**Fix:** Check `HUBSPOT_ACCESS_TOKEN` is set and valid.

**403 - Missing Scope**
```json
{
  "status": "error",
  "message": "This app hasn't been granted all required scopes to make this call",
  "category": "MISSING_SCOPES",
  "errors": [
    {"message": "crm.objects.contacts.write"}
  ]
}
```
**Fix:** Add missing scope to Private App settings.

---

### Validation Errors

**400 - Invalid Property**
```json
{
  "status": "error",
  "message": "Property values were not valid",
  "category": "VALIDATION_ERROR",
  "errors": [
    {"message": "Property 'bad_prop' does not exist", "name": "bad_prop"}
  ]
}
```
**Fix:** Use valid property names from schema.

**400 - Invalid Email**
```json
{
  "status": "error",
  "category": "VALIDATION_ERROR",
  "errors": [
    {"message": "Email is invalid", "error": "INVALID_EMAIL", "name": "email"}
  ]
}
```
**Fix:** Validate email format before sending.

---

### Conflict Errors

**409 - Duplicate Contact**
```json
{
  "status": "error",
  "message": "Contact already exists",
  "category": "CONFLICT",
  "errors": [
    {"message": "Contact already exists. Existing ID: 12345"}
  ]
}
```
**Fix:** Use search to find existing, then update instead.

---

### Not Found Errors

**404 - Record Not Found**
```json
{
  "status": "error",
  "message": "resource not found",
  "category": "OBJECT_NOT_FOUND"
}
```
**Fix:** Verify record ID exists.

---

## Error Handling Pattern

```python
import requests
import time
import logging

class HubSpotError(Exception):
    def __init__(self, status_code, message, category=None, errors=None):
        self.status_code = status_code
        self.message = message
        self.category = category
        self.errors = errors or []
        super().__init__(f"HubSpot API Error ({status_code}): {message}")

def hubspot_request(method, url, **kwargs):
    """Make HubSpot API request with error handling."""

    max_retries = 3

    for attempt in range(max_retries):
        response = requests.request(method, url, **kwargs)

        # Success
        if response.status_code in (200, 201, 204):
            return response.json() if response.content else None

        # Rate limited - retry with backoff
        if response.status_code == 429:
            wait = int(response.headers.get('Retry-After', 2 ** attempt))
            logging.warning(f"Rate limited, waiting {wait}s")
            time.sleep(wait)
            continue

        # Server error - retry
        if response.status_code >= 500:
            time.sleep(2 ** attempt)
            continue

        # Client error - don't retry
        error_data = response.json()
        raise HubSpotError(
            status_code=response.status_code,
            message=error_data.get('message', 'Unknown error'),
            category=error_data.get('category'),
            errors=error_data.get('errors', [])
        )

    raise HubSpotError(500, "Max retries exceeded")

# Usage
try:
    contact = hubspot_request('POST', f'{BASE_URL}/crm/v3/objects/contacts',
        headers=headers,
        json={"properties": {"email": "test@example.com"}}
    )
except HubSpotError as e:
    if e.category == 'CONFLICT':
        # Handle duplicate
        logging.info("Contact exists, updating instead")
    elif e.category == 'VALIDATION_ERROR':
        # Log validation details
        for error in e.errors:
            logging.error(f"Validation: {error['name']} - {error['message']}")
    else:
        raise
```

---

## Correlation ID

Every error includes a `correlationId`. Save this for debugging:

```python
except HubSpotError as e:
    logging.error(f"HubSpot error: {e.message}")
    logging.error(f"Correlation ID: {e.correlation_id}")  # For HubSpot support
```

---

## References

- [Error Responses](https://developers.hubspot.com/docs/api/error-handling)
- [Validation Errors](https://developers.hubspot.com/docs/api/crm/understanding-the-crm#validation)
