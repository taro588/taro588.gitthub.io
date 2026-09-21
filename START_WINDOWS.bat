@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo [GameArt AI Toolkit] Creating virtual environment...
  py -3 -m venv .venv
  if errorlevel 1 (
    echo Failed to create Python environment. Please install Python 3.10+.
    pause
    exit /b 1
  )
)
".venv\Scripts\python.exe" -m pip install -e . --quiet
if errorlevel 1 (
  echo Installation failed.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m src.launcher_cli start
if errorlevel 1 pause
