# Hosts File Guardian

A background application that monitors the Windows hosts file (`C:\Windows\System32\drivers\etc\hosts`) and automatically reverts any unauthorized changes back to a known good state.

**Perfect for:** System administrators, parents, or anyone who needs to ensure the hosts file remains protected from unauthorized modifications.

## Features

- **Silent Background Operation**: Runs covertly without visible windows
- **Automatic Monitoring**: Watches the hosts file for changes in real-time
- **Auto-Restore**: Immediately reverts any modifications to the protected state
- **Windows Service Support**: Can run as a Windows service for persistent protection
- **Minimal Logging**: Logs only to file, no console output

## Requirements

- Windows 10/11
- Python 3.7+
- Administrator privileges (for modifying hosts file)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run as Administrator** (required for file access)

## Usage

### Option 1: Run as Background Process

Run directly in the background:
```bash
python hosts_guardian.py
```

Or use the background runner (hides console window):
```bash
python run_background.py
```

**To Stop:**
- If running in a terminal: Press `Ctrl+C`
- If running in background: Run `stop_guardian.bat` (double-click or run as admin)
- Or use Task Manager to kill the Python process

### Option 2: Install as Windows Service (Recommended)

For persistent protection that starts automatically:

1. **Install the service:**
   - Right-click `install_service.bat` and select "Run as administrator"
   - Or run: `python hosts_guardian_service.py install`

2. **Start the service:**
   ```bash
   python hosts_guardian_service.py start
   ```
   Or use Services.msc (services.msc) and start "Hosts File Guardian Service"

3. **Stop the service:**
   ```bash
   python hosts_guardian_service.py stop
   ```

4. **Uninstall the service:**
   - Right-click `uninstall_service.bat` and select "Run as administrator"
   - Or run: `python hosts_guardian_service.py remove`

## How It Works

1. On first run, the application creates a backup of the current hosts file (`hosts_backup.txt`)
2. It monitors the hosts file directory for changes using file system events
3. When a change is detected, it compares the current file with the backup
4. If they differ, it immediately restores the file from the backup
5. All activity is logged to `hosts_guardian.log`

## Files

- `hosts_guardian.py` - Main monitoring application
- `hosts_guardian_service.py` - Windows service wrapper
- `run_background.py` - Background runner (hides console)
- `start_guardian.bat` - Start the guardian in background
- `stop_guardian.bat` - Stop any running guardian processes
- `hosts_backup.txt` - Backup of the protected hosts file (created automatically)
- `hosts_guardian.log` - Application log file

## Notes

- The application must run with administrator privileges to modify the hosts file
- The backup file (`hosts_backup.txt`) contains the "known good" state
- To update the protected state, stop the guardian, modify `hosts_backup.txt`, then restart
- The service runs silently with no visible windows or notifications

## Troubleshooting

- Check `hosts_guardian.log` for errors
- Ensure you're running as Administrator
- Verify the hosts file path is accessible
- For service issues, check Windows Event Viewer or `hosts_guardian_service.log`
- If you get "Permission denied" errors, run `fix_permissions.bat` as administrator
- For service error 1053, see [Service Issues](#service-issues) below

### Service Issues

If the Windows service fails to start (error 1053):

1. **Uninstall and reinstall:**
   ```bash
   python hosts_guardian_service.py remove
   python hosts_guardian_service.py install
   ```

2. **Check the service log:**
   - Open `hosts_guardian_service.log` for detailed error messages

3. **Verify Python path:**
   - The service needs to find Python in the system PATH
   - Or manually edit the service to use full Python path

4. **Alternative:** Use the background process method instead of the service

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

