# Configuration

Tune ActiveVPN without touching the code.

## In this guide

- [Config file location](#config-file-location)
- [Overridable settings](#overridable-settings)
- [Environment variable](#environment-variable)
- [Scoring weights](#scoring-weights)

## Config file location

ActiveVPN stores its config under the `neostore` namespace in your platform's user config directory:

| Platform | Path |
| --- | --- |
| Linux | `~/.config/neostore/ActiveVPN/config.toml` |
| macOS | `~/Library/Application Support/neostore/ActiveVPN/config.toml` |
| Windows | `%LOCALAPPDATA%\neostore\ActiveVPN\config.toml` |

The file is auto-discovered on every run; you don't need to create it. Keys may use either the lowercase field names below or the legacy **uppercase constant names** from `config.py`. Supported value types are strings, lists, integers, and booleans.

Example `config.toml`:

```toml
vpn_interface_patterns = ["tun", "tap", "wg"]
vpn_process_names = ["openvpn", "mullvad", "nordvpn"]
color_success = "bold cyan"
```

A legacy `.activevpn.json` in the current working directory is still honored as a last resort (deprecated); existing JSON files load through a compatibility fallback.

## Overridable settings

| Constant | Type | Default | Purpose |
| --- | --- | --- | --- |
| `VPN_INTERFACE_PATTERNS` | list | `["tun", "tap", "ppp", ...]` | Substrings matched against network interface names. |
| `VPN_PROCESS_NAMES` | list | `["openvpn", "wireguard", ...]` | Process names/CLI tokens treated as VPN signals. |
| `TOR_PROCESS_NAMES` | list | `["tor", "tor.exe", "vidalia"]` | Tor-related process names. |
| `IP_API_URLS` | list | 3 URLs | Public IP/ISP endpoints, tried in order. |
| `DNS_LEAK_API_URL` | string | `https://edns.ip-api.com/json` | DNS resolver endpoint. |
| `IPV4_URLS` / `IPV6_URLS` | list | ipify / ipv6-test | IPv4 and IPv6 detection endpoints. |
| `COLOR_SUCCESS` etc. | string | `bold green` | `rich` styles used in the UI. |
| `LOG_FILE` | string | `scan_history.json` in the data dir | Where scan history is stored. |

## Environment variable

The config file path can be set with the `ACTIVEVPN_CONFIG` environment variable:

```bash
ACTIVEVPN_CONFIG=/etc/activevpn/config.toml activevpn
```

## Scoring weights

The verdict score is the sum of the weights below (capped at 100). They can be overridden from the config file as well.

| Constant | Default | Signal |
| --- | --- | --- |
| `SCORE_INTERFACE` | `50` | VPN interface detected |
| `SCORE_VPN_PROCESS` | `40` | VPN process running |
| `SCORE_TOR_PROCESS` | `35` | Tor process running |
| `SCORE_HOSTING` | `25` | IP flagged as hosting/datacenter |
| `SCORE_PROXY` | `30` | IP flagged as proxy/VPN |

---

<a href="../">← Back to Home</a>
