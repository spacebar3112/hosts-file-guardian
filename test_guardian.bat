@echo off
REM Test Hosts Guardian functionality
REM Must be run as Administrator

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Testing Hosts Guardian...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

python test_guardian.py

pause

