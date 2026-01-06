@echo off
REM Start Hosts Guardian in background mode
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

REM Start the guardian in background with elevated privileges
REM Using PowerShell to ensure admin privileges are maintained
powershell -Command "Start-Process pythonw.exe -ArgumentList 'run_background.py' -Verb RunAs -WindowStyle Hidden"

echo Hosts Guardian started in background.
echo Check hosts_guardian.log for status.
echo.
echo NOTE: If you see "Permission denied" errors in the log,
echo       the guardian may not have admin privileges.
echo       Try running hosts_guardian.py directly as administrator.

