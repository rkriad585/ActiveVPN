# Architecture

How ActiveVPN is organized under the hood.

## In this guide

- [File layout](#file-layout)
- [Module responsibilities](#module-responsibilities)
- [Scan flow](#scan-flow)
- [Verdict scoring](#verdict-scoring)
- [History and export](#history-and-export)

## File layout

```
ActiveVPN/
├── main.py               # Entry point + CLI (argparse) + rich TUI rendering
├── config.py             # Settings: patterns, API URLs, colors, scoring
├── pyproject.toml        # Packaging, metadata, console script
├── requirements.txt      # Runtime dependencies
├── .scan_history.json    # Scan history log (auto-generated)
├── core/
│   ├── __init__.py       # Package marker
│   ├── logo.py           # ASCII banner generation (pyfiglet + rich)
│   ├── help.py           # Help menu rendering
│   ├── detector.py       # NetworkDetector: the main scanning logic
│   └── logger.py         # History persistence and export helpers
├── tests/                # pytest suite (mocked psutil/requests)
├── logo/                 # Brand logo
└── docs/                 # Documentation
```

## Module responsibilities

| Module | Responsibility |
| --- | --- |
| `main.py` | Parses CLI flags, orchestrates the scan, renders tables/panels with `rich`, returns exit codes. |
| `config.py` | Holds detection patterns, API endpoint lists, UI colors, and verdict scoring weights. Also loads user overrides from `.activevpn.json`. |
| `core/detector.py` | `NetworkDetector` checks interfaces (`check_interfaces`), processes (`check_processes`), public IP with API failover (`get_public_ip_info`), DNS resolver (`check_dns_leak`), IPv4/IPv6 (`get_ipv4`/`get_ipv6`), computes the verdict (`_compute_verdict`), and kills VPN processes (`kill_vpn_services`). |
| `core/logger.py` | Appends scans to `.scan_history.json`, loads history, clears it, and exports to JSON/CSV/TXT. |
| `core/logo.py` | Renders the pyfiglet banner inside a `rich` panel. |
| `core/help.py` | Renders the help menu and exit-code table. |

## Scan flow

```text
run()                          # main.py
 ├─ print_banner()             # core/logo.py
 ├─ NetworkDetector(console)   # core/detector.py
 ├─ scan_network()
 │   ├─ check_interfaces()     # psutil.net_if_addrs() vs VPN_INTERFACE_PATTERNS
 │   ├─ check_processes()      # psutil.process_iter() vs VPN/TOR_PROCESS_NAMES
 │   ├─ get_public_ip_info()   # tries IP_API_URLS in order until one succeeds
 │   ├─ check_dns_leak()       # edns.ip-api.com
 │   ├─ get_ipv4() / get_ipv6()# api.ipify.org / api6.ipify.org
 │   └─ _compute_verdict()     # weighted score + label
 ├─ save_log()                 # core/logger.py
 └─ display tables/panels      # main.py (rich)
```

## Verdict scoring

`_compute_verdict()` sums weights defined in `config.py`:

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

Every scan is appended to `.scan_history.json` with an ISO timestamp. `core/logger.py` flattens each entry into CSV/TXT/JSON rows for `--export` and renders the table for `--history`.

---

<a href="../README.md">← Back to README</a>
