#!/usr/bin/env python3
"""
Simple background runner for Hosts Guardian.
Runs the application in the background without a console window.
"""

import sys
import os

# Hide console window
if sys.platform == 'win32':
    try:
        import win32gui
        import win32con
        
        # Hide the console window
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)
    except ImportError:
        # If pywin32 not available, continue without hiding window
        pass

# Run the main guardian
from hosts_guardian import HostsGuardian

if __name__ == "__main__":
    guardian = HostsGuardian()
    guardian.run()

