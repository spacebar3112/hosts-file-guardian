@echo off
REM Reinstall Hosts Guardian Service (removes old, installs new)
REM Must be run as Administrator

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Reinstalling Hosts Guardian Service...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Stop and remove existing service
echo Stopping existing service (if any)...
python hosts_guardian_service.py stop 2>nul
python hosts_guardian_service.py remove 2>nul

echo.
echo Installing service...
python hosts_guardian_service.py install

if %errorLevel% equ 0 (
    echo.
    echo Service installed successfully!
    echo.
    echo To start the service, run:
    echo   python hosts_guardian_service.py start
    echo.
    echo Or use Services.msc to start it.
    echo.
    echo NOTE: Make sure Python and all dependencies are installed.
    echo       The service will log errors to hosts_guardian_service.log
) else (
    echo.
    echo Failed to install service.
    echo Make sure:
    echo   1. pywin32 is installed: pip install pywin32
    echo   2. watchdog is installed: pip install watchdog
    echo   3. You're running as Administrator
)

pause

