# CLI Reference

ActiveVPN is a command-line tool. It ships as the `activevpn` console script and can also be run with `python main.py`.

## In this guide

- [Synopsis](#synopsis)
- [Global behavior](#global-behavior)
- [Options](#options)
- [Exit codes](#exit-codes)

## Synopsis

```text
activevpn [-h] [-k] [--kill-force] [--history] [--clear-history]
          [--export [FORMAT]] [--watch [SECONDS]] [--debug]
```

## Global behavior

Run with no arguments to perform a full scan. The scan checks network interfaces, running processes, public IP and ISP reputation, IPv6, and DNS routing, then saves the result to the history file in your platform's data directory.

## Options

| Flag | Description |
| --- | --- |
| `-h`, `--help` | Show the help menu and exit. |
| `-k`, `--kill` | Attempt to gracefully terminate active VPN processes. Requires admin/root. |
| `--kill-force` | Like `--kill`, but sends `SIGKILL` when a graceful stop times out (3s). |
| `--history` | Show the last 20 saved scans as a table. |
| `--clear-history` | Delete the scan history file. |
| `--export [FORMAT]` | Export all history. `FORMAT` is `json` (default), `csv`, or `txt`. Writes `activevpn_export_<timestamp>.<format>`. |
| `--watch [SECONDS]` | Continuously rescan every `SECONDS` (default `10`). Press `Ctrl+C` to stop. |
| `--debug` | Print verbose diagnostics, including which API endpoints are attempted. |

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | No VPN detected, or clean exit (help, history, export, kill). |
| `1` | VPN / Tor / Proxy detected by the verdict. |
| `2` | Offline (public IP unavailable with no local signals), or invalid `--export` format. |

---

<a href="../README.md">← Back to README</a>
