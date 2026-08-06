# Usage

How to use ActiveVPN day to day.

## In this guide

- [Default scan](#default-scan)
- [Kill active VPNs](#kill-active-vpns)
- [History](#history)
- [Export](#export)
- [Watch mode](#watch-mode)
- [Debug mode](#debug-mode)
- [Exit codes](#exit-codes)

## Default scan

```bash
activevpn
```

Runs the full scan: interfaces, processes, Tor, public IP, IPv6, and DNS.

## Kill active VPNs

```bash
# Graceful terminate (requires admin/root)
activevpn --kill

# Graceful first, then SIGKILL if a process won't stop
activevpn --kill-force
```

On Linux/macOS prefix with `sudo`. On Windows run the terminal as Administrator.

## History

```bash
# Show the last 20 saved scans
activevpn --history

# Delete all saved history
activevpn --clear-history
```

History is stored in `scan_history.json` inside your platform's data directory.

## Export

```bash
# JSON (default)
activevpn --export

# CSV
activevpn --export csv

# Plain text
activevpn --export txt
```

Exports write `activevpn_export_<timestamp>.<format>` in the current directory.

## Watch mode

```bash
# Rescan every 10 seconds (default)
activevpn --watch

# Custom interval
activevpn --watch 30
```

Press `Ctrl+C` to stop.

## Debug mode

```bash
activevpn --debug
```

Prints extra diagnostics, such as which API endpoints were tried.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | No VPN detected (or clean exit) |
| `1` | VPN / Tor / Proxy detected |
| `2` | Offline, error, or invalid usage |

Useful for scripting:

```bash
if activevpn > /dev/null 2>&1; then
  echo "No VPN detected"
elif [ $? -eq 1 ]; then
  echo "VPN detected!"
fi
```

For the full flag reference, see [cli.md](cli.md).

---

<a href="../README.md">← Back to README</a>
