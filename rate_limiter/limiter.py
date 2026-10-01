from collections import deque
from time import monotonic


class FixedWindowRateLimiter:
    """Simple fixed-window limiter.

    Allows up to ``max_requests`` requests within a rolling ``window_seconds``
    interval.
    """

    def __init__(self, max_requests: int, window_seconds: float):
        if max_requests <= 0:
            raise ValueError("max_requests must be greater than 0")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than 0")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps = deque()

    def acquire(self, now: float | None = None) -> bool:
        timestamp = monotonic() if now is None else now
        cutoff = timestamp - self.window_seconds

        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

        if len(self._timestamps) >= self.max_requests:
            return False

        self._timestamps.append(timestamp)
        return True

    def allow(self, now: float | None = None) -> bool:
        return self.acquire(now)

    def remaining(self, now: float | None = None) -> int:
        timestamp = monotonic() if now is None else now
        cutoff = timestamp - self.window_seconds

        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

        return max(self.max_requests - len(self._timestamps), 0)

    def reset(self) -> None:
        self._timestamps.clear()
