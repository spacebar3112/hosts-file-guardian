@echo off
REM Install Hosts Guardian as a Windows Service with full Python path
REM This fixes the 1053 error by using explicit Python executable path
REM Must be run as Administrator

cd /d "%~dp0"

echo Installing Hosts Guardian Service (Fixed Version)...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Find Python executable
echo Finding Python executable...
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python not found in PATH!
    echo Make sure Python is installed and added to PATH.
    pause
    exit /b 1
)

REM Get full path to Python
for /f "delims=" %%i in ('where python') do set PYTHON_EXE=%%i
echo Found Python: %PYTHON_EXE%

REM Get full paths
set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%hosts_guardian_service.py

echo Script path: %SCRIPT_PATH%
echo.

REM Uninstall existing service first
echo Removing existing service (if any)...
"%PYTHON_EXE%" "%SCRIPT_PATH%" stop 2>nul
"%PYTHON_EXE%" "%SCRIPT_PATH%" remove 2>nul

echo.
echo Installing service with explicit Python path...
"%PYTHON_EXE%" "%SCRIPT_PATH%" install

if %errorLevel% equ 0 (
    echo.
    echo Service installed successfully!
    echo.
    echo IMPORTANT: The service is configured to use:
    echo   Python: %PYTHON_EXE%
    echo   Script: %SCRIPT_PATH%
    echo.
    echo To start the service:
    echo   1. Use Services.msc (services.msc)
    echo   2. Find "Hosts File Guardian Service"
    echo   3. Right-click and select "Start"
    echo.
    echo Or run: "%PYTHON_EXE%" "%SCRIPT_PATH%" start
    echo.
    echo If you still get error 1053, check hosts_guardian_service.log
) else (
    echo.
    echo Failed to install service.
    echo.
    echo Troubleshooting:
    echo   1. Make sure pywin32 is installed: pip install pywin32
    echo   2. Make sure watchdog is installed: pip install watchdog
    echo   3. Verify Python path is correct: %PYTHON_EXE%
    echo   4. Check that the script exists: %SCRIPT_PATH%
)

pause

