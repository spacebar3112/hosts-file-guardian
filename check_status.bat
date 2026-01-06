@echo off
REM Check if Hosts Guardian is running and has admin privileges

cd /d "%~dp0"

echo Checking Hosts Guardian Status...
echo.

REM Check if Python process is running
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *hosts_guardian*" 2>nul | find /I "python.exe" >nul
if %errorLevel% equ 0 (
    echo [OK] Python process found running hosts_guardian
) else (
    echo [NOT RUNNING] No Python process found running hosts_guardian
)

tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul | find /I "pythonw.exe" >nul
if %errorLevel% equ 0 (
    echo [OK] Pythonw process found (may be running guardian)
) else (
    echo [INFO] No pythonw.exe process found
)

echo.
echo Checking log file for recent activity...
if exist hosts_guardian.log (
    echo Last 5 lines of log:
    powershell -Command "Get-Content hosts_guardian.log -Tail 5"
) else (
    echo [WARNING] Log file not found - guardian may not have run yet
)

echo.
echo Checking backup file...
if exist hosts_backup.txt (
    echo [OK] Backup file exists
    for %%A in (hosts_backup.txt) do echo    Size: %%~zA bytes
) else (
    echo [WARNING] Backup file not found - guardian will create it on first run
)

echo.
pause


