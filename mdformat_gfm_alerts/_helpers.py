"""General Helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from . import __plugin_name__

ContextOptions = Mapping[str, Any]


def get_conf(options: ContextOptions, key: str) -> bool | str | int | None:
    """Read setting from mdformat configuration context."""
    if (api := options["mdformat"].get(key)) is not None:
        return api
    return options["mdformat"].get("plugin", {}).get(__plugin_name__, {}).get(key)
