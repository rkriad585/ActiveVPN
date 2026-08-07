# Troubleshooting

Common problems and their fixes.

## In this guide

- [`activevpn: command not found`](#activevpn-command-not-found)
- [`ModuleNotFoundError`](#modulenotfounderror)
- [Exit code 2 / "Could not fetch Public IP"](#exit-code-2--could-not-fetch-public-ip)
- [`--kill` fails with permission errors](#--kill-fails-with-permission-errors)
- [Garbled characters in the output](#garbled-characters-in-the-output)
- [My config file is ignored](#my-config-file-is-ignored)
- [History shows old scans](#history-shows-old-scans)

## `activevpn: command not found`

The package isn't installed, or the script directory isn't on your PATH.

```bash
pip install activevpn
python -m pip show activevpn   # prints install location
```

## `ModuleNotFoundError`

The runtime dependencies are missing. Install them from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs `psutil`, `rich`, `pyfiglet`, and `requests`.

## Exit code 2 / "Could not fetch Public IP"

The public IP/DNS APIs are unreachable. Check your connection, then confirm the endpoints in `IP_API_URLS` and `DNS_LEAK_API_URL` (see [configuration.md](configuration.md)). Run with `--debug` to see which endpoints were attempted.

## `--kill` fails with permission errors

`--kill` needs administrator/root privileges:

```bash
sudo activevpn --kill          # Linux/macOS
```

On Windows, open the terminal **as Administrator**. If a process still refuses to stop after 3 seconds, use `--kill-force`.

## Garbled characters in the output

On some Windows consoles (legacy `cp1252`), non-ASCII symbols can render as `?`. The confidence bar uses only ASCII `#` and `-`. If you still see issues, run inside Windows Terminal, use the `--export txt` output, or switch the console codepage to UTF-8:

```powershell
chcp 65001
```

## My config file is ignored

- The file must be named `config.toml` under `~/.config/neostore/ActiveVPN/` (Linux), `%LOCALAPPDATA%\neostore\ActiveVPN\` (Windows), or set explicitly with `ACTIVEVPN_CONFIG`.
- Keys must match `config.py` constants exactly (uppercase).
- Only string, list, and boolean values are applied.

See [configuration.md](configuration.md).

## History shows old scans

History accumulates across runs. Use `activevpn --clear-history` to wipe it, or delete the history file in the data dir.

---

<a href="../">← Back to Home</a>
