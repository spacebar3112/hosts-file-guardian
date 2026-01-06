@echo off
REM Install Hosts Guardian as a Windows Service
REM Must be run as Administrator

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Installing Hosts Guardian Service...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Get the full path to the Python script
set SCRIPT_PATH=%~dp0hosts_guardian_service.py

REM Install the service with full path
python "%SCRIPT_PATH%" install

if %errorLevel% equ 0 (
    echo.
    echo Service installed successfully!
    echo.
    echo To start the service, run:
    echo   python hosts_guardian_service.py start
    echo.
    echo Or use Services.msc to start it.
) else (
    echo.
    echo Failed to install service. Make sure pywin32 is installed.
    echo Install with: pip install pywin32
)

pause

