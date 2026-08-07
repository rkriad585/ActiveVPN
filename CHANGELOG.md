# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.0] - 2026-08-07

### Added

- **TOML config file**: the default config is now `config.toml` (still at `~/.config/neostore/ActiveVPN/`), parsed with the stdlib `tomllib` (Python 3.11+) or `tomli` (older Pythons) and written with `tomli-w`.
- Dependencies: `tomli>=2.0; python_version<'3.11'` and `tomli-w>=1.0`.
- **Automated documentation deployment**: MkDocs site built and deployed to GitHub Pages by GitHub Actions (`.github/workflows/docs.yml`), with a docs build check in CI.
- **Automated container publishing**: `.github/workflows/docker-publish.yml` builds the image with Docker Buildx and pushes it to GitHub Container Registry (`ghcr.io/rkriad585/activevpn`) on version tags, `main` pushes, and manual dispatch.

### Changed

- `activevpn.config.save_config()` writes TOML; `load_config_file()` parses TOML with a JSON fallback so legacy `.activevpn.json` files keep loading.
- Docs (configuration, architecture, troubleshooting) and README updated for the `config.toml` path.
- Project URLs updated: `Documentation` points to the GitHub Pages site (`https://rkriad585.github.io/ActiveVPN`) and an `Author Website` entry added.
- README logo and screenshot now use absolute raw GitHub URLs so they render on PyPI.

## [2.3.0] - 2026-08-06

### Added

- **Library API**: new importable `activevpn` package with a typed data model (`ScanResult`, `Verdict`, `IPInfo`, `DNSInfo`, `ProcessInfo`), a one-shot `activevpn.scan()`, silent mode (`console=None`), serializable results (`.to_dict()` / `.to_json()`), and a `watch()` generator with `on_scan` / `on_change` callbacks.
- **Cross-platform config paths** via `platformdirs`: config now lives at `~/.config/neostore/ActiveVPN/config.json` (Linux), `%LOCALAPPDATA%\neostore\ActiveVPN` (Windows), or `~/Library/Application Support/neostore/ActiveVPN` (macOS). Scan history moved to the platform data directory.
- Typed `Config` dataclass with `load_config()`, `save_config()`, and `resolve_config_path()`. File keys accept both snake_case field names and legacy uppercase constant names.
- `core/` and top-level `config.py` kept as backward-compatible shims for existing imports.
- Config test suite (`tests/test_config.py`).

### Changed

- Dependency added: `platformdirs>=3.0`.
- Docs updated: README "Using as a Library" section, rewritten architecture guide, updated config/CLI/history references.

## [2.2.2] - 2026-08-06

### Changed

- Rewrote the `LICENSE` with the official standard MIT License text.

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

[2.4.0]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.4.0
[2.3.0]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.3.0
[2.2.2]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.2.2
[2.2.1]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.2.1
[2.2.0]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.2.0
[2.1.0]: https://github.com/rkriad585/ActiveVPN/releases/tag/v2.1.0
