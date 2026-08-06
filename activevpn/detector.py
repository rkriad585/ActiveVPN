# ActiveVPN/activevpn/detector.py
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import psutil
import requests

from activevpn.config import Config, load_config

API_TIMEOUT = 5


@dataclass
class ProcessInfo:
    """A running process that matched a VPN/Tor pattern."""
    pid: int
    name: str


@dataclass
class IPInfo:
    """Details about the external (public) IP address."""
    query: Optional[str] = None
    ip: Optional[str] = None
    isp: Optional[str] = None
    org: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    hosting: Optional[bool] = None
    proxy: Optional[bool] = None
    source: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def address(self) -> str:
        return self.query or self.ip or "?"

    @property
    def provider(self) -> str:
        return self.isp or self.org or ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "ip": self.ip,
            "isp": self.isp,
            "org": self.org,
            "country": self.country,
            "countryCode": self.country_code,
            "city": self.city,
            "region": self.region,
            "hosting": self.hosting,
            "proxy": self.proxy,
            "source": self.source,
            "raw": self.raw,
        }


@dataclass
class DNSInfo:
    """Info about the DNS resolver currently in use."""
    ip: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"ip": self.ip, "raw": self.raw}


@dataclass
class Verdict:
    """Overall confidence score and label for the current scan."""
    score: int = 0
    label: str = "CLEAN"
    reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"score": self.score, "label": self.label, "reasons": self.reasons}


@dataclass
class ScanResult:
    """Full result of one network scan. Serializable and copy-safe."""
    interfaces: List[str] = field(default_factory=list)
    vpn_processes: List[ProcessInfo] = field(default_factory=list)
    tor_processes: List[ProcessInfo] = field(default_factory=list)
    public_ip: Optional[IPInfo] = None
    dns_leak: Optional[DNSInfo] = None
    ipv4: Optional[str] = None
    ipv6: Optional[str] = None
    verdict: Verdict = field(default_factory=Verdict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "interfaces": self.interfaces,
            "vpn_processes": [{"pid": p.pid, "name": p.name} for p in self.vpn_processes],
            "tor_processes": [{"pid": p.pid, "name": p.name} for p in self.tor_processes],
            "public_ip": self.public_ip.to_dict() if self.public_ip else None,
            "dns_leak": self.dns_leak.to_dict() if self.dns_leak else None,
            "ipv4": self.ipv4,
            "ipv6": self.ipv6,
            "verdict": self.verdict.to_dict(),
        }

    def to_json(self) -> str:
        """Serialize this result to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)


class NetworkDetector:
    """Scans the system for VPN/Tor indicators and computes a verdict.

    :param console: optional ``rich`` Console for output. Pass ``None`` to run
        silently as a library (no terminal UI, no prints).
    :param debug: enable verbose debug logging (printed via console).
    :param config: a :class:`activevpn.config.Config`. Defaults to
        :func:`activevpn.config.load_config`.
    """

    def __init__(self, console=None, debug: bool = False, config: Optional[Config] = None):
        self.console = console
        self.debug = debug
        self.config = config or load_config()

    # --- helpers ---

    def _print(self, message: str = ""):
        if self.console is not None:
            self.console.print(message)

    def _debug(self, message):
        if self.debug:
            self._print(f"[dim][debug][/] {message}")

    # --- system checks ---

    def check_interfaces(self) -> List[str]:
        """Checks network interfaces for VPN signatures."""
        found: List[str] = []
        try:
            stats = psutil.net_if_addrs()
            for nic_name in stats.keys():
                for pattern in self.config.vpn_interface_patterns:
                    if pattern in nic_name.lower():
                        found.append(nic_name)
                        break
        except Exception as e:
            self._print(f"[{self.config.color_danger}]Error scanning interfaces: {e}[/]")
        return found

    @staticmethod
    def _process_matches(target, name, cmdline) -> bool:
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

    def check_processes(self, target_list: List[str]) -> List[ProcessInfo]:
        """Checks running processes against a target list."""
        found: List[ProcessInfo] = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    info = proc.info
                    name = (info['name'] or '').replace('.exe', '')
                    cmdline = ' '.join(info['cmdline'] or [])
                    for target in target_list:
                        if self._process_matches(target, name, cmdline):
                            found.append(ProcessInfo(pid=info['pid'], name=info['name']))
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass  # Suppress permission errors for cleaner output
        return found

    # --- online checks ---

    def get_public_ip_info(self) -> Optional[IPInfo]:
        """
        Fetches Public IP details to determine ISP/Location.
        Tries multiple APIs in order and returns the first successful result.
        Returns IPInfo or None if offline.
        """
        for url in self.config.ip_api_urls:
            try:
                self._debug(f"Fetching public IP info from {url}")
                response = requests.get(url, timeout=API_TIMEOUT)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict):
                        query = data.get("query") or data.get("ip")
                        if query:
                            return IPInfo(
                                query=query,
                                ip=data.get("ip", query),
                                isp=data.get("isp") or data.get("org"),
                                org=data.get("org"),
                                country=data.get("country"),
                                country_code=data.get("countryCode"),
                                city=data.get("city"),
                                region=data.get("region"),
                                hosting=data.get("hosting"),
                                proxy=data.get("proxy"),
                                source=url,
                                raw=data,
                            )
            except requests.RequestException as e:
                self._debug(f"{url} failed: {e}")
                continue
        return None

    def check_dns_leak(self) -> Optional[DNSInfo]:
        """
        Checks the DNS resolver IP.
        If the DNS IP ISP is different from the Public IP ISP, it notes it.
        """
        try:
            response = requests.get(self.config.dns_leak_api_url, timeout=API_TIMEOUT)
            if response.status_code == 200:
                data = response.json().get("dns", {})
                return DNSInfo(ip=data.get("ip"), raw=data)
        except requests.RequestException:
            return None
        return None

    def get_ipv4(self) -> Optional[str]:
        """Fetches the external IPv4 address, or None."""
        for url in self.config.ipv4_urls:
            try:
                response = requests.get(url, timeout=API_TIMEOUT)
                if response.status_code == 200:
                    return response.text.strip()
            except requests.RequestException:
                continue
        return None

    def get_ipv6(self) -> Optional[str]:
        """Fetches the external IPv6 address, or None (no IPv6 connectivity)."""
        for url in self.config.ipv6_urls:
            try:
                response = requests.get(url, timeout=API_TIMEOUT)
                if response.status_code == 200 and response.text.strip():
                    return response.text.strip()
            except requests.RequestException:
                continue
        return None

    # --- scan orchestration ---

    def scan_network(self) -> ScanResult:
        """Performs the full scan: System, IP, and DNS."""
        result = ScanResult(
            interfaces=self.check_interfaces(),
            vpn_processes=self.check_processes(self.config.vpn_process_names),
            tor_processes=self.check_processes(self.config.tor_process_names),
            public_ip=self.get_public_ip_info(),
            dns_leak=self.check_dns_leak(),
            ipv4=self.get_ipv4(),
            ipv6=self.get_ipv6(),
        )
        result.verdict = self._compute_verdict(result)
        return result

    def _compute_verdict(self, results: ScanResult) -> Verdict:
        """Combine all signals into a confidence score and label."""
        score = 0
        reasons: List[str] = []

        if results.interfaces:
            score += self.config.score_interface
            reasons.append("VPN interface detected")

        if results.vpn_processes:
            score += self.config.score_vpn_process
            reasons.append(f"{len(results.vpn_processes)} VPN process(es)")

        if results.tor_processes:
            score += self.config.score_tor_process
            reasons.append("Tor process detected")

        ip_data = results.public_ip
        if ip_data:
            if ip_data.hosting:
                score += self.config.score_hosting
                reasons.append("Hosting/datacenter IP")
            if ip_data.proxy:
                score += self.config.score_proxy
                reasons.append("Proxy/VPN flagged by provider")

        if score >= 75:
            label = "VPN DETECTED"
        elif score >= 40:
            label = "LIKELY VPN/PROXY"
        elif score >= 20:
            label = "SUSPICIOUS"
        else:
            label = "CLEAN"

        return Verdict(score=min(score, 100), label=label, reasons=reasons)

    # --- watch mode (library-friendly) ---

    def watch(
        self,
        interval: float = 10.0,
        on_scan: Optional[Callable[[ScanResult], Any]] = None,
        on_change: Optional[Callable[[ScanResult], Any]] = None,
    ):
        """Continuously scan, yielding each :class:`ScanResult`.

        :param interval: seconds between scans.
        :param on_scan: callback invoked after every scan.
        :param on_change: callback invoked only when the verdict label changes
            from the previous scan (handy for VPN-drop alerts).
        Usage::

            for result in detector.watch(interval=30, on_change=lambda r: print(r.verdict)):
                ...
        """
        previous_label: Optional[str] = None
        while True:
            try:
                result = self.scan_network()
            except KeyboardInterrupt:
                return

            if callable(on_scan):
                on_scan(result)
            if callable(on_change) and previous_label is not None and result.verdict.label != previous_label:
                on_change(result)
            previous_label = result.verdict.label

            yield result

            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                return

    # --- kill mode ---

    def kill_vpn_services(self, force: bool = False):
        """Attempts to terminate running VPN processes."""
        vpn_procs = self.check_processes(self.config.vpn_process_names)
        if not vpn_procs:
            self._print(f"[{self.config.color_warning}]No active VPN processes found to kill.[/]")
            return

        self._print(f"[bold]Attempting to terminate {len(vpn_procs)} processes...[/]")
        for proc_info in vpn_procs:
            pid = proc_info.pid
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait(timeout=3)
            except (psutil.TimeoutExpired, psutil.AccessDenied, psutil.NoSuchProcess):
                if force:
                    try:
                        proc.kill()
                        self._print(
                            f"[{self.config.color_success}]Force-killed: {proc_info.name} (PID: {pid})[/]"
                        )
                        continue
                    except Exception as e:
                        self._print(
                            f"[{self.config.color_danger}]Failed to force-kill {proc_info.name}: {e}[/]"
                        )
                        continue
                self._print(
                    f"[{self.config.color_warning}]Could not stop {proc_info.name} (PID: {pid}). "
                    f"Use --kill-force.[/]"
                )
                continue
            except Exception as e:
                self._print(f"[{self.config.color_danger}]Failed to kill {proc_info.name}: {e}[/]")
                continue
            self._print(f"[{self.config.color_success}]Terminated: {proc_info.name} (PID: {pid})[/]")


def scan(config: Optional[Config] = None, console=None, debug: bool = False) -> ScanResult:
    """One-shot convenience API.

    Runs a full scan without building a detector yourself::

        import activevpn
        result = activevpn.scan()
        print(result.verdict.label, result.verdict.score)
    """
    return NetworkDetector(console=console, debug=debug, config=config).scan_network()
