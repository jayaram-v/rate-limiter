# Rate Limiter MVP

A minimal in-memory rate limiter with configurable limits, a local IP tracking model, and admin bypass support.

## Default configuration

- Local IP for rate limiting: `127.0.0.1`
- Default request limit: `3` requests per `60` seconds
- Admin bypass user: `admin-user`

See [config.yaml](config.yaml) and [project.yaml](project.yaml) for the default values.

## Quick Python usage

```python
from rate_limiter import RateLimitPolicy, RateLimitRequest, RateLimitService, RequestStatus

service = RateLimitService(RateLimitPolicy(max_requests=2, window_seconds=60, admin_users={"admin-user"}))
request = RateLimitRequest(
    user_id="user-42",
    ip="127.0.0.1",
    port=8000,
    endpoint="/resource",
    status=RequestStatus.REQUESTED,
)

print(service.allow_request(request))
print(service.allow_request(request))
print(service.allow_request(request))
```

## Running the API locally

```bash
uvicorn rate_limiter.api:app --host 127.0.0.1 --port 8000 --reload
```

## Manual validation

Follow the instructions in [rate_limiter/docs/manual_testing.md](rate_limiter/docs/manual_testing.md) for:
- rate limiting a standard local IP request
- validating admin bypass for `admin-user`
- checking cache-status tracking

## Running tests

```bash
python -m pytest -q
```
