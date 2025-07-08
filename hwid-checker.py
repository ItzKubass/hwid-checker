import tkinter as tk
from tkinter import scrolledtext
import wmi
import uuid
import getpass
import platform
import winreg
import subprocess
import hashlib

def safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return f"Error: {e}"

def get_system_info():
    return f"PC Name: {platform.node()}\nOS: {platform.system()} {platform.release()} ({platform.version()})"

def get_machine_guid():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        guid, _ = winreg.QueryValueEx(key, "MachineGuid")
        return f"MachineGuid: {guid}"
    except Exception as e:
        return f"MachineGuid Error: {e}"

def get_windows_product_id():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion")
        value, _ = winreg.QueryValueEx(key, "ProductId")
        return f"Windows Product ID: {value}"
    except Exception as e:
        return f"Product ID Error: {e}"

def get_user_sid():
    try:
        username = getpass.getuser()
        result = subprocess.check_output(f'wmic useraccount where name="{username}" get sid', shell=True)
        lines = result.decode().splitlines()
        sid = [line.strip() for line in lines if line.strip() and "SID" not in line]
        return f"User SID: {sid[0] if sid else 'N/A'}"
    except Exception as e:
        return f"SID Error: {e}"

def get_all_mac_addresses():
    try:
        c = wmi.WMI()
        macs = []
        for nic in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            mac = nic.MACAddress
            desc = nic.Description
            if mac:
                macs.append(f"{mac} ({desc})")
        if macs:
            return "MAC Addresses:\n" + "\n".join(macs)
        else:
            return "No MAC Addresses found"
    except Exception as e:
        return f"MAC Error: {e}"

def get_cpu_info():
    try:
        c = wmi.WMI()
        cpus = []
        for cpu in c.Win32_Processor():
            cpus.append(f"CPU ID: {cpu.ProcessorId.strip()}\nName: {cpu.Name}\nManufacturer: {cpu.Manufacturer}\nMaxClockSpeed: {cpu.MaxClockSpeed} MHz")
        return "CPU Info:\n" + "\n\n".join(cpus)
    except Exception as e:
        return f"CPU Error: {e}"

def get_disk_info():
    try:
        c = wmi.WMI()
        disks = []
        for disk in c.Win32_DiskDrive():
            disks.append(
                f"Model: {disk.Model}\n"
                f"Serial: {disk.SerialNumber.strip() if disk.SerialNumber else 'N/A'}\n"
                f"InterfaceType: {disk.InterfaceType}\n"
                f"Size: {int(disk.Size)//(1024**3)} GB\n"
                f"MediaType: {getattr(disk, 'MediaType', 'N/A')}\n"
            )
        return "Disk Info:\n" + "\n---\n".join(disks)
    except Exception as e:
        return f"Disk Error: {e}"

def get_mb_info():
    try:
        c = wmi.WMI()
        boards = []
        for board in c.Win32_BaseBoard():
            boards.append(f"Manufacturer: {board.Manufacturer}\nProduct: {board.Product}\nSerial: {board.SerialNumber}")
        return "Motherboard Info:\n" + "\n---\n".join(boards)
    except Exception as e:
        return f"Motherboard Error: {e}"

def get_bios_info():
    try:
        c = wmi.WMI()
        bioses = []
        for bios in c.Win32_BIOS():
            bioses.append(f"Manufacturer: {bios.Manufacturer}\nVersion: {bios.SMBIOSBIOSVersion}\nSerial: {bios.SerialNumber}")
        return "BIOS Info:\n" + "\n---\n".join(bioses)
    except Exception as e:
        return f"BIOS Error: {e}"

def get_ram_info():
    try:
        c = wmi.WMI()
        rams = []
        for ram in c.Win32_PhysicalMemory():
            rams.append(f"Capacity: {int(ram.Capacity)//(1024**3)} GB\nManufacturer: {ram.Manufacturer}\nSpeed: {ram.Speed} MHz\nSerial: {ram.SerialNumber}")
        return "RAM Info:\n" + "\n---\n".join(rams)
    except Exception as e:
        return f"RAM Error: {e}"

def get_drivers_info():
    try:
        c = wmi.WMI()
        drivers = c.Win32_PnPSignedDriver()
        driver_list = []
        for d in drivers[:10]:
            driver_list.append(f"{d.DeviceName} | Provider: {d.DriverProviderName} | Version: {d.DriverVersion}")
        return "Sample Drivers Info (first 10):\n" + "\n".join(driver_list)
    except Exception as e:
        return f"Drivers Error: {e}"

def get_processes_info():
    try:
        c = wmi.WMI()
        procs = c.Win32_Process()
        proc_names = [p.Name for p in procs[:30]]
        return "Running Processes (first 30):\n" + ", ".join(proc_names)
    except Exception as e:
        return f"Processes Error: {e}"

def check_virtualization():
    try:
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        if "vmware" in bios.Manufacturer.lower() or "virtual" in bios.SerialNumber.lower():
            return "Virtualization Detected: VMware or Virtual Machine"
        else:
            return "Virtualization: Not detected"
    except Exception as e:
        return f"Virtualization Check Error: {e}"

def get_install_date():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        value, _ = winreg.QueryValueEx(key, "InstallDate")
        import datetime
        date = datetime.datetime.fromtimestamp(int(value))
        return f"Windows Install Date: {date.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        return f"Install Date Error: {e}"

def get_gpu_info():
    try:
        c = wmi.WMI()
        gpus = []
        for gpu in c.Win32_VideoController():
            gpus.append(f"Name: {gpu.Name}\nDriverVersion: {gpu.DriverVersion}\nVideoProcessor: {gpu.VideoProcessor}")
        return "GPU Info:\n" + "\n---\n".join(gpus)
    except Exception as e:
        return f"GPU Error: {e}"

def show_all_info():
    result_text.delete(1.0, tk.END)
    sections = [
        get_system_info(),
        get_machine_guid(),
        get_windows_product_id(),
        get_install_date(),
        get_user_sid(),
        get_all_mac_addresses(),
        get_cpu_info(),
        get_disk_info(),
        get_mb_info(),
        get_bios_info(),
        get_ram_info(),
        get_gpu_info(),
        get_drivers_info(),
        get_processes_info(),
        check_virtualization(),
    ]
    result_text.insert(tk.END, "\n\n---\n\n".join(sections))

window = tk.Tk()
window.title("HWID Checker")
window.geometry("700x700")
window.resizable(True, True)

label = tk.Label(window, text="Complete System HWID & Info Collector", font=("Segoe UI", 16, "bold"))
label.pack(pady=10)

result_text = scrolledtext.ScrolledText(window, width=85, height=35, font=("Courier New", 9))
result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

check_button = tk.Button(window, text="Load Full System Info", command=show_all_info, font=("Segoe UI", 11))
check_button.pack(pady=5)

window.mainloop()
