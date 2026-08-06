# ActiveVPN/config.py
import json
import os

# --- Application Info ---
APP_NAME = "ActiveVPN"
VERSION = "2.2.1"
AUTHOR = "rkriad585"

# --- Paths ---
LOG_FILE = ".scan_history.json"
CONFIG_FILE = os.environ.get("ACTIVEVPN_CONFIG", ".activevpn.json")

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


def _load_config_overrides():
    """Load user overrides from a JSON config file, if present."""
    if not os.path.isfile(CONFIG_FILE):
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            overrides = json.load(f)
        if not isinstance(overrides, dict):
            return {}
        return overrides
    except (json.JSONDecodeError, IOError, UnicodeDecodeError):
        return {}


def _apply_overrides(overrides):
    """Apply string/list config overrides onto module globals."""
    for key, value in overrides.items():
        if not key.isupper() or not isinstance(key, str):
            continue
        current = globals().get(key)
        if isinstance(current, list) and isinstance(value, list):
            globals()[key] = value
        elif isinstance(current, str) and isinstance(value, str):
            globals()[key] = value
        elif isinstance(current, bool) and isinstance(value, bool):
            globals()[key] = value


_apply_overrides(_load_config_overrides())
