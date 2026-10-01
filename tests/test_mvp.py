import unittest

from rate_limiter import (
    FixedWindowRateLimiter,
    InMemoryCache,
    RateLimitPolicy,
    RateLimitRequest,
    RateLimitService,
    RequestStatus,
    UserProfile,
)


class RateLimitMVPTTests(unittest.TestCase):
    def test_fixed_window_limiter_enforces_limit(self):
        limiter = FixedWindowRateLimiter(max_requests=2, window_seconds=60)

        self.assertTrue(limiter.acquire(100.0))
        self.assertTrue(limiter.acquire(101.0))
        self.assertFalse(limiter.acquire(102.0))

    def test_rate_limit_service_blocks_local_ip_when_limit_is_reached(self):
        service = RateLimitService(
            RateLimitPolicy(max_requests=2, window_seconds=60, admin_users={"admin-user"})
        )

        request = RateLimitRequest(
            user_id="user-42",
            ip="127.0.0.1",
            port=8000,
            endpoint="/resource",
            status=RequestStatus.REQUESTED,
        )

        self.assertTrue(service.allow_request(request))
        self.assertTrue(service.allow_request(request))
        self.assertFalse(service.allow_request(request))

    def test_admin_user_bypasses_rate_limit(self):
        service = RateLimitService(
            RateLimitPolicy(max_requests=1, window_seconds=60, admin_users={"admin-user"})
        )
        service.cache.set_user(
            UserProfile(
                user_id="admin-user",
                role="admin",
                is_admin=True,
                ip="127.0.0.1",
                port=9000,
            )
        )

        admin_request = RateLimitRequest(
            user_id="admin-user",
            ip="127.0.0.1",
            port=9000,
            endpoint="/admin",
            status=RequestStatus.REQUESTED,
        )

        self.assertTrue(service.allow_request(admin_request))
        self.assertTrue(service.allow_request(admin_request))
        self.assertTrue(service.allow_request(admin_request))

    def test_cache_stores_user_profile(self):
        cache = InMemoryCache()
        user = UserProfile(
            user_id="user-1",
            role="standard",
            is_admin=False,
            ip="127.0.0.1",
            port=5000,
        )

        cache.set_user(user)
        self.assertEqual(cache.get_user("user-1"), user)


if __name__ == "__main__":
    unittest.main()
