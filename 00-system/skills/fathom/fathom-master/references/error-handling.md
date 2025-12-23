# Fathom API Error Handling

## Common HTTP Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Check request parameters, invalid query format |
| 401 | Unauthorized | API key invalid or missing - regenerate in Fathom Settings |
| 403 | Forbidden | API access not enabled on your Fathom plan |
| 404 | Not Found | Recording ID doesn't exist or is inaccessible |
| 429 | Rate Limited | Too many requests - wait and retry (automatic in client) |
| 500 | Server Error | Fathom service issue - retry after a moment |

## Error Response Format

```json
{
  "error": "error_type",
  "message": "Human readable description",
  "details": {}
}
```

## Troubleshooting Guide

### "FATHOM_API_KEY not found"

**Cause**: API key not configured in `.env` file

**Fix**:
1. Get your API key from Fathom Settings → API
2. Add to `.env`: `FATHOM_API_KEY=your-key-here`
3. Ensure no extra spaces or quotes around the key

### "401 Unauthorized"

**Cause**: Invalid API key

**Fix**:
1. Verify key in `.env` matches Fathom exactly
2. Check for accidental spaces or line breaks
3. Regenerate key in Fathom if needed

### "403 Forbidden"

**Cause**: API access not available on your plan

**Fix**:
1. Check Fathom subscription includes API access
2. Contact Fathom support if you believe this is an error

### "404 Not Found" for Transcripts

**Cause**: Recording ID doesn't exist or hasn't finished processing

**Fix**:
1. Use `list_meetings.py` to get valid recording IDs
2. Wait a few minutes if meeting just ended (processing time)
3. Verify the meeting was recorded (not just scheduled)

### "429 Rate Limited"

**Cause**: Too many requests in short time

**Fix**:
- The client handles this automatically with exponential backoff
- If persistent, reduce request frequency
- Default limit is approximately 100 requests/minute

### Connection Timeouts

**Cause**: Network issues or Fathom service slow

**Fix**:
- Client automatically retries 3 times
- Check internet connection
- Try again in a few minutes

## Best Practices

1. **Cache responses** - Meeting data doesn't change often
2. **Use filters** - Reduce data transfer with domain/date filters
3. **Batch requests** - Group multiple meeting fetches when possible
4. **Handle errors gracefully** - Check for empty results, missing fields
