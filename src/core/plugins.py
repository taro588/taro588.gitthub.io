"""Failure-safe third-party plugin registry.

Plugins are capabilities, never core dependencies. This module only records
metadata and validates local paths; it does not import or execute plugins.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True)
class PluginSpec:
    name: str
    path: Path
    host: str = "shared"
    optional: bool = True

@dataclass(frozen=True)
class PluginHealth:
    name: str
    state: str
    path: str
    reason: str = ""

class PluginRegistry:
    def __init__(self, specs: Iterable[PluginSpec] = ()) -> None:
        self._specs = {spec.name: spec for spec in specs}

    def register(self, spec: PluginSpec, *, replace: bool = False) -> None:
        if not spec.name:
            raise ValueError("Plugin name cannot be empty.")
        if spec.name in self._specs and not replace:
            raise KeyError(f"Plugin already registered: {spec.name}")
        self._specs[spec.name] = spec

    def health(self) -> list[PluginHealth]:
        result = []
        for spec in self._specs.values():
            try:
                exists = spec.path.exists()
                state = "available" if exists else "missing"
                reason = "" if exists else "Plugin path does not exist."
            except OSError as exc:
                state, reason = "error", f"{type(exc).__name__}: {exc}"
            result.append(PluginHealth(spec.name, state, str(spec.path), reason))
        return sorted(result, key=lambda item: item.name)

    def names(self) -> list[str]:
        return sorted(self._specs)
