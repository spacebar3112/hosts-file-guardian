#!/usr/bin/env python3
"""
Windows Service wrapper for Hosts Guardian.
Allows the application to run as a Windows service for true background operation.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Change to script directory (services run from system32 by default)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

# Setup logging to file before importing (in case of errors)
log_file = os.path.join(script_dir, "hosts_guardian_service.log")
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(log_file, mode='a', encoding='utf-8')]
    )
except:
    pass  # If logging fails, continue anyway

try:
    import win32serviceutil
    import win32service
    import servicemanager
except ImportError:
    print("pywin32 is required for service functionality.")
    print("Install with: pip install pywin32")
    sys.exit(1)

from hosts_guardian import HostsGuardian


class HostsGuardianService(win32serviceutil.ServiceFramework):
    """Windows Service class for Hosts Guardian."""
    
    _svc_name_ = "HostsGuardian"
    _svc_display_name_ = "Hosts File Guardian Service"
    _svc_description_ = "Monitors and protects the Windows hosts file from unauthorized modifications"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        import threading
        self.stop_event = threading.Event()
        self.guardian = None
        
    def SvcStop(self):
        """Stop the service."""
        try:
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            logging.info("Stopping Hosts Guardian Service...")
            if self.guardian:
                self.guardian.stop()
            self.stop_event.set()
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        except Exception as e:
            logging.error(f"Error stopping service: {e}", exc_info=True)
        
    def SvcDoRun(self):
        """Run the service."""
        try:
            # Report that service is starting
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            
            # Report start pending
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            
            # Start the main loop in a separate thread to avoid blocking
            import threading
            main_thread = threading.Thread(target=self.main, daemon=False)
            main_thread.start()
            
            # Give it a moment to initialize
            time.sleep(0.5)
            
            # Report running status immediately (required to prevent timeout)
            # The actual initialization happens in the background thread
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            
            # Wait for the main thread or stop event
            while main_thread.is_alive() and not self.stop_event.is_set():
                time.sleep(1)
                
        except Exception as e:
            servicemanager.LogErrorMsg(f"Service startup error: {e}")
            import traceback
            servicemanager.LogErrorMsg(traceback.format_exc())
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        
    def main(self):
        """Main service loop."""
        try:
            logging.info("=" * 60)
            logging.info("Hosts Guardian Service starting...")
            logging.info(f"Working directory: {os.getcwd()}")
            logging.info(f"Script directory: {script_dir}")
            
            self.guardian = HostsGuardian()
            
            if not self.guardian.start():
                error_msg = "Failed to start Hosts Guardian"
                logging.error(error_msg)
                servicemanager.LogErrorMsg(error_msg)
                return
            
            logging.info("Hosts Guardian Service started successfully")
            logging.info("=" * 60)
            
            # Keep service running
            while not self.stop_event.is_set():
                time.sleep(1)
                
        except Exception as e:
            error_msg = f"Service error: {e}"
            logging.error(error_msg, exc_info=True)
            servicemanager.LogErrorMsg(error_msg)
        finally:
            if self.guardian:
                logging.info("Stopping guardian...")
                self.guardian.stop()
            logging.info("Hosts Guardian Service stopped")


def main():
    """Service entry point."""
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(HostsGuardianService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(HostsGuardianService)


if __name__ == "__main__":
    main()

