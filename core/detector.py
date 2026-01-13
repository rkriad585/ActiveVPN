# vpnActive/core/detector.py
import psutil
import requests
from rich.console import Console
from config import (
    VPN_INTERFACE_PATTERNS, 
    VPN_PROCESS_NAMES, 
    TOR_PROCESS_NAMES,
    IP_API_URL,
    DNS_LEAK_API_URL,
    COLOR_DANGER, COLOR_WARNING, COLOR_SUCCESS
)

class NetworkDetector:
    def __init__(self, console: Console):
        self.console = console

    def check_interfaces(self):
        """Checks network interfaces for VPN signatures."""
        found = []
        try:
            stats = psutil.net_if_addrs()
            for nic_name in stats.keys():
                for pattern in VPN_INTERFACE_PATTERNS:
                    if pattern in nic_name.lower():
                        found.append(nic_name)
                        break
        except Exception as e:
            self.console.print(f"[{COLOR_DANGER}]Error scanning interfaces: {e}[/]")
        return found

    def check_processes(self, target_list):
        """Checks running processes against a target list."""
        found = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    p_name = proc.info['name'].lower()
                    for target in target_list:
                        if target in p_name:
                            found.append({'pid': proc.info['pid'], 'name': proc.info['name']})
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass # Suppress permission errors for cleaner output
        return found

    def get_public_ip_info(self):
        """
        Fetches Public IP details to determine ISP/Location.
        Returns dict or None if offline.
        """
        try:
            response = requests.get(IP_API_URL, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            return None
        return None

    def check_dns_leak(self):
        """
        Checks the DNS resolver IP. 
        If the DNS IP ISP is different from the Public IP ISP, it notes it.
        """
        try:
            response = requests.get(DNS_LEAK_API_URL, timeout=5)
            if response.status_code == 200:
                return response.json().get("dns", {})
        except requests.RequestException:
            return None
        return None

    def scan_network(self):
        """Performs the full scan: System, IP, and DNS."""
        
        # 1. System Scans
        vpn_ifs = self.check_interfaces()
        vpn_procs = self.check_processes(VPN_PROCESS_NAMES)
        tor_procs = self.check_processes(TOR_PROCESS_NAMES)

        # 2. Online Scans
        ip_info = self.get_public_ip_info()
        dns_info = self.check_dns_leak()

        return {
            "interfaces": vpn_ifs,
            "vpn_processes": vpn_procs,
            "tor_processes": tor_procs,
            "public_ip": ip_info,
            "dns_leak": dns_info
        }

    def kill_vpn_services(self):
        """Attempts to terminate running VPN processes."""
        vpn_procs = self.check_processes(VPN_PROCESS_NAMES)
        if not vpn_procs:
            self.console.print(f"[{COLOR_WARNING}]No active VPN processes found to kill.[/]")
            return

        self.console.print(f"[bold]Attempting to terminate {len(vpn_procs)} processes...[/]")
        for proc_info in vpn_procs:
            try:
                psutil.Process(proc_info['pid']).terminate()
                self.console.print(f"[{COLOR_SUCCESS}]Terminated: {proc_info['name']} (PID: {proc_info['pid']})[/]")
            except Exception as e:
                self.console.print(f"[{COLOR_DANGER}]Failed to kill {proc_info['name']}: {e}[/]")
