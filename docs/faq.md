# FAQ

Frequently asked questions about ActiveVPN.

## What exactly does ActiveVPN detect?

It combines three layers: system inspection (VPN/Tor network interfaces and processes), external IP reputation (datacenter/hosting/proxy flags from IP lookup APIs), and DNS routing (whether your DNS resolver IP differs from your traffic IP). See [architecture.md](architecture.md).

## How reliable is the verdict?

The verdict is a weighted score of independent signals. Local signals (interfaces, processes) are strong; the IP reputation is a hint. Treat `LIKELY VPN/PROXY` and below as guidance, not proof.

## Can it be a false positive?

Yes. The IP-reputation check can flag legitimate datacenter or cloud-hosted residential IPs. Interface/process detection can miss exotic VPN clients. You can tune the pattern lists in the config file &mdash; see [configuration.md](configuration.md).

## What does "DNS matches Public IP" mean?

If your traffic IP and DNS resolver IP are identical, it usually means your DNS is handled locally or everything is wrapped inside the VPN tunnel. If they differ, DNS is resolved by a different server &mdash; standard for most VPNs, and not necessarily a leak.

## Why do I get exit code 2?

Exit code `2` means the scan could not reach the public IP APIs and found no local VPN signals &mdash; typically you are offline or the APIs are blocked. See [cli.md](cli.md) for all exit codes.

## Does it require root?

No, a normal scan does not. Only `--kill` and `--kill-force` require administrator/root privileges.

## Where is the history stored?

In `.scan_history.json` in the current working directory. Manage it with `--history`, `--export`, and `--clear-history`.

## Does it work on Android?

Yes, when run inside Termux. See [installation.md](installation.md).

## How do I make it match my VPN client?

Add your client's process name to `VPN_PROCESS_NAMES` or its interface prefix to `VPN_INTERFACE_PATTERNS` via the config file. See [configuration.md](configuration.md).

---

<a href="../README.md">← Back to README</a>
