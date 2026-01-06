# Service Troubleshooting Guide

## Error 1053: The service did not respond to the start or control request

This error typically occurs when:
1. Python executable cannot be found
2. Script path is incorrect
3. Service times out before reporting status
4. Missing dependencies

## Solutions

### Solution 1: Use the Fixed Installer

Use `install_service_fixed.bat` which explicitly sets the Python path:

1. Right-click `install_service_fixed.bat` → "Run as administrator"
2. This will find Python and install the service with full paths

### Solution 2: Manual Service Configuration

If the installer doesn't work, manually configure the service:

1. Install the service normally:
   ```bash
   python hosts_guardian_service.py install
   ```

2. Open Services.msc (services.msc)

3. Find "Hosts File Guardian Service"

4. Right-click → Properties

5. In the "General" tab, note the "Path to executable"

6. Edit the path to use full Python path:
   - Find your Python: `where python`
   - Update the service path to: `C:\Full\Path\To\Python.exe C:\Full\Path\To\hosts_guardian_service.py`

### Solution 3: Check Logs

Check `hosts_guardian_service.log` for detailed error messages.

### Solution 4: Verify Dependencies

Make sure all dependencies are installed:
```bash
pip install watchdog pywin32
```

### Solution 5: Use Background Process Instead

If the service continues to fail, use the background process method:
- Run `start_guardian.bat` as administrator
- Or run `python hosts_guardian.py` directly

This provides the same protection without service complications.

## Common Issues

### "Python not found"
- Add Python to system PATH
- Or use full path to Python in service configuration

### "Module not found"
- Install dependencies: `pip install -r requirements.txt`
- Make sure Python can find the modules

### "Permission denied"
- Service must run with administrator privileges
- Check service "Log on as" settings in Services.msc

## Alternative: Task Scheduler

If Windows Service continues to fail, use Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Hosts File Guardian"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program: `C:\Full\Path\To\Python.exe`
7. Arguments: `C:\Full\Path\To\hosts_guardian.py`
8. Check "Run with highest privileges"

