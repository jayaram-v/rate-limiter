from __future__ import annotations

from time import monotonic
from typing import Dict

from .cache import InMemoryCache
from .limiter import FixedWindowRateLimiter
from .models import RateLimitPolicy, RateLimitRequest, RequestStatus, UserProfile


class RateLimitService:
    def __init__(self, policy: RateLimitPolicy | None = None, cache: InMemoryCache | None = None) -> None:
        self.policy = policy or RateLimitPolicy()
        self.cache = cache or InMemoryCache()
        self._limiters: Dict[str, FixedWindowRateLimiter] = {}

        self._seed_default_user_data()

    def _seed_default_user_data(self) -> None:
        if self.cache.get_user("admin-user") is None:
            self.cache.set_user(
                UserProfile(
                    user_id="admin-user",
                    role="admin",
                    is_admin=True,
                    ip="127.0.0.1",
                    port=9000,
                )
            )

    def _get_limiter_for(self, request: RateLimitRequest) -> FixedWindowRateLimiter:
        key = request.request_key
        if key not in self._limiters:
            self._limiters[key] = FixedWindowRateLimiter(
                max_requests=self.policy.max_requests,
                window_seconds=self.policy.window_seconds,
            )
        return self._limiters[key]

    def _is_admin(self, request: RateLimitRequest) -> bool:
        profile = self.cache.get_user(request.user_id)
        if profile and profile.is_admin:
            return True
        return request.user_id in self.policy.admin_users

    def allow_request(self, request: RateLimitRequest) -> bool:
        if self._is_admin(request):
            self.cache.record_status(request.request_key, RequestStatus.ALLOWED)
            return True

        limiter = self._get_limiter_for(request)
        now = request.request_time if request.request_time is not None else monotonic()
        allowed = limiter.acquire(now)
        self.cache.record_status(request.request_key, RequestStatus.ALLOWED if allowed else RequestStatus.DENIED)
        return allowed

    def get_remaining(self, request: RateLimitRequest) -> int:
        if self._is_admin(request):
            return self.policy.max_requests

        limiter = self._get_limiter_for(request)
        now = request.request_time if request.request_time is not None else monotonic()
        return limiter.remaining(now)
