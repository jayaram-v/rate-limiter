from __future__ import annotations

from threading import Lock
from typing import Dict, Optional

from .models import RequestStatus, UserProfile


class InMemoryCache:
    def __init__(self) -> None:
        self._users: Dict[str, UserProfile] = {}
        self._request_status: Dict[str, RequestStatus] = {}
        self._lock = Lock()

    def set_user(self, user: UserProfile) -> None:
        with self._lock:
            self._users[user.user_id] = user

    def get_user(self, user_id: str) -> Optional[UserProfile]:
        with self._lock:
            return self._users.get(user_id)

    def record_status(self, key: str, status: RequestStatus) -> None:
        with self._lock:
            self._request_status[key] = status

    def get_status(self, key: str) -> Optional[RequestStatus]:
        with self._lock:
            return self._request_status.get(key)

    def clear(self) -> None:
        with self._lock:
            self._users.clear()
            self._request_status.clear()
