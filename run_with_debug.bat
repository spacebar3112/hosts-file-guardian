@echo off
REM Run Hosts Guardian with debug output visible
REM Must be run as Administrator

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Running Hosts Guardian with debug output...
echo Press Ctrl+C to stop
echo.

python hosts_guardian.py --debug

pause

