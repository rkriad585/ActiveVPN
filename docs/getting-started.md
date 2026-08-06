# Getting Started

A quick tour of ActiveVPN: install it, run your first scan, and read the result.

## In this guide

- [Install](#install)
- [Run your first scan](#run-your-first-scan)
- [Read the output](#read-the-output)
- [Next steps](#next-steps)

## Install

```bash
pip install activevpn
```

Prefer installing from source? See [installation.md](installation.md).

## Run your first scan

```bash
activevpn
```

The tool checks your network interfaces, running processes, public IP, and DNS routing. A scan normally completes in a few seconds.

## Read the output

The scan prints four sections:

1. **System Internal Check** — whether VPN/Tor interfaces or processes were found.
2. **External IP Analysis** — your public IP, country, ISP, and whether it looks like a datacenter.
3. **DNS Consistency Check** — whether your DNS resolver IP matches your traffic IP.
4. **Overall Verdict** — a confidence score (`0`&ndash;`100`) and a label: `CLEAN`, `SUSPICIOUS`, `LIKELY VPN/PROXY`, or `VPN DETECTED`.

Every scan is appended to `.scan_history.json`.

## Next steps

- Learn every flag in [cli.md](cli.md).
- Explore configuration in [configuration.md](configuration.md).
- Troubleshoot problems in [troubleshooting.md](troubleshooting.md).

---

<a href="../README.md">← Back to README</a>
