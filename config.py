# vpnActive/config.py
import os

# --- Application Info ---
APP_NAME = "VPNActive"
VERSION = "2.1.0"
AUTHOR = "RK Riad Khan"

# --- Paths ---
LOG_FILE = ".scan_history.json"

# --- Detection Patterns ---
VPN_INTERFACE_PATTERNS = [
    "tun", "tap", "ppp", "utun", "wg", "ipsec", 
    "proton", "nord", "express", "tailscale", "zerotier"
]

VPN_PROCESS_NAMES = [
    "openvpn", "wireguard", "vpn", "nordvpn", "expressvpn", 
    "protonvpn", "surfshark", "mullvad", "pia-service", "tailscaled",
    "globalprotect", "cisco anyconnect"
]

TOR_PROCESS_NAMES = ["tor", "tor.exe", "vidalia"]

# --- External APIs ---
# Used to check Public IP and ISP info
IP_API_URL = "http://ip-api.com/json/"
# Used to check which IP is actually resolving DNS queries
DNS_LEAK_API_URL = "https://edns.ip-api.com/json"

# --- UI Colors ---
COLOR_SUCCESS = "bold green"
COLOR_WARNING = "bold yellow"
COLOR_DANGER = "bold red"
COLOR_INFO = "cyan"
COLOR_TITLE = "bold magenta"
