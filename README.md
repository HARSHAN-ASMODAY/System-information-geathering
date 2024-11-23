# System Access Tool Suite

An advanced system access and exploitation tool for security testing. **Use only with proper authorization and for educational purposes.**

## Features

- Port scanning with service detection
- Vulnerability assessment for common services:
  - SSH weak credentials
  - SMB vulnerabilities
  - RDP security checks
- System access capabilities:
  - SSH brute force protection bypass
  - SMB null session detection
  - Remote command execution
- Comprehensive logging
- Colored console output

## Prerequisites

- Python 3.x
- Required packages (install via requirements.txt)
- Administrator/root privileges for certain features

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python exploit_tool.py -t TARGET_IP -p PORTS
```

Example:
```bash
python exploit_tool.py -t 192.168.1.100 -p 22,445,3389
```

## Important Security Notice

This tool is for EDUCATIONAL PURPOSES ONLY. Unauthorized use of this tool against systems you don't own or have explicit permission to test is illegal and unethical.

## Features in Detail

1. Port Scanning
   - Service version detection
   - Common vulnerability checking
   - Automated service identification

2. SSH Testing
   - Weak credential detection
   - Authentication attempt monitoring
   - Command execution capability

3. SMB Analysis
   - Null session detection
   - Share enumeration
   - Access testing

4. RDP Security
   - Port accessibility check
   - Security configuration analysis

## Logging

The tool maintains detailed logs of all operations, including:
- Scan results
- Vulnerability findings
- Access attempts
- Error messages

## Requirements

See requirements.txt for the complete list of dependencies:
- paramiko
- python-nmap
- impacket
- colorama
- cryptography

## Disclaimer

The authors take no responsibility for misuse of this tool. Users are responsible for ensuring they have proper authorization before testing any systems.

# USB System Information Harvester

A sophisticated USB-based system information gathering tool for security testing and system analysis. **For educational purposes only - use with proper authorization.**

## Project Overview

This tool suite provides automated system information gathering capabilities through USB device insertion. When a USB drive containing these tools is inserted into a target system, it automatically collects and transmits detailed system information to a remote server.

## Components

1. **USB Monitor (`usb_monitor.py`)**
   - System information collection
   - Network configuration analysis
   - Drive space monitoring
   - Software inventory
   - User file enumeration
   - Stealth operation capabilities
   - Automatic server connection

2. **Server (`server.py`)**
   - Remote data collection
   - Multi-client support
   - JSON data processing
   - Organized data storage
   - Real-time monitoring
   - Colored console output

3. **USB Automation**
   - `autorun.inf` for automatic execution
   - `launch.bat` for silent deployment
   - Requirements installation
   - Persistence mechanism

## Features & Capabilities

### System Information Collection
```json
{
    "timestamp": "2024-11-24 00:41:25",
    "hostname": "HARSHU",
    "os": "Windows",
    "os_release": "11",
    "architecture": "AMD64",
    "processor": "Intel64 Family 6 Model 140 Stepping 1, GenuineIntel",
    "username": "harsh",
    "mac_address": "b6:b5:b*:**:**:**"
}
```

### Drive Information
```json
{
    "drives": [
        {
            "drive": "C:",
            "total_space": "226 GB",
            "used_space": "200 GB",
            "free_space": "26 GB"
        }
    ]
}
```

### Network Configuration
```json
{
    "network": {
        "ip_address": "172.2*.**.*",
        "public_ip": "106.195.**.**",
        "default_gateway": "4964%8"
    }
}
```

### Software Inventory
- Installed applications
- Version information
- Installation dates
- Update status

### User Data Analysis
- Documents folder scanning
- Desktop contents
- Download history
- File metadata

## Installation & Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Copy files to USB drive:
   - `usb_monitor.py`
   - `launch.bat`
   - `autorun.inf`
   - `requirements.txt`

3. Configure server:
```bash
python server.py
```
Server listens on `0.0.0.0:4444` by default

## Usage Example

1. Start the server:
```bash
python server.py
```

2. Insert USB into target system
3. Automatic execution begins
4. Data collection starts
5. Information transmitted to server
6. Results saved in `collected_data` directory

## Sample Output

### Server Console
```
[+] Server listening on 0.0.0.0:4444
[+] New connection from 172.20.10.5
[+] Data received and saved to: collected_data/172.20.10.5_20241124_004130.json
```

### Collected Data
```json
{
    "timestamp": "2024-11-24 00:41:25",
    "hostname": "HARSHU",
    "os": "Windows",
    "drives": [
        {
            "drive": "C:",
            "total_space": "226 GB",
            "used_space": "200 GB",
            "free_space": "26 GB"
        }
    ],
    "network": {
        "ip_address": "172.20.**.**",
        "public_ip": "106.195.**.**"
    },
    "installed_software": [
        "Adobe Creative Cloud",
        "Google Chrome",
        "Microsoft Edge",
        "Nmap 7.95"
    ]
}
```

## Security Features

1. **Stealth Operation**
   - Silent execution
   - Hidden window operation
   - Minimal system footprint

2. **Data Protection**
   - Secure transmission
   - JSON data formatting
   - Error handling

3. **Persistence**
   - Startup script creation
   - Error recovery
   - Reconnection capability

## Requirements

- Python 3.x
- Windows OS (target)
- Required packages:
  - requests
  - python-nmap
  - paramiko
  - colorama
  - socket
  - json

## Important Notice

This tool is designed for **EDUCATIONAL PURPOSES ONLY**. Usage of this tool on systems without explicit permission is:
- Potentially illegal
- Unethical
- May violate privacy laws
- Could result in criminal charges

Always obtain proper authorization before testing any system.

## Logging

All operations are logged in `system_info.log`:
- Connection attempts
- Data collection status
- Error messages
- System interactions

## Error Handling

- Network connection failures
- File access errors
- Permission issues
- Data transmission problems

## Future Enhancements

- [ ] Encrypted data transmission
- [ ] More detailed hardware information
- [ ] Process monitoring
- [ ] Network traffic analysis
- [ ] Cross-platform support

## Disclaimer

The authors take no responsibility for misuse of this tool. Users are responsible for ensuring they have proper authorization before testing any systems.
