@echo off
REM Test the service installation and configuration
REM Must be run as Administrator

cd /d "%~dp0"

echo Testing Hosts Guardian Service...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    pause
    exit /b 1
)

echo Checking service status...
sc query HostsGuardian >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Service is installed
    echo.
    echo Current service status:
    sc query HostsGuardian
    echo.
) else (
    echo [NOT INSTALLED] Service is not installed
    echo Run install_service.bat first
    pause
    exit /b 1
)

echo.
echo Checking service configuration...
sc qc HostsGuardian

echo.
echo Checking log file...
if exist hosts_guardian_service.log (
    echo Last 10 lines of service log:
    powershell -Command "Get-Content hosts_guardian_service.log -Tail 10"
) else (
    echo [INFO] Service log file not found yet
)

echo.
pause


