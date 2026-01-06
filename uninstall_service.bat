@echo off
REM Uninstall Hosts Guardian Windows Service
REM Must be run as Administrator

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Uninstalling Hosts Guardian Service...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Stop the service first
python hosts_guardian_service.py stop

REM Remove the service
python hosts_guardian_service.py remove

if %errorLevel% equ 0 (
    echo.
    echo Service uninstalled successfully!
) else (
    echo.
    echo Failed to uninstall service.
)

pause

