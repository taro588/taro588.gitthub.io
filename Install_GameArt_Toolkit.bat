@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m src.installer_app
  exit /b %errorlevel%
)
where python >nul 2>nul
if %errorlevel%==0 (
  python -m src.installer_app
  exit /b %errorlevel%
)
echo Python 3 is required. Please install Python 3.10+ and run this installer again.
pause
