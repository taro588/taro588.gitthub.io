"""GameArt Toolkit launcher, discovery, diagnostics, and optional capability health."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os, platform
from .dcc.manager import DCCManager
from .dcc.session import DCCSession
from .maya.adapter import MayaAdapter
from .max.adapter import MaxAdapter
from .core.plugins import PluginRegistry, PluginSpec

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
    def __init__(self, config: LauncherConfig | None = None):
        home=Path.home()
        self.config=config or LauncherConfig(home/"GameArtAI"/"Toolkit", home/"GameArtAI"/"Config")
        self.dcc=DCCManager()
        self.dcc.register("maya", DCCSession(MayaAdapter()))
        self.dcc.register("3ds_max", DCCSession(MaxAdapter()))
        self.plugins=PluginRegistry()

    def health_check(self):
        return {"installed":self.config.install_root.exists(),"install_root":str(self.config.install_root),"config_root":str(self.config.config_root)}

    def detect_dcc(self):
        found=[]
        for name,env in (("Maya","MAYA_LOCATION"),("3ds Max","ADSK_3DSMAX_ROOT")):
            value=os.environ.get(env)
            if value:
                path=Path(value).expanduser()
                found.append(DCCInstallation(name,"detected" if path.exists() else "environment_only",path))
        return found

    def dcc_status(self):
        self.dcc.connect_all()
        return self.dcc.status()

    def doctor(self):
        detections=self.detect_dcc()
        dcc_api=self.dcc_status()
        dcc_failures=[n for n,i in dcc_api.items() if not i.get("connected")]
        return {"status":"degraded" if dcc_failures else "ready","toolkit":"GameArt AI Toolkit","version":"0.1.0-alpha","python":platform.python_version(),"platform":platform.platform(),"launcher":self.health_check(),"environment_detection":[{"name":d.name,"version":d.version,"path":str(d.path)} for d in detections],"dcc_api":dcc_api,"dcc_failures":dcc_failures,"plugins":[h.__dict__ for h in self.plugins.health()]}

    def repair(self):
        self.config.config_root.mkdir(parents=True,exist_ok=True)
        return {"status":"ready","action":"repair","config_root":str(self.config.config_root)}

    def start(self):
        return {"status":"ready",**self.health_check()}
