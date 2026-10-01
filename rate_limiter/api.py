from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .config import load_policy_from_yaml
from .models import RateLimitRequest, RequestStatus
from .service import RateLimitService


class RateLimitCheckRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    ip: str = Field(default="127.0.0.1", description="Client IP address")
    port: int = Field(default=8000, ge=1, le=65535)
    endpoint: str = Field(default="/resource", description="Target endpoint")
    status: RequestStatus = RequestStatus.REQUESTED


class RateLimitCheckResponse(BaseModel):
    allowed: bool
    status: Literal["allowed", "denied"]
    remaining: int
    key: str
    local_ip: str


service = RateLimitService(policy=load_policy_from_yaml())
app = FastAPI(title="Rate Limiter MVP")


@app.post("/rate-limit/check", response_model=RateLimitCheckResponse)
def check_rate_limit(payload: RateLimitCheckRequest) -> RateLimitCheckResponse:
    request = RateLimitRequest(
        user_id=payload.user_id,
        ip=payload.ip,
        port=payload.port,
        endpoint=payload.endpoint,
        status=payload.status,
    )
    allowed = service.allow_request(request)

    return RateLimitCheckResponse(
        allowed=allowed,
        status="allowed" if allowed else "denied",
        remaining=service.get_remaining(request),
        key=request.request_key,
        local_ip=service.policy.local_ip,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
