import unittest

from rate_limiter import FixedWindowRateLimiter


class FixedWindowRateLimiterTests(unittest.TestCase):
    def test_allows_requests_within_limit(self):
        limiter = FixedWindowRateLimiter(max_requests=3, window_seconds=10)

        self.assertTrue(limiter.acquire(100.0))
        self.assertTrue(limiter.acquire(101.0))
        self.assertTrue(limiter.acquire(102.0))

    def test_rejects_requests_over_limit(self):
        limiter = FixedWindowRateLimiter(max_requests=2, window_seconds=5)

        self.assertTrue(limiter.acquire(10.0))
        self.assertTrue(limiter.acquire(11.0))
        self.assertFalse(limiter.acquire(12.0))

    def test_expires_old_requests_after_window(self):
        limiter = FixedWindowRateLimiter(max_requests=2, window_seconds=5)

        self.assertTrue(limiter.acquire(0.0))
        self.assertTrue(limiter.acquire(1.0))
        self.assertFalse(limiter.acquire(2.0))
        self.assertTrue(limiter.acquire(6.0))


if __name__ == "__main__":
    unittest.main()
