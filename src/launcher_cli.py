from __future__ import annotations

import argparse
import json

from .launcher import Launcher
from .launcher_gui import LauncherApp

def _json_default(value):
    return str(value)

def main() -> None:
    parser = argparse.ArgumentParser(prog="gameart")
    parser.add_argument("command", choices=["doctor", "detect", "start", "repair"], nargs="?", default="start")
    args = parser.parse_args()
    launcher = Launcher()

    if args.command == "start":
        LauncherApp(launcher).run()
        return

    if args.command == "detect":
        payload = [{"name": d.name, "version": d.version, "path": str(d.path)} for d in launcher.detect_dcc()]
        print(json.dumps(payload, indent=2, ensure_ascii=False, default=_json_default))
        return

    if args.command == "doctor":
        print(json.dumps(launcher.doctor(), indent=2, ensure_ascii=False, default=_json_default))
        return

    print(json.dumps(launcher.repair(), indent=2, ensure_ascii=False, default=_json_default))

if __name__ == "__main__":
    main()
