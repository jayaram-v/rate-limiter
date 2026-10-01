# Manual testing guide

This MVP is configured to use the local IP `127.0.0.1` for request tracking and admin-bypass validation.

## Default local test configuration

- local IP: `127.0.0.1`
- default endpoint: `/resource`
- default limit: `3` requests within `60` seconds
- admin user: `admin-user`
- admin port: `9000`

## Test 1: standard user is rate limited

1. Start the API:
   ```bash
   uvicorn rate_limiter.api:app --host 127.0.0.1 --port 8000 --reload
   ```
2. Send requests from the local IP using a normal user:
   ```bash
   curl -X POST "http://127.0.0.1:8000/rate-limit/check" \
     -H "Content-Type: application/json" \
     -d '{"user_id":"user-42","ip":"127.0.0.1","port":8000,"endpoint":"/resource"}'
   ```
3. Repeat the same request at least 3 times in quick succession.
4. Confirm that the third request is denied and the response contains `"allowed": false`.

## Test 2: admin bypass works

1. Use the admin user payload:
   ```bash
   curl -X POST "http://127.0.0.1:8000/rate-limit/check" \
     -H "Content-Type: application/json" \
     -d '{"user_id":"admin-user","ip":"127.0.0.1","port":9000,"endpoint":"/admin"}'
   ```
2. Repeat the same request multiple times.
3. Confirm that all requests are allowed because `admin-user` is configured as an admin bypass user.

## Test 3: cache and status tracking

1. Check the in-memory cache by using the API request repeatedly.
2. Confirm that the service records `requested`, `allowed`, or `denied` states for each request key.
3. Verify that the same local IP and endpoint combination is tracked as one rate-limited key.

## Expected outcomes

- Normal local IP request sequence: allow, allow, deny
- Admin user sequence: always allow
- Request statuses should be stored and readable from the in-memory cache
