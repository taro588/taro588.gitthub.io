"""Safe, transactional Toolkit lifecycle operations."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json, shutil, tempfile, time

@dataclass(frozen=True)
class InstallResult:
    ok: bool
    action: str
    root: str
    error: str | None = None
    version: str | None = None

class ToolkitInstaller:
    def __init__(self, root: str | Path):
        self.root=Path(root).expanduser().resolve()
        self.current=self.root/"current"; self.versions=self.root/"versions"; self.backups=self.root/"backups"
        self.state=self.root/"state.json"

    def _owned(self,path):
        target=Path(path).expanduser().resolve()
        try: target.relative_to(self.root)
        except ValueError as exc: raise ValueError("Refusing to operate outside Toolkit root.") from exc
        return target

    def _write_state(self, version: str | None):
        self.root.mkdir(parents=True,exist_ok=True)
        self.state.write_text(json.dumps({"current":version},ensure_ascii=False,indent=2),encoding="utf-8")

    def install(self):
        try:
            for d in (self.current,self.versions,self.backups): d.mkdir(parents=True,exist_ok=True)
            return InstallResult(True,"install",str(self.root))
        except Exception as exc: return InstallResult(False,"install",str(self.root),f"{type(exc).__name__}: {exc}")

    def repair(self):
        result=self.install()
        return InstallResult(result.ok,"repair",result.root,result.error)

    def stage_update(self,source,version=None):
        try:
            source=Path(source).expanduser().resolve()
            if not source.is_dir(): raise ValueError("Update source directory does not exist.")
            try: source.relative_to(self.root); raise ValueError("Update source must not be inside the Toolkit root.")
            except ValueError as exc:
                if "inside the Toolkit root" in str(exc): raise
            self.install()
            version=version or time.strftime("%Y%m%d-%H%M%S")
            target=self.versions/version
            if target.exists(): raise ValueError(f"Version already exists: {version}")
            shutil.copytree(source,target)
            return InstallResult(True,"stage_update",str(self.root),version=version)
        except Exception as exc: return InstallResult(False,"stage_update",str(self.root),f"{type(exc).__name__}: {exc}")

    def activate(self,version):
        try:
            target=self._owned(self.versions/version)
            if not target.is_dir(): raise ValueError(f"Version does not exist: {version}")
            backup=self.backups/(time.strftime("%Y%m%d-%H%M%S") + "-previous")
            if self.current.exists(): shutil.move(str(self.current),str(backup))
            shutil.copytree(target,self.current)
            self._write_state(version)
            return InstallResult(True,"activate",str(self.root),version=version)
        except Exception as exc: return InstallResult(False,"activate",str(self.root),f"{type(exc).__name__}: {exc}",version)

    def rollback(self,version=None):
        try:
            if version:
                return self.activate(version)
            backups=sorted((p for p in self.backups.iterdir() if p.is_dir()),reverse=True) if self.backups.exists() else []
            if not backups: raise ValueError("No rollback backup is available.")
            backup=backups[0]
            if self.current.exists(): shutil.rmtree(self.current)
            shutil.copytree(backup,self.current)
            self._write_state(backup.name)
            return InstallResult(True,"rollback",str(self.root),version=backup.name)
        except Exception as exc: return InstallResult(False,"rollback",str(self.root),f"{type(exc).__name__}: {exc}")

    def uninstall(self):
        try:
            if self.root.exists(): shutil.rmtree(self.root)
            return InstallResult(True,"uninstall",str(self.root))
        except Exception as exc: return InstallResult(False,"uninstall",str(self.root),f"{type(exc).__name__}: {exc}")
