# Auth Token Expiry

Auth tokens (JWTs) expire because the server sets a TTL (time-to-live) on issue.
The default in this system is 30 minutes. After expiry the server rejects the token
with a 401 Unauthorized response.

## Why this happens

The short TTL is intentional — it limits the damage window if a token is stolen.
A stolen token becomes useless after 30 minutes without the refresh token.

## How to fix

1. **Implement token refresh**: Before the access token expires, call the
   `/auth/refresh` endpoint with the refresh token to get a new access token.

2. **Handle 401 responses globally**: In your HTTP client, intercept 401 responses,
   attempt a token refresh, then retry the original request automatically.

3. **Store tokens correctly**: Keep the access token in memory (not localStorage).
   Store the refresh token in an httpOnly cookie to prevent XSS access.

## Example refresh flow

```
Access token expires → API returns 401
→ Client calls POST /auth/refresh with refresh token cookie
→ Server returns new access token
→ Client retries original request with new token
```

If the refresh token is also expired the user must log in again.
