"""CLI entry point for launcher operations."""
import argparse
from pathlib import Path
from .launcher import Launcher, LauncherConfig

def main():
    parser = argparse.ArgumentParser(prog="gameart-launcher")
    parser.add_argument("command", choices=["doctor", "detect", "start", "repair"])
    args = parser.parse_args()
    root = Path.cwd()
    launcher = Launcher(LauncherConfig(root, root / "config"))
    if args.command == "doctor":
        print(launcher.health_check())
    elif args.command == "detect":
        for dcc in launcher.detect_dcc():
            print(f"{dcc.name}: {dcc.path}")
    elif args.command == "start":
        print(launcher.start())
    else:
        print("Repair mode: validate Toolkit-owned files and DCC registration.")

if __name__ == "__main__":
    main()
