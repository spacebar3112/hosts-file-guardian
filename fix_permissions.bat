@echo off
REM Fix permissions on hosts file
REM Must be run as Administrator

cd /d "%~dp0"

echo Fixing hosts file permissions...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Remove read-only attribute from hosts file
attrib -R "C:\Windows\System32\drivers\etc\hosts" 2>nul
if %errorLevel% equ 0 (
    echo [OK] Removed read-only attribute from hosts file
) else (
    echo [WARNING] Could not remove read-only attribute
)

REM Grant full control to Administrators
icacls "C:\Windows\System32\drivers\etc\hosts" /grant Administrators:F 2>nul
if %errorLevel% equ 0 (
    echo [OK] Granted full control to Administrators
) else (
    echo [WARNING] Could not modify ACLs
)

echo.
echo Done. Try running the guardian again.
echo.
pause


