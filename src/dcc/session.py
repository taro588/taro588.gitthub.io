"""Safe DCC session wrapper.

A failed DCC connection must never prevent the Toolkit process from starting.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import DCCAdapter


@dataclass
class DCCSession:
    adapter: DCCAdapter
    connected: bool = False
    last_error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def connect(self) -> bool:
        try:
            self.connected = bool(self.adapter.is_available())
            self.last_error = None if self.connected else "DCC API is not available"
        except Exception as exc:
            self.connected = False
            self.last_error = str(exc)
        return self.connected

    def info(self) -> dict[str, Any]:
        result = self.adapter.status()
        result.update({"connected": self.connected, "error": self.last_error})
        if self.connected:
            try:
                result["scene"] = self.adapter.scene_info()
            except Exception as exc:
                result["scene_error"] = str(exc)
        return result
