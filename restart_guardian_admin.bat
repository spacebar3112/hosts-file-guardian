@echo off
REM Stop and restart Hosts Guardian with proper admin privileges
REM Must be run as Administrator

cd /d "%~dp0"

echo Stopping any running instances...
call stop_guardian.bat

timeout /t 2 /nobreak >nul

echo.
echo Starting Hosts Guardian with admin privileges...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Start with visible window first to verify it works
echo Starting guardian (you can close this window after verifying it started)...
echo.
python hosts_guardian.py

pause


