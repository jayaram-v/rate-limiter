import json

from fastapi.testclient import TestClient

from rate_limiter.api import app


client = TestClient(app)

payload = {
    "user_id": "user-42",
    "ip": "127.0.0.1",
    "port": 8000,
    "endpoint": "/resource",
}

admin_payload = {
    "user_id": "admin-user",
    "ip": "127.0.0.1",
    "port": 9000,
    "endpoint": "/admin",
}

for i in range(1, 4):
    response = client.post("/rate-limit/check", json=payload)
    print(f"user request {i}: {response.status_code} {response.json()}")

for i in range(1, 4):
    response = client.post("/rate-limit/check", json=admin_payload)
    print(f"admin request {i}: {response.status_code} {response.json()}")
