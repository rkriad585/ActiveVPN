# Architecture

How ActiveVPN is organized under the hood.

## In this guide

- [File layout](#file-layout)
- [Module responsibilities](#module-responsibilities)
- [Scan flow](#scan-flow)
- [Verdict scoring](#verdict-scoring)
- [History and export](#history-and-export)
- [Using as a library](#using-as-a-library)

## File layout

```
ActiveVPN/
├── main.py               # Entry point + CLI (argparse) + rich TUI rendering
├── config.py             # Legacy shim → re-exports activevpn.config
├── pyproject.toml        # Packaging, metadata, console script
├── requirements.txt      # Runtime dependencies
├── activevpn/            # The library (importable as a package)
│   ├── __init__.py       # Public API exports
│   ├── config.py         # Config dataclass, platformdirs paths, load_config()
│   ├── detector.py       # NetworkDetector + typed data model
│   ├── logger.py         # History persistence and export helpers
│   ├── logo.py           # ASCII banner generation (pyfiglet + rich)
│   └── help.py           # Help menu rendering
├── core/                 # Backward-compatible shim (deprecated, use activevpn)
├── tests/                # pytest suite (mocked psutil/requests)
├── logo/                 # Brand logo
└── docs/                 # Documentation
```

## Module responsibilities

| Module | Responsibility |
| --- | --- |
| `main.py` | Parses CLI flags, orchestrates the scan, renders tables/panels with `rich`, returns exit codes. |
| `activevpn/config.py` | Defines the typed `Config` dataclass and the user-facing paths via `platformdirs`: config at `~/.config/neostore/ActiveVPN/config.json` (Linux), `%LOCALAPPDATA%\neostore\ActiveVPN` (Windows), `~/Library/Application Support/neostore/ActiveVPN` (macOS). `load_config()` merges defaults + file overrides + inline overrides. |
| `activevpn/detector.py` | `NetworkDetector` checks interfaces (`check_interfaces`), processes (`check_processes`), public IP with API failover (`get_public_ip_info`), DNS resolver (`check_dns_leak`), IPv4/IPv6 (`get_ipv4`/`get_ipv6`), computes the verdict (`_compute_verdict`), and kills VPN processes (`kill_vpn_services`). Exposes the typed model `ScanResult` / `Verdict` / `IPInfo` / `DNSInfo` / `ProcessInfo`, a one-shot `scan()` function, and a `watch()` generator with callbacks. |
| `activevpn/logger.py` | Appends scans to the history JSON (in the data dir), loads history, clears it, and exports to JSON/CSV/TXT. `save_log()` accepts either a `ScanResult` or a dict. |
| `activevpn/logo.py` | Renders the pyfiglet banner inside a `rich` panel. |
| `activevpn/help.py` | Renders the help menu and exit-code table. |
| `core/` | Deprecated shim that re-exports `activevpn.*` for backward compatibility. |

## Scan flow

```text
run()                          # main.py
 ├─ print_banner()             # activevpn/logo.py
 ├─ NetworkDetector(console)   # activevpn/detector.py
 ├─ scan_network()
 │   ├─ check_interfaces()     # psutil.net_if_addrs() vs vpn_interface_patterns
 │   ├─ check_processes()      # psutil.process_iter() vs vpn/tor_process_names
 │   ├─ get_public_ip_info()   # tries ip_api_urls in order until one succeeds
 │   ├─ check_dns_leak()       # edns.ip-api.com
 │   ├─ get_ipv4() / get_ipv6()# api.ipify.org / api6.ipify.org
 │   └─ _compute_verdict()     # weighted score + label
 ├─ save_log()                 # activevpn/logger.py
 └─ display tables/panels      # main.py (rich)
```

## Verdict scoring

`_compute_verdict()` sums weights from the active `Config` (defaults in `activevpn/config.py`):

| Signal | Weight |
| --- | --- |
| VPN interface detected | 50 |
| VPN process(es) running | 40 |
| Tor process detected | 35 |
| IP flagged as `hosting` | 25 |
| IP flagged as `proxy` | 30 |

The score is capped at 100 and mapped to a label:

| Score | Label |
| --- | --- |
| 75&ndash;100 | `VPN DETECTED` |
| 40&ndash;74 | `LIKELY VPN/PROXY` |
| 20&ndash;39 | `SUSPICIOUS` |
| 0&ndash;19 | `CLEAN` |

## History and export

Every scan is appended to `scan_history.json` in the platform data directory (`~/.local/share/neostore/ActiveVPN/` on Linux, `%LOCALAPPDATA%\neostore\ActiveVPN\` on Windows). `activevpn/logger.py` flattens each entry into CSV/TXT/JSON rows for `--export` and renders the table for `--history`.

## Using as a library

```python
import activevpn

result = activevpn.scan(console=None)          # silent one-shot scan
result.verdict.label                           # -> "CLEAN"
result.to_json()                               # serializable dict/JSON

cfg = activevpn.load_config()                  # merge file overrides
cfg.vpn_process_names.append("my-vpn-daemon")

detector = activevpn.NetworkDetector(console=None, config=cfg)
for r in detector.watch(interval=30, on_change=lambda r: print(r.verdict.label)):
    ...
```

---

<a href="../README.md">← Back to README</a>
