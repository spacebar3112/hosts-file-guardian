@echo off
REM Stop Hosts Guardian process

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Stopping Hosts Guardian...
echo.

REM Try to stop Windows service first (if installed)
python hosts_guardian_service.py stop 2>nul

REM Kill any running Python processes with hosts_guardian
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *hosts_guardian*" 2>nul
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq *hosts_guardian*" 2>nul

REM More aggressive: kill all python processes running hosts_guardian
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /I "hosts_guardian" >nul
    if not errorlevel 1 (
        taskkill /F /PID %%a 2>nul
        echo Stopped process PID %%a
    )
)

for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /I "hosts_guardian" >nul
    if not errorlevel 1 (
        taskkill /F /PID %%a 2>nul
        echo Stopped process PID %%a
    )
)

echo.
echo Hosts Guardian stopped.
echo.
pause

