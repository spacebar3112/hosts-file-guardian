#!/usr/bin/env python3
"""
Test script to verify Hosts Guardian is working.
This will make a test change to the hosts file and verify it gets reverted.
"""

import sys
import time
import subprocess
from pathlib import Path

HOSTS_FILE = Path(r"C:\Windows\System32\drivers\etc\hosts")
BACKUP_FILE = Path(__file__).parent / "hosts_backup.txt"

def test_guardian():
    """Test if the guardian is working by making a test change."""
    print("=" * 60)
    print("Hosts Guardian Test")
    print("=" * 60)
    print()
    
    # Check if running as admin
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("ERROR: This test must be run as Administrator!")
            print("Right-click test_guardian.bat and select 'Run as administrator'")
            return False
        print("✓ Running with administrator privileges")
    except Exception as e:
        print(f"WARNING: Could not verify admin status: {e}")
        print("Attempting to continue...")
    
    # Read current hosts file
    try:
        with open(HOSTS_FILE, 'r', encoding='utf-8') as f:
            original_content = f.read()
        print(f"✓ Read hosts file ({len(original_content)} bytes)")
    except Exception as e:
        print(f"ERROR: Could not read hosts file: {e}")
        return False
    
    # Read backup file
    try:
        with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        print(f"✓ Read backup file ({len(backup_content)} bytes)")
    except Exception as e:
        print(f"ERROR: Could not read backup file: {e}")
        return False
    
    # Make a test change
    test_line = "\n# TEST LINE - SHOULD BE REMOVED BY GUARDIAN\n"
    test_content = original_content + test_line
    
    print()
    print("Making test change to hosts file...")
    try:
        # Try to remove read-only attribute if present
        try:
            import os
            import stat
            file_stat = os.stat(HOSTS_FILE)
            if not file_stat.st_mode & stat.S_IWRITE:
                os.chmod(HOSTS_FILE, stat.S_IWRITE)
        except:
            pass
        
        with open(HOSTS_FILE, 'w', encoding='utf-8') as f:
            f.write(test_content)
        print("✓ Test change written")
    except PermissionError as e:
        print(f"ERROR: Permission denied. Make sure you're running as Administrator!")
        print(f"Details: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Could not write test change: {e}")
        return False
    
    # Wait for guardian to detect and revert
    print()
    print("Waiting for guardian to detect and revert (max 10 seconds)...")
    for i in range(10):
        time.sleep(1)
        try:
            with open(HOSTS_FILE, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Check if the test line is gone
            if test_line not in current_content:
                # Check if it matches backup
                if current_content.strip() == backup_content.strip():
                    print(f"✓ SUCCESS! File was reverted after {i+1} seconds")
                    print()
                    print("Hosts Guardian is working correctly!")
                    return True
                else:
                    print(f"  Test line removed but content doesn't match backup (check {i+1}/10)")
            else:
                print(f"  Still waiting... (check {i+1}/10)")
        except Exception as e:
            print(f"  Error checking file: {e}")
    
    print()
    print("✗ FAILED: File was not reverted within 10 seconds")
    print()
    print("Possible issues:")
    print("  1. Guardian is not running")
    print("  2. Guardian doesn't have admin privileges")
    print("  3. Check hosts_guardian.log for errors")
    
    # Restore manually
    print()
    print("Restoring file manually...")
    try:
        with open(HOSTS_FILE, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        print("✓ File restored manually")
    except Exception as e:
        print(f"ERROR: Could not restore file: {e}")
    
    return False

if __name__ == "__main__":
    success = test_guardian()
    sys.exit(0 if success else 1)

