"""Failure-safe third-party plugin registry and quarantine metadata."""
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
    min_host_version: str | None = None
    max_host_version: str | None = None

@dataclass(frozen=True)
class PluginHealth:
    name: str
    state: str
    path: str
    reason: str = ""

class PluginRegistry:
    def __init__(self,specs: Iterable[PluginSpec]=()):
        self._specs={s.name:s for s in specs}
        self._disabled:set[str]=set()

    def register(self,spec:PluginSpec,*,replace=False):
        if not spec.name: raise ValueError("Plugin name cannot be empty.")
        if spec.name in self._specs and not replace: raise KeyError(f"Plugin already registered: {spec.name}")
        self._specs[spec.name]=spec

    def disable(self,name,reason=""):
        if name not in self._specs: raise KeyError(name)
        self._disabled.add(name)

    def enable(self,name):
        self._disabled.discard(name)

    def health(self):
        result=[]
        for spec in self._specs.values():
            if spec.name in self._disabled:
                result.append(PluginHealth(spec.name,"disabled",str(spec.path),"Plugin is quarantined/disabled."))
                continue
            try:
                exists=spec.path.exists()
                state="available" if exists else "missing"
                reason="" if exists else "Plugin path does not exist."
            except OSError as exc:
                state,reason="error",f"{type(exc).__name__}: {exc}"
            result.append(PluginHealth(spec.name,state,str(spec.path),reason))
        return sorted(result,key=lambda x:x.name)

    def names(self): return sorted(self._specs)
