<div align="center">

  <img src=".github/logo.svg" alt="VPNActive Logo" width="200" height="200">

  # 🛡️ VPNActive

  **The Ultimate Network Privacy & VPN Detection Tool**

  [Report Bug](https://github.com/rkriad585/vpnActive/issues) · [Request Feature](https://github.com/rkriad585/vpnActive/issues)

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Rich](https://img.shields.io/badge/TUI-Rich-magenta.svg)](https://github.com/Textualize/rich)

</div>

---

## 📖 Introduction

**VPNActive** is a powerful, cross-platform terminal utility designed to verify your digital privacy status. Whether you are a privacy enthusiast, a sysadmin, or just a casual user, knowing if your VPN is *actually* working is crucial.

Unlike simple "What is my IP" websites, **VPNActive** dives deeper. It inspects your system's network interfaces, analyzes running processes, checks your external IP against known hosting providers, and performs DNS leak tests—all presented in a beautiful, hacker-style TUI (Terminal User Interface).

## 🚀 How It Works

VPNActive operates on three distinct layers to ensure accuracy:

1.  **System Layer Inspection 💻**
    *   It scans your operating system (Linux, Windows, macOS, Android/Termux) for network interfaces commonly used by VPN protocols (e.g., `tun0`, `wg0`, `ppp`).
    *   It checks for active processes associated with VPN providers (e.g., `openvpn`, `wireguard`, `nordvpn`, `tor`).

2.  **External IP Analysis 🌍**
    *   It queries external APIs to fetch your Public IP.
    *   It analyzes the ISP (Internet Service Provider) name. If the ISP is a known Data Center (e.g., DigitalOcean, M247), it flags the connection as **"LIKELY VPN/PROXY"**.

3.  **DNS Leak Detection 🕵️‍♂️**
    *   It compares your Public IP with the IP address resolving your DNS queries. If they are different, it warns you, helping you identify potential DNS leaks where your ISP might still see your requests.

## ✨ Features

*   **🖥️ Beautiful TUI:** Built with the `rich` library for a modern, colorful, and easy-to-read terminal interface.
*   **🐧 Cross-Platform:** Works seamlessly on Linux, macOS, Windows, and Android (via Termux).
*   **🔎 Deep Scan:** Detects VPNs via Interface names, Process names, and IP reputation.
*   **🧅 Tor Detection:** Specifically checks for active Tor services.
*   **☠️ Kill Switch:** Built-in command to terminate running VPN processes instantly.
*   **📝 History Logging:** Automatically saves scan results to `scan_history.json` for your records.
*   **🚨 DNS Consistency:** Verifies if your DNS requests are being tunneled correctly.

## 📂 Project Structure

Here is how **VPNActive** is organized:

```text
vpnActive/
├── main.py               # 🚀 Entry point: The script you run to start the tool
├── config.py             # ⚙️ Configuration: Settings, API URLs, and Colors
├── .scan_history.json     # 📄 Logs: Stores past scan results (Auto-generated)
└── core/                 # 🧠 Core Logic Folder
    ├── __init__.py       #    Package initializer
    ├── logo.py           #    🎨 Generates the ASCII Art Banner
    ├── help.py           #    ℹ️ Handles the Help Menu display
    ├── detector.py       #    🕵️ Main Logic: Scans IPs, Interfaces & DNS
    └── logger.py         #    💾 Handles saving data to JSON
```

## 🛠️ Installation & Usage

### Prerequisites
*   Python 3.8 or higher
*   Pip (Python Package Manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/rkriad585/vpnActive.git
cd vpnActive
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
# Or manually:
pip install psutil rich pyfiglet requests
```

### Step 3: Run the Tool
```bash
python main.py
```

## 🎮 Command Usage Examples

### 1. Standard Network Scan
Performs a full check of interfaces, processes, and external IP.
```bash
python main.py
```

### 2. Kill Active VPNs ☠️
*Requires Administrator/Root privileges.* Attempts to terminate known VPN processes.
```bash
# Linux/Mac
sudo python main.py --kill

# Windows (Run cmd as Admin)
python main.py --kill
```

### 3. Help Menu ℹ️
Displays all available commands and flags.
```bash
python main.py --help
```

## ⚙️ Configuration

You can customize the tool by editing `config.py`.

*   **Add new VPNs:** Add process names to `VPN_PROCESS_NAMES` or interface prefixes to `VPN_INTERFACE_PATTERNS`.
*   **Change Colors:** Modify the `COLOR_*` constants to theme the UI to your liking.

## 🤝 Contributing & Issues

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  **Fork** the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  **Push** to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a **Pull Request**

Found a bug? [Open an Issue](https://github.com/rkriad585/vpnActive/issues) to help us fix it!

## 🌐 Connect with Me

If you like this project, feel free to connect!

| Platform | Username | Link |
| :--- | :--- | :--- |
| **GitHub** | @rkriad585 | [github.com/rkriad585](https://github.com/rkriad585) |
| **YouTube** | @rkriad585 | [youtube.com/@rkriad585](https://youtube.com/@rkriad585) |
| **X (Twitter)** | @rk_riad585 | [x.com/rk_riad585](https://x.com/rk_riad585) |
| **Facebook** | @rkriad585 | [facebook.com/rkriad585](https://facebook.com/rkriad585) |
| **Instagram** | @rkriad585 | [instagram.com/rkriad585](https://instagram.com/rkriad585) |
| **Threads** | @rkriad585 | [threads.net/@rkriad585](https://threads.net/@rkriad585) |
| **Email** | rkriad585 | [mailto:rkriad585@gmail.com](mailto:rkriad585@gmail.com) |

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---
<div align="center">
  <sub>Built with ❤️ by Google Gemini & rkriad585</sub>
</div>
