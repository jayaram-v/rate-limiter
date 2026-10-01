from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RequestStatus(str, Enum):
    REQUESTED = "requested"
    ALLOWED = "allowed"
    DENIED = "denied"


@dataclass(frozen=True)
class UserProfile:
    user_id: str
    role: str
    is_admin: bool = False
    ip: str = "127.0.0.1"
    port: int = 8000


@dataclass(frozen=True)
class RateLimitPolicy:
    max_requests: int = 3
    window_seconds: float = 60.0
    admin_users: set[str] = field(default_factory=set)
    local_ip: str = "127.0.0.1"

    def __post_init__(self) -> None:
        if self.max_requests <= 0:
            raise ValueError("max_requests must be greater than 0")
        if self.window_seconds <= 0:
            raise ValueError("window_seconds must be greater than 0")


@dataclass(frozen=True)
class RateLimitRequest:
    user_id: str
    ip: str
    port: int
    endpoint: str
    status: RequestStatus = RequestStatus.REQUESTED
    request_time: float | None = None

    @property
    def request_key(self) -> str:
        return f"{self.ip}:{self.port}:{self.endpoint}"
