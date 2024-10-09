import os
import platform
import psutil
import sys
import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_info = response.json()
        return ip_info['ip']
    except requests.RequestException as e:
        return f"Error retrieving public IP: {e}"

def gather_system_info():
    system_info = {}

    # OS module information
    system_info['Current Working Directory'] = os.getcwd()
    system_info['Files and Directories'] = os.listdir()
    system_info['Environment Variables'] = dict(os.environ)
    system_info['Process ID'] = os.getpid()
    system_info['Parent Process ID'] = os.getppid()

    if hasattr(os, 'getuid'):
        system_info['User ID'] = os.getuid()
    if hasattr(os, 'geteuid'):
        system_info['Effective User ID'] = os.geteuid()
    if hasattr(os, 'getgid'):
        system_info['Group ID'] = os.getgid()
    if hasattr(os, 'getegid'):
        system_info['Effective Group ID'] = os.getegid()

    # Platform module information
    system_info['System/OS Name'] = platform.system()
    system_info['Node Name'] = platform.node()
    system_info['OS Release'] = platform.release()
    system_info['OS Version'] = platform.version()
    system_info['Machine Type'] = platform.machine()
    system_info['Processor Type'] = platform.processor()
    system_info['Full Platform Info'] = platform.platform()
    system_info['Python Version'] = platform.python_version()

    # PSUtil module information
    system_info['CPU Count'] = psutil.cpu_count(logical=True)
    system_info['CPU Usage'] = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    system_info['Total Memory'] = memory.total
    system_info['Available Memory'] = memory.available
    system_info['Used Memory'] = memory.used
    system_info['Memory Usage'] = memory.percent
    disk = psutil.disk_usage('/')
    system_info['Total Disk Space'] = disk.total
    system_info['Used Disk Space'] = disk.used
    system_info['Free Disk Space'] = disk.free
    system_info['Disk Usage'] = disk.percent
    net = psutil.net_if_addrs()
    system_info['Network Interfaces'] = {iface: [snic._asdict() for snic in addrs] for iface, addrs in net.items()}

    # Sys module information
    system_info['Python Version'] = sys.version
    system_info['Python Version Info'] = sys.version_info
    system_info['Platform'] = sys.platform
    system_info['Path'] = sys.path
    system_info['Executable'] = sys.executable
    system_info['Byte Order'] = sys.byteorder
    system_info['Recursion Limit'] = sys.getrecursionlimit()

    # Public IP
    system_info['Public IP'] = get_public_ip()

    return system_info

def print_system_info(system_info):
    for key, value in system_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    system_info = gather_system_info()
    print_system_info(system_info)
