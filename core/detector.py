# ActiveVPN/core/detector.py
import time

import psutil
import requests
from rich.console import Console

from config import (
    VPN_INTERFACE_PATTERNS,
    VPN_PROCESS_NAMES,
    TOR_PROCESS_NAMES,
    IP_API_URLS,
    DNS_LEAK_API_URL,
    IPV4_URLS,
    IPV6_URLS,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SUCCESS,
    SCORE_INTERFACE,
    SCORE_VPN_PROCESS,
    SCORE_TOR_PROCESS,
    SCORE_HOSTING,
    SCORE_PROXY,
)

API_TIMEOUT = 5


class NetworkDetector:
    def __init__(self, console: Console, debug: bool = False):
        self.console = console
        self.debug = debug

    def _debug(self, message):
        if self.debug:
            self.console.print(f"[dim][debug][/] {message}")

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

    @staticmethod
    def _process_matches(target, name, cmdline):
        """Match a target against a process name and its command line.

        Uses exact/prefix matching on the binary name and CLI tokens to
        avoid the false positives caused by naive substring matching.
        """
        target = target.strip().lower()
        name = name.strip().lower()
        if isinstance(cmdline, (list, tuple)):
            cmdline = " ".join(cmdline)
        cmdline = cmdline.lower()

        if not target:
            return False

        # Multi-word targets (e.g. "cisco anyconnect") are matched word-wise
        # against the command line to avoid path separators breaking the match.
        if ' ' in target:
            return all(word in cmdline for word in target.split())

        for token in cmdline.split():
            base = token.rsplit('/', 1)[-1].lower()
            if base.endswith('.exe'):
                base = base[:-4]
            if base == target or base.startswith(target + '-') or base.startswith(target + '.'):
                return True
        return (name == target
                or name.startswith(target + '-')
                or name.startswith(target + '.'))

    def check_processes(self, target_list):
        """Checks running processes against a target list."""
        found = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    info = proc.info
                    name = (info['name'] or '').replace('.exe', '')
                    cmdline = ' '.join(info['cmdline'] or [])
                    for target in target_list:
                        if self._process_matches(target, name, cmdline):
                            found.append({'pid': info['pid'], 'name': info['name']})
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass  # Suppress permission errors for cleaner output
        return found

    def get_public_ip_info(self):
        """
        Fetches Public IP details to determine ISP/Location.
        Tries multiple APIs in order and returns the first successful result.
        Returns dict or None if offline.
        """
        for url in IP_API_URLS:
            try:
                self._debug(f"Fetching public IP info from {url}")
                response = requests.get(url, timeout=API_TIMEOUT)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and data.get("query"):
                        data["source"] = url
                        return data
                    if isinstance(data, dict) and data.get("ip"):
                        data["query"] = data["ip"]
                        data["source"] = url
                        return data
            except requests.RequestException as e:
                self._debug(f"{url} failed: {e}")
                continue
        return None

    def check_dns_leak(self):
        """
        Checks the DNS resolver IP.
        If the DNS IP ISP is different from the Public IP ISP, it notes it.
        """
        try:
            response = requests.get(DNS_LEAK_API_URL, timeout=API_TIMEOUT)
            if response.status_code == 200:
                return response.json().get("dns", {})
        except requests.RequestException:
            return None
        return None

    def get_ipv4(self):
        """Fetches the external IPv4 address, or None."""
        for url in IPV4_URLS:
            try:
                response = requests.get(url, timeout=API_TIMEOUT)
                if response.status_code == 200:
                    return response.text.strip()
            except requests.RequestException:
                continue
        return None

    def get_ipv6(self):
        """Fetches the external IPv6 address, or None (no IPv6 connectivity)."""
        for url in IPV6_URLS:
            try:
                response = requests.get(url, timeout=API_TIMEOUT)
                if response.status_code == 200 and response.text.strip():
                    return response.text.strip()
            except requests.RequestException:
                continue
        return None

    def scan_network(self):
        """Performs the full scan: System, IP, and DNS."""
        results = {
            "interfaces": [],
            "vpn_processes": [],
            "tor_processes": [],
            "public_ip": None,
            "dns_leak": None,
            "ipv4": None,
            "ipv6": None,
            "verdict": {"score": 0, "label": "CLEAN"},
        }

        # 1. System Scans
        results["interfaces"] = self.check_interfaces()
        results["vpn_processes"] = self.check_processes(VPN_PROCESS_NAMES)
        results["tor_processes"] = self.check_processes(TOR_PROCESS_NAMES)

        # 2. Online Scans
        results["public_ip"] = self.get_public_ip_info()
        results["dns_leak"] = self.check_dns_leak()
        results["ipv4"] = self.get_ipv4()
        results["ipv6"] = self.get_ipv6()

        results["verdict"] = self._compute_verdict(results)
        return results

    @staticmethod
    def _compute_verdict(results):
        """Combine all signals into a confidence score and label."""
        score = 0
        reasons = []

        if results.get("interfaces"):
            score += SCORE_INTERFACE
            reasons.append("VPN interface detected")

        if results.get("vpn_processes"):
            score += SCORE_VPN_PROCESS
            reasons.append(f"{len(results['vpn_processes'])} VPN process(es)")

        if results.get("tor_processes"):
            score += SCORE_TOR_PROCESS
            reasons.append("Tor process detected")

        ip_data = results.get("public_ip") or {}
        if ip_data.get("hosting"):
            score += SCORE_HOSTING
            reasons.append("Hosting/datacenter IP")
        if ip_data.get("proxy"):
            score += SCORE_PROXY
            reasons.append("Proxy/VPN flagged by provider")

        if score >= 75:
            label = "VPN DETECTED"
        elif score >= 40:
            label = "LIKELY VPN/PROXY"
        elif score >= 20:
            label = "SUSPICIOUS"
        else:
            label = "CLEAN"

        return {"score": min(score, 100), "label": label, "reasons": reasons}

    def kill_vpn_services(self, force: bool = False):
        """Attempts to terminate running VPN processes."""
        vpn_procs = self.check_processes(VPN_PROCESS_NAMES)
        if not vpn_procs:
            self.console.print(f"[{COLOR_WARNING}]No active VPN processes found to kill.[/]")
            return

        self.console.print(f"[bold]Attempting to terminate {len(vpn_procs)} processes...[/]")
        for proc_info in vpn_procs:
            pid = proc_info['pid']
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait(timeout=3)
            except (psutil.TimeoutExpired, psutil.AccessDenied, psutil.NoSuchProcess):
                if force:
                    try:
                        proc.kill()
                        self.console.print(
                            f"[{COLOR_SUCCESS}]Force-killed: {proc_info['name']} (PID: {pid})[/]"
                        )
                        continue
                    except Exception as e:
                        self.console.print(
                            f"[{COLOR_DANGER}]Failed to force-kill {proc_info['name']}: {e}[/]"
                        )
                        continue
                self.console.print(
                    f"[{COLOR_WARNING}]Could not stop {proc_info['name']} (PID: {pid}). "
                    f"Use --kill-force.[/]"
                )
                continue
            except Exception as e:
                self.console.print(f"[{COLOR_DANGER}]Failed to kill {proc_info['name']}: {e}[/]")
                continue
            self.console.print(f"[{COLOR_SUCCESS}]Terminated: {proc_info['name']} (PID: {pid})[/]")
