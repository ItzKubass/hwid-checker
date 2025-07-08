# HWID Checker

**HWID Checker** is a tool for collecting and displaying detailed hardware and system identifiers (HWID) on Windows computers. It is designed for developers of anti-cheat systems, network administrators, or anyone who needs a unique device fingerprint to verify a computer's identity.

---

## Features

- Retrieves basic system information (PC name, Windows version)
- Reads the unique `MachineGuid` from the Windows registry
- Fetches Windows Product ID
- Retrieves current user SID
- Lists MAC addresses of all active network adapters
- Provides detailed info about CPU, disks, motherboard, BIOS, RAM, and GPU
- Lists running processes and installed drivers (sample)
- Detects virtualization environments (e.g., VMware, virtual machines)
- Shows Windows installation date

---

## Why HWID Checker?

HWID (Hardware ID) is a unique identifier of a computer based on hardware and system details. It is commonly used for:

- Verifying user or device identity
- Implementing anti-cheat mechanisms in games
- Software license management
- Device tracking and security in corporate environments

---

## Requirements

- Windows operating system (tested on Windows 10/11)
- Python 3.x
- Installed `wmi` Python module (`pip install wmi`)
- Recommended to run with administrator privileges to access all system info

---

## Usage

1. Install Python 3.x if you don’t have it already
2. Install dependencies:
   ```bash
   pip install wmi
Run the script:

bash
Zkopírovat
Upravit
python hwid_checker.py
In the GUI window, click the Load Full System Info button to display the complete system fingerprint.

Security and Privacy
This tool collects sensitive hardware and system information. Use it only on devices you own or have permission to inspect. Do not share collected data without the owner’s consent.

License
This project is open source. You are free to use and modify it. Please credit the author if you include it in your own projects.
