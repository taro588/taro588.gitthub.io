from __future__ import annotations

import argparse
import json

from .launcher import Launcher
from .launcher_gui import LauncherApp


def main() -> None:
    parser = argparse.ArgumentParser(prog="gameart")
    parser.add_argument("command", choices=["doctor", "detect", "start", "repair"], nargs="?", default="start")
    args = parser.parse_args()
    launcher = Launcher()

    if args.command == "start":
        LauncherApp(launcher).run()
        return

    if args.command == "detect":
        print(json.dumps([d.__dict__ for d in launcher.detect_dcc()], indent=2))
        return

    if args.command == "doctor":
        print(json.dumps(launcher.doctor(), indent=2))
        return

    print(json.dumps(launcher.repair(), indent=2))


if __name__ == "__main__":
    main()
