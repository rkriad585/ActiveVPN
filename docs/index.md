# ActiveVPN

<p align="center">
  <img src="assets/logo.svg" alt="ActiveVPN logo" height="150">
</p>

**The Ultimate Network Privacy & VPN Detection Tool.**

ActiveVPN inspects your system's network interfaces, analyzes running processes, checks your external IP against known hosting providers, and performs DNS leak tests &mdash; all in one hacker-style terminal UI. It tells you whether your VPN is *actually* working.

## Key Features

- **Deep scan** &mdash; detects VPNs via interface names, process names, and IP reputation in one pass.
- **Tor detection** &mdash; specifically checks for active Tor services.
- **External IP analysis** &mdash; queries public IP APIs and flags datacenter/hosting/proxy IPs.
- **DNS leak detection** &mdash; compares your traffic IP with your DNS resolver IP.
- **IPv6 leak check** &mdash; reports your external IPv6 address and warns when IPv6 may leak around a tunnel.
- **Overall verdict** &mdash; combines every signal into a confidence score and a CLEAN / SUSPICIOUS / LIKELY VPN-PROXY / VPN DETECTED label.
- **Kill switch** &mdash; terminates active VPN processes, with a `--kill-force` fallback.
- **History & export** &mdash; automatically logs scans and exports them as JSON, CSV, or TXT.
- **Library API** &mdash; importable as a Python package with a typed `ScanResult`, silent mode, and watch callbacks.
- **Watch mode** &mdash; continuously re-scans at a configurable interval.
- **Configurable** &mdash; patterns, colors, and API endpoints can be overridden with a TOML config file.

## Quick Start

```bash
pip install activevpn
activevpn
```

## Documentation

- [Getting Started](getting-started.md)
- [Installation](installation.md)
- [Usage](usage.md)
- [CLI Reference](cli.md)
- [Configuration](configuration.md)
- [Architecture](architecture.md)
- [Development](development.md)
- [Deployment](deployment.md)
- [FAQ](faq.md)
- [Troubleshooting](troubleshooting.md)
- [Screenshots](screenshots.md)

---

Source code, the repository README, releases, and the issue tracker live on [GitHub](https://github.com/rkriad585/ActiveVPN).
