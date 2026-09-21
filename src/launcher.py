"""GameArt Toolkit launcher and DCC discovery."""
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class DCCInstallation:
    name: str
    version: str
    path: Path

@dataclass
class LauncherConfig:
    install_root: Path
    config_root: Path

class Launcher:
    def __init__(self, config: LauncherConfig):
        self.config = config

    def health_check(self):
        return {"installed": self.config.install_root.exists(),
                "install_root": str(self.config.install_root)}

    def detect_dcc(self):
        found = []
        for name, env in (("Maya", "MAYA_LOCATION"), ("3ds Max", "ADSK_3DSMAX_ROOT")):
            value = os.environ.get(env)
            if value:
                found.append(DCCInstallation(name, "detected", Path(value)))
        return found

    def start(self):
        return {"status": "ready", **self.health_check()}
