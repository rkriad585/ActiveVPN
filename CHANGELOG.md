# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.1] - 2026-08-06

### Changed

- Rewrote the README and added a full `docs/` suite (getting started, installation, usage, CLI reference, configuration, architecture, development, deployment, FAQ, troubleshooting, screenshots).
- Added community and project standards: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `CONTRIBUTORS`, `CODEOWNERS`, `SECURITY.md`, `ACCESSIBILITY.md`, and a Keep-a-Changelog `CHANGELOG.md`.
- Added packaging extras: `Dockerfile`, `.dockerignore`, `.editorconfig`, `.gitattributes`, `.env.example`, and `.version`.
- Added a flat, dark-mode-safe brand logo at `logo/logo.svg`.
- Updated all repository URLs to `github.com/rkriad585/ActiveVPN`.

## [2.2.0] - 2026-08-06

### Added

- Project renamed from VPNActive to **ActiveVPN**.
- Overall verdict with confidence score and `CLEAN` / `SUSPICIOUS` / `LIKELY VPN/PROXY` / `VPN DETECTED` labels.
- Public IP API failover (`ip-api.com`, `ipinfo.io`, `ipapi.co`) using real `proxy`/`hosting` flags.
- IPv6 leak detection (IPv4/IPv6 via ipify).
- `--kill-force` (graceful `terminate()` then `kill()`).
- `--history`, `--clear-history`, and `--export json|csv|txt`.
- `--watch [SECONDS]` continuous monitoring mode.
- `--debug` verbose logging.
- JSON config file (`.activevpn.json` or `ACTIVEVPN_CONFIG` env var).
- Meaningful exit codes: `0` clean, `1` VPN detected, `2` offline/error.
- Exact/CLI-based process matching to reduce false positives.
- `pyproject.toml` packaging with the `activevpn` console script.
- pytest test suite (`tests/`) and GitHub Actions CI.
- Initial project docs, Dockerfile, and contributing/security files.

### Changed

- Removed the ambiguous `"vpn"` entry from `VPN_PROCESS_NAMES`.
- Dependencies pinned with minimum versions in `requirements.txt` and `pyproject.toml`.

## [2.1.0] - 2026-01-13

### Added

- Initial release as VPNActive.
- Rich TUI with system, IP, and DNS scan sections.
- Interface, process, and Tor detection.
- Kill switch (`--kill`).
- Automatic history logging to `.scan_history.json`.
- DNS consistency check.

[2.2.1]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.2.1
[2.2.0]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.2.0
[2.1.0]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.1.0
