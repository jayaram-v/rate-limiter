from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import RateLimitPolicy


def load_policy_from_yaml(path: str | Path | None = None) -> RateLimitPolicy:
    config_path = Path(path) if path else Path(__file__).resolve().parent.parent / "config.yaml"
    with config_path.open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = yaml.safe_load(handle) or {}

    rate_config = data.get("rate_limit", {})
    admin_users = set(rate_config.get("admin_users", []))

    return RateLimitPolicy(
        max_requests=int(rate_config.get("max_requests", 3)),
        window_seconds=float(rate_config.get("window_seconds", 60)),
        admin_users=admin_users,
        local_ip=str(rate_config.get("local_ip", "127.0.0.1")),
    )
