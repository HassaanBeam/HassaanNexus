# HubSpot Rate Limits

## Overview

HubSpot enforces rate limits to ensure API stability and fair usage.

---

## Limits

### Burst Limit
- **100 requests per 10 seconds** per private app
- Applies to all endpoints combined

### Daily Limit
- **500,000 requests per day** per private app
- Resets at midnight UTC

---

## Response Headers

Monitor these headers in every response:

| Header | Description |
|--------|-------------|
| `X-HubSpot-RateLimit-Daily` | Daily quota limit |
| `X-HubSpot-RateLimit-Daily-Remaining` | Remaining daily requests |
| `X-HubSpot-RateLimit-Interval-Milliseconds` | Burst window (10000ms) |
| `X-HubSpot-RateLimit-Max` | Burst limit (100) |
| `X-HubSpot-RateLimit-Remaining` | Remaining burst requests |

---

## Rate Limit Exceeded

### HTTP 429 Response
```json
{
  "status": "error",
  "message": "You have reached your secondly limit.",
  "errorType": "RATE_LIMIT",
  "correlationId": "...",
  "policyName": "SECONDLY",
  "requestId": "..."
}
```

### Retry-After Header
When rate limited, check `Retry-After` header for seconds to wait.

---

## Best Practices

### 1. Use Batch Operations
Instead of individual requests, use batch endpoints:
```
POST /crm/v3/objects/contacts/batch/read
POST /crm/v3/objects/contacts/batch/create
POST /crm/v3/objects/contacts/batch/update
```
- Up to 100 records per batch
- Counts as 1 request against rate limit

### 2. Implement Exponential Backoff
```python
import time

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        response = func()
        if response.status_code == 429:
            wait = 2 ** attempt  # 1, 2, 4 seconds
            time.sleep(wait)
            continue
        return response
    raise Exception("Rate limit exceeded after retries")
```

### 3. Cache Responses
- Cache frequently accessed data
- Use `If-Modified-Since` for conditional requests
- Store property definitions (they rarely change)

### 4. Request Only Needed Properties
```
GET /crm/v3/objects/contacts?properties=email,firstname,lastname
```
Instead of fetching all properties.

### 5. Use Search Instead of List + Filter
```python
# BAD: Fetch all, filter locally
contacts = list_all_contacts()
filtered = [c for c in contacts if c['email'].endswith('@acme.com')]

# GOOD: Search on server
search_contacts(filters=[
    {"propertyName": "email", "operator": "CONTAINS_TOKEN", "value": "acme.com"}
])
```

---

## Monitoring

### Track Usage
```python
def log_rate_limits(response):
    daily_remaining = response.headers.get('X-HubSpot-RateLimit-Daily-Remaining')
    burst_remaining = response.headers.get('X-HubSpot-RateLimit-Remaining')

    if int(daily_remaining) < 10000:
        logger.warning(f"Daily limit low: {daily_remaining}")
    if int(burst_remaining) < 10:
        logger.warning(f"Burst limit low: {burst_remaining}")
```

---

## References

- [Usage Guidelines](https://developers.hubspot.com/docs/api/usage-details)
- [Rate Limits](https://developers.hubspot.com/docs/api/usage-details#rate-limits)
