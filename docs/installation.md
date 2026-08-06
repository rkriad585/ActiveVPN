# Installation

Install ActiveVPN on any supported platform.

## Requirements

- Python 3.8 or newer
- `pip`

## Install from PyPI (recommended)

```bash
pip install activevpn
```

The `activevpn` console command becomes available on your PATH.

## Install from source

```bash
git clone https://github.com/rkriad585/ActiveVPN.git
cd ActiveVPN
pip install -r requirements.txt
```

Or install it as a package in development mode:

```bash
pip install -e .
```

## Platform notes

### Linux

```bash
sudo apt update && sudo apt install -y python3 python3-pip
pip install activevpn
```

`--kill` and `--kill-force` require root: `sudo activevpn --kill`.

### macOS

Install Python via Homebrew:

```bash
brew install python
pip install activevpn
```

### Windows

1. Install Python from [python.org](https://www.python.org/) (tick **"Add Python to PATH"**).
2. Open a terminal (run as Administrator for `--kill`).

```powershell
pip install activevpn
```

### Android (Termux)

```bash
pkg install python
pip install activevpn
```

## Verify the install

```bash
activevpn --help
```

You should see the banner and the help menu. See [getting-started.md](getting-started.md) for your first scan.

---

<a href="../README.md">← Back to README</a>
