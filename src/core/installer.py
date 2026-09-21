"""Safe Toolkit lifecycle operations.

The installer only owns files under the Toolkit root. It never removes DCC
installations, user assets, or third-party files outside the owned root.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shutil
import tempfile

@dataclass(frozen=True)
class InstallResult:
    ok: bool
    action: str
    root: str
    error: str | None = None

class ToolkitInstaller:
    def __init__(self, root: str | Path):
        self.root = Path(root).expanduser().resolve()

    def _owned(self, path: str | Path) -> Path:
        target = Path(path).expanduser().resolve()
        try: target.relative_to(self.root)
        except ValueError: raise ValueError("Refusing to operate outside Toolkit root.")
        return target

    def install(self) -> InstallResult:
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            (self.root / "current").mkdir(exist_ok=True)
            (self.root / "versions").mkdir(exist_ok=True)
            (self.root / "backups").mkdir(exist_ok=True)
            return InstallResult(True, "install", str(self.root))
        except Exception as exc:
            return InstallResult(False, "install", str(self.root), f"{type(exc).__name__}: {exc}")

    def repair(self) -> InstallResult:
        return self.install().__class__(self.install().ok, "repair", str(self.root), self.install().error)

    def uninstall(self) -> InstallResult:
        try:
            if self.root.exists(): shutil.rmtree(self.root)
            return InstallResult(True, "uninstall", str(self.root))
        except Exception as exc:
            return InstallResult(False, "uninstall", str(self.root), f"{type(exc).__name__}: {exc}")

    def stage_update(self, source: str | Path) -> InstallResult:
        try:
            source=Path(source).expanduser().resolve()
            if not source.exists() or not source.is_dir(): raise ValueError("Update source directory does not exist.")
            self.root.mkdir(parents=True, exist_ok=True)
            staging=Path(tempfile.mkdtemp(prefix=".update-", dir=self.root))
            shutil.copytree(source, staging / "payload", dirs_exist_ok=True)
            return InstallResult(True, "stage_update", str(staging))
        except Exception as exc:
            return InstallResult(False, "stage_update", str(self.root), f"{type(exc).__name__}: {exc}")
