# Security Policy

## Supported Versions

Only the latest release is supported with security updates.

| Version | Supported |
| --- | --- |
| 2.2.x | ✅ |
| < 2.2 | ❌ |

## Reporting a Vulnerability

Please do **not** open a public issue for security problems. Report them
privately instead:

- Open a GitHub issue with the label `security` and mark it as sensitive if
  you can, or
- Email rkriad585@gmail.com with the subject `[SECURITY]` and include:
  - the version affected,
  - a description of the vulnerability,
  - steps to reproduce, and
  - any suggested fix, if you have one.

You should receive an acknowledgment within a few days. Once the issue is
confirmed, we will prepare a fix, publish a release, and credit the reporter
unless they prefer to remain anonymous.

## Security notes for this tool

- ActiveVPN only reads system information and makes outbound HTTPS/HTTP
  requests to the public IP/DNS APIs listed in `config.py`. It does not
  collect or transmit anything beyond what those endpoints return.
- Scan history is stored locally in plain text in your platform's data
  directory. Treat it as privacy-sensitive and avoid committing it.
- `--kill` and `--kill-force` require elevated privileges and will terminate
  processes matched by `VPN_PROCESS_NAMES`. Review that list in your config
  before running it in shared environments.
