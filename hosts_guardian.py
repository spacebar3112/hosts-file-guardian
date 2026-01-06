#!/usr/bin/env python3
"""
Hosts File Guardian - Monitors and protects the hosts file from unauthorized changes.
Runs silently in the background and automatically restores the hosts file to a known good state.
"""

import os
import sys
import shutil
import time
import logging
import stat
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
HOSTS_FILE = Path(r"C:\Windows\System32\drivers\etc\hosts")
BACKUP_FILE = Path(__file__).parent / "hosts_backup.txt"
LOG_FILE = Path(__file__).parent / "hosts_guardian.log"

# Setup logging (to file and optionally console for debugging)
import sys
DEBUG_MODE = '--debug' in sys.argv or '-d' in sys.argv

handlers = [logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')]
if DEBUG_MODE:
    handlers.append(logging.StreamHandler(sys.stdout))

logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=handlers
)
logger = logging.getLogger(__name__)


class HostsFileHandler(FileSystemEventHandler):
    """Handles file system events for the hosts file."""
    
    def __init__(self, backup_file, hosts_file):
        self.backup_file = backup_file
        self.hosts_file = hosts_file
        self.last_modified = 0
        self.processing = False
        
    def on_modified(self, event):
        """Called when the hosts file is modified."""
        if event.is_directory:
            return
        
        # Normalize paths for comparison
        event_path = os.path.normpath(event.src_path).lower()
        hosts_path = os.path.normpath(str(self.hosts_file)).lower()
        
        logger.debug(f"File system event: {event_path} (watching: {hosts_path})")
        
        if event_path == hosts_path:
            logger.info("Hosts file modification event detected")
            # Small delay to ensure file write is complete
            time.sleep(0.5)
            self._check_and_restore()
    
    def on_created(self, event):
        """Called when a file is created (handles file replacement)."""
        if event.is_directory:
            return
        
        # Normalize paths for comparison
        event_path = os.path.normpath(event.src_path).lower()
        hosts_path = os.path.normpath(str(self.hosts_file)).lower()
        
        if event_path == hosts_path:
            logger.info("Hosts file creation/replacement event detected")
            time.sleep(0.5)
            self._check_and_restore()
    
    def _check_and_restore(self, force=False):
        """Check if hosts file has changed and restore if necessary."""
        if self.processing and not force:
            logger.debug("Already processing, skipping check")
            return
            
        self.processing = True
        try:
            current_time = time.time()
            # Prevent rapid-fire restorations (debounce) unless forced
            if not force and current_time - self.last_modified < 1.0:
                logger.debug(f"Debounce: last check was {current_time - self.last_modified:.2f}s ago")
                return
            self.last_modified = current_time
            
            logger.debug("Checking hosts file for changes...")
            
            # Read current hosts file
            try:
                with open(self.hosts_file, 'r', encoding='utf-8', errors='ignore') as f:
                    current_content = f.read()
                logger.debug(f"Current hosts file size: {len(current_content)} bytes")
            except Exception as e:
                logger.error(f"Error reading hosts file: {e}")
                return
            
            # Read backup file
            try:
                with open(self.backup_file, 'r', encoding='utf-8', errors='ignore') as f:
                    backup_content = f.read()
                logger.debug(f"Backup file size: {len(backup_content)} bytes")
            except FileNotFoundError:
                logger.warning("Backup file not found. Creating initial backup...")
                self._create_backup()
                return
            except Exception as e:
                logger.error(f"Error reading backup file: {e}")
                return
            
            # Compare contents (normalize whitespace)
            current_normalized = current_content.strip().replace('\r\n', '\n').replace('\r', '\n')
            backup_normalized = backup_content.strip().replace('\r\n', '\n').replace('\r', '\n')
            
            if current_normalized != backup_normalized:
                logger.warning("=" * 60)
                logger.warning("Hosts file modification detected! Restoring from backup...")
                logger.warning(f"Current content preview: {current_content[:100]}...")
                logger.warning(f"Backup content preview: {backup_content[:100]}...")
                logger.warning("=" * 60)
                self._restore_hosts_file(backup_content)
            else:
                logger.debug("Hosts file unchanged (no modifications detected)")
                
        except Exception as e:
            logger.error(f"Error in check_and_restore: {e}")
        finally:
            self.processing = False
    
    def _create_backup(self):
        """Create initial backup of the hosts file."""
        try:
            if self.hosts_file.exists():
                shutil.copy2(self.hosts_file, self.backup_file)
                logger.info(f"Initial backup created at {self.backup_file}")
            else:
                logger.warning("Hosts file does not exist. Creating empty backup.")
                self.backup_file.write_text("", encoding='utf-8')
        except PermissionError:
            logger.error("Permission denied. Run as administrator!")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            sys.exit(1)
    
    def _restore_hosts_file(self, backup_content):
        """Restore the hosts file from backup with retry logic for locked files."""
        max_retries = 15
        retry_delay = 0.3
        
        # Remove read-only attribute and prepare file for writing
        if sys.platform == 'win32':
            try:
                import stat
                import ctypes
                from ctypes import wintypes
                
                # Remove read-only attribute
                try:
                    file_stat = os.stat(self.hosts_file)
                    if not file_stat.st_mode & stat.S_IWRITE:
                        os.chmod(self.hosts_file, stat.S_IWRITE)
                        logger.debug("Removed read-only attribute")
                except Exception as e:
                    logger.debug(f"Could not change file attributes: {e}")
                
                # Try to close any open handles to the file
                kernel32 = ctypes.windll.kernel32
                try:
                    # Open with maximum access
                    handle = kernel32.CreateFileW(
                        str(self.hosts_file),
                        0x40000000,  # GENERIC_WRITE
                        0x00000001 | 0x00000002 | 0x00000004,  # FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE
                        None,
                        0x00000003,  # OPEN_EXISTING
                        0x02000000,  # FILE_FLAG_BACKUP_SEMANTICS
                        None
                    )
                    if handle != -1 and handle != 0xFFFFFFFF:  # INVALID_HANDLE_VALUE
                        kernel32.CloseHandle(handle)
                        logger.debug("Closed file handles")
                        time.sleep(0.2)
                except Exception as e:
                    logger.debug(f"Could not close file handles: {e}")
            except Exception as e:
                logger.debug(f"Windows-specific file handling error: {e}")
        
        for attempt in range(max_retries):
            try:
                # Method 1: Try direct write
                try:
                    with open(self.hosts_file, 'w', encoding='utf-8') as f:
                        f.write(backup_content)
                    logger.debug(f"Direct write succeeded (attempt {attempt + 1})")
                except (PermissionError, IOError, OSError):
                    # Method 2: Try using a temporary file and move
                    if sys.platform == 'win32':
                        temp_file = self.hosts_file.with_suffix('.tmp')
                        try:
                            # Write to temp file
                            with open(temp_file, 'w', encoding='utf-8') as f:
                                f.write(backup_content)
                            
                            # Remove read-only from target
                            try:
                                os.chmod(self.hosts_file, stat.S_IWRITE)
                            except:
                                pass
                            
                            # Replace the file
                            if self.hosts_file.exists():
                                self.hosts_file.unlink()
                            temp_file.replace(self.hosts_file)
                            logger.debug(f"Temp file method succeeded (attempt {attempt + 1})")
                        except Exception as e:
                            logger.debug(f"Temp file method failed: {e}")
                            if temp_file.exists():
                                try:
                                    temp_file.unlink()
                                except:
                                    pass
                            raise
                    else:
                        raise
                
                # Verify the restore worked
                time.sleep(0.2)
                with open(self.hosts_file, 'r', encoding='utf-8', errors='ignore') as f:
                    restored_content = f.read()
                
                # Normalize for comparison
                restored_normalized = restored_content.strip().replace('\r\n', '\n').replace('\r', '\n')
                backup_normalized = backup_content.strip().replace('\r\n', '\n').replace('\r', '\n')
                
                if restored_normalized == backup_normalized:
                    logger.info("Hosts file restored successfully")
                    return True
                else:
                    logger.warning(f"Restore verification failed (attempt {attempt + 1}/{max_retries})")
                    logger.debug(f"Restored length: {len(restored_content)}, Backup length: {len(backup_content)}")
                    
            except PermissionError as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Permission denied, retrying in {retry_delay:.1f}s (attempt {attempt + 1}/{max_retries})...")
                    logger.debug(f"Error details: {e}")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 1.3, 2.0)  # Cap at 2 seconds
                else:
                    logger.error(f"Permission denied after {max_retries} attempts!")
                    logger.error("Make sure:")
                    logger.error("  1. You're running as Administrator")
                    logger.error("  2. No other programs have the hosts file open")
                    logger.error("  3. Antivirus is not blocking file access")
                    return False
            except (IOError, OSError) as e:
                if attempt < max_retries - 1:
                    logger.warning(f"File locked, retrying in {retry_delay:.1f}s (attempt {attempt + 1}/{max_retries})...")
                    logger.debug(f"Error details: {e}")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 1.3, 2.0)
                else:
                    logger.error(f"Error restoring hosts file after {max_retries} attempts: {e}")
                    return False
            except Exception as e:
                logger.error(f"Unexpected error restoring hosts file: {e}")
                import traceback
                logger.debug(traceback.format_exc())
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 1.3, 2.0)
                else:
                    return False
        
        return False


class HostsGuardian:
    """Main application class for monitoring the hosts file."""
    
    def __init__(self):
        self.observer = None
        self.event_handler = None
        
    def initialize(self):
        """Initialize the guardian and create backup if needed."""
        # Check if running as administrator
        if not self._is_admin():
            logger.error("This application requires administrator privileges!")
            return False
        
        # Create backup if it doesn't exist
        if not BACKUP_FILE.exists():
            handler = HostsFileHandler(BACKUP_FILE, HOSTS_FILE)
            handler._create_backup()
        
        return True
    
    def _is_admin(self):
        """Check if running with administrator privileges."""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def start(self):
        """Start monitoring the hosts file."""
        if not self.initialize():
            logger.error("Initialization failed. Exiting.")
            return False
        
        # Create event handler
        self.event_handler = HostsFileHandler(BACKUP_FILE, HOSTS_FILE)
        
        # Create observer
        self.observer = Observer()
        
        # Watch the directory containing the hosts file
        watch_dir = HOSTS_FILE.parent
        self.observer.schedule(self.event_handler, str(watch_dir), recursive=False)
        
        # Start observer
        self.observer.start()
        logger.info("=" * 60)
        logger.info("Hosts Guardian started successfully!")
        logger.info(f"Monitoring: {HOSTS_FILE}")
        logger.info(f"Backup file: {BACKUP_FILE}")
        logger.info(f"Log file: {LOG_FILE}")
        logger.info("Periodic checks every 3 seconds")
        logger.info("=" * 60)
        
        # Do an initial check
        logger.info("Performing initial check...")
        self.event_handler._check_and_restore(force=True)
        
        return True
    
    def stop(self):
        """Stop monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Hosts Guardian stopped")
    
    def run(self):
        """Run the guardian (blocking) with periodic checks."""
        if not self.start():
            return
        
        # Periodic check interval (every 3 seconds)
        CHECK_INTERVAL = 3.0
        last_check = time.time()
        
        try:
            while True:
                time.sleep(0.5)
                
                # Periodic check in addition to file system events
                # This catches changes even if file system events are missed
                current_time = time.time()
                if current_time - last_check >= CHECK_INTERVAL:
                    logger.debug("Periodic check triggered")
                    if self.event_handler:
                        self.event_handler._check_and_restore(force=True)
                    last_check = current_time
                    
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.stop()


def main():
    """Main entry point."""
    guardian = HostsGuardian()
    guardian.run()


if __name__ == "__main__":
    main()

