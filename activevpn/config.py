# ActiveVPN/activevpn/config.py
import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

import platformdirs

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import tomli_w

# --- Application Info ---
APP_NAME = "ActiveVPN"
ORG_NAME = "neostore"
VERSION = "2.4.0"
AUTHOR = "rkriad585"

# --- Paths ---
# Cross-platform user config/data directories.
#   Linux:  ~/.config/neostore/ActiveVPN   and   ~/.local/share/neostore/ActiveVPN
#   macOS:  ~/Library/Application Support/neostore/ActiveVPN
#   Windows: %LOCALAPPDATA%\neostore\ActiveVPN
CONFIG_DIR = platformdirs.user_config_dir(APP_NAME, ORG_NAME)
DATA_DIR = platformdirs.user_data_dir(APP_NAME, ORG_NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")
LOG_FILE = os.path.join(DATA_DIR, "scan_history.json")

# Legacy location kept for backward compatibility.
LEGACY_CONFIG_FILE = ".activevpn.json"

# --- Detection Patterns ---
VPN_INTERFACE_PATTERNS = [
    "tun", "tap", "ppp", "utun", "wg", "ipsec",
    "proton", "nord", "express", "tailscale", "zerotier"
]

VPN_PROCESS_NAMES = [
    "openvpn", "wireguard", "nordvpn", "expressvpn",
    "protonvpn", "surfshark", "mullvad", "pia-service", "tailscaled",
    "globalprotect", "cisco anyconnect"
]

TOR_PROCESS_NAMES = ["tor", "tor.exe", "vidalia"]

# --- External APIs ---
# Used to check Public IP and ISP info (queried in order until one succeeds)
IP_API_URLS = [
    "http://ip-api.com/json/",
    "https://ipinfo.io/json",
    "https://ipapi.co/json/",
]

# Used to check which IP is actually resolving DNS queries
DNS_LEAK_API_URL = "https://edns.ip-api.com/json"

# Used to fetch IPv4/IPv6 addresses independently (IPv6 leak detection)
IPV4_URLS = [
    "https://api.ipify.org",
    "https://api4.ipify.org",
]

IPV6_URLS = [
    "https://api6.ipify.org",
    "http://v6.ipv6-test.com/api/myip.php",
]

# --- UI Colors ---
COLOR_SUCCESS = "bold green"
COLOR_WARNING = "bold yellow"
COLOR_DANGER = "bold red"
COLOR_INFO = "cyan"
COLOR_TITLE = "bold magenta"

# --- Verdict Scoring ---
SCORE_INTERFACE = 50
SCORE_VPN_PROCESS = 40
SCORE_TOR_PROCESS = 35
SCORE_HOSTING = 25
SCORE_PROXY = 30


@dataclass
class Config:
    """Typed, overridable ActiveVPN settings.

    Every field maps to one of the uppercase constants above, so the JSON
    config file can override any of them by key name.
    """
    vpn_interface_patterns: List[str] = field(default_factory=lambda: list(VPN_INTERFACE_PATTERNS))
    vpn_process_names: List[str] = field(default_factory=lambda: list(VPN_PROCESS_NAMES))
    tor_process_names: List[str] = field(default_factory=lambda: list(TOR_PROCESS_NAMES))
    ip_api_urls: List[str] = field(default_factory=lambda: list(IP_API_URLS))
    dns_leak_api_url: str = DNS_LEAK_API_URL
    ipv4_urls: List[str] = field(default_factory=lambda: list(IPV4_URLS))
    ipv6_urls: List[str] = field(default_factory=lambda: list(IPV6_URLS))
    color_success: str = COLOR_SUCCESS
    color_warning: str = COLOR_WARNING
    color_danger: str = COLOR_DANGER
    color_info: str = COLOR_INFO
    color_title: str = COLOR_TITLE
    score_interface: int = SCORE_INTERFACE
    score_vpn_process: int = SCORE_VPN_PROCESS
    score_tor_process: int = SCORE_TOR_PROCESS
    score_hosting: int = SCORE_HOSTING
    score_proxy: int = SCORE_PROXY
    log_file: str = LOG_FILE
    config_file: str = CONFIG_FILE

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Build a Config from raw dict, coercing keys to field names.

        Accepts both snake_case field names and the legacy uppercase constant
        names used by the old JSON config file.
        """
        mapping = {
            "VPN_INTERFACE_PATTERNS": "vpn_interface_patterns",
            "VPN_PROCESS_NAMES": "vpn_process_names",
            "TOR_PROCESS_NAMES": "tor_process_names",
            "IP_API_URLS": "ip_api_urls",
            "DNS_LEAK_API_URL": "dns_leak_api_url",
            "IPV4_URLS": "ipv4_urls",
            "IPV6_URLS": "ipv6_urls",
            "COLOR_SUCCESS": "color_success",
            "COLOR_WARNING": "color_warning",
            "COLOR_DANGER": "color_danger",
            "COLOR_INFO": "color_info",
            "COLOR_TITLE": "color_title",
            "SCORE_INTERFACE": "score_interface",
            "SCORE_VPN_PROCESS": "score_vpn_process",
            "SCORE_TOR_PROCESS": "score_tor_process",
            "SCORE_HOSTING": "score_hosting",
            "SCORE_PROXY": "score_proxy",
            "LOG_FILE": "log_file",
            "CONFIG_FILE": "config_file",
        }
        clean: Dict[str, Any] = {}
        for key, value in data.items():
            if key in mapping:
                clean[mapping[key]] = value
            elif key in cls.__dataclass_fields__:
                clean[key] = value
        return cls(**clean)


def resolve_config_path(custom: Optional[str] = None) -> Optional[str]:
    """Resolve which config file to load, by priority:

    1. ``$ACTIVEVPN_CONFIG`` environment variable (explicit path)
    2. ``~/.config/neostore/ActiveVPN/config.toml`` (or platform equivalent)
    3. Legacy ``.activevpn.json`` in the current directory (deprecated)

    Returns None when no config file exists.
    """
    if custom:
        return custom if os.path.isfile(custom) else None

    env_path = os.environ.get("ACTIVEVPN_CONFIG")
    if env_path and os.path.isfile(env_path):
        return env_path

    if os.path.isfile(CONFIG_FILE):
        return CONFIG_FILE

    if os.path.isfile(LEGACY_CONFIG_FILE):
        return LEGACY_CONFIG_FILE

    return None


def _parse_config_text(text: str) -> Dict[str, Any]:
    """Parse config text as TOML, falling back to legacy JSON syntax."""
    try:
        data = tomllib.loads(text)
        if isinstance(data, dict):
            return data
    except ValueError:
        pass  # Not valid TOML; try legacy JSON below.
    try:
        data = json.loads(text)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def load_config_file(path: Optional[str] = None) -> Dict[str, Any]:
    """Load raw overrides from a TOML config file (legacy JSON also accepted).
    Returns {} on any failure."""
    resolved = resolve_config_path(path)
    if resolved is None:
        return {}

    try:
        with open(resolved, "r", encoding="utf-8") as f:
            text = f.read()
        return _parse_config_text(text)
    except (IOError, UnicodeDecodeError):
        return {}


def load_config(custom: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None) -> Config:
    """Build a Config from defaults + file overrides + explicit overrides.

    :param custom: explicit config file path (takes priority over discovery)
    :param overrides: inline overrides dict (highest priority)
    """
    data: Dict[str, Any] = {}
    if custom:
        data.update(load_config_file(custom))
    else:
        data.update(load_config_file())
    if overrides:
        data.update(overrides)
    return Config.from_dict(data)


def save_config(config: Config, path: Optional[str] = None) -> str:
    """Persist a Config to disk as TOML. Returns the path written."""
    target = path or config.config_file or CONFIG_FILE
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "wb") as f:
        tomli_w.dump(config.to_dict(), f)
    return target
