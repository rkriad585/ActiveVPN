# ActiveVPN/activevpn/__init__.py
"""ActiveVPN — the network privacy & VPN detection library.

Public API for developers::

    import activevpn

    # One-shot scan
    result = activevpn.scan()
    print(result.verdict.label, result.verdict.score)
    print(result.to_json())

    # Programmatic configuration
    cfg = activevpn.load_config()
    cfg.vpn_process_names.append("myvpn")

    # Continuous watch with callbacks
    detector = activevpn.NetworkDetector(console=None, config=cfg)
    for result in detector.watch(interval=60, on_change=lambda r: print(r.verdict.label)):
        ...
"""

from activevpn.config import (
    APP_NAME,
    AUTHOR,
    VERSION,
    ORG_NAME,
    CONFIG_DIR,
    CONFIG_FILE,
    DATA_DIR,
    LOG_FILE,
    Config,
    load_config,
    load_config_file,
    resolve_config_path,
    save_config,
)
from activevpn.detector import (
    NetworkDetector,
    ProcessInfo,
    IPInfo,
    DNSInfo,
    Verdict,
    ScanResult,
    scan,
)
from activevpn.logger import (
    load_history,
    save_log,
    clear_history,
    flatten_entry,
    export_history,
    history_to_json,
    history_to_csv,
)

__all__ = [
    "APP_NAME",
    "AUTHOR",
    "VERSION",
    "ORG_NAME",
    "CONFIG_DIR",
    "CONFIG_FILE",
    "DATA_DIR",
    "LOG_FILE",
    "Config",
    "load_config",
    "load_config_file",
    "resolve_config_path",
    "save_config",
    "NetworkDetector",
    "ProcessInfo",
    "IPInfo",
    "DNSInfo",
    "Verdict",
    "ScanResult",
    "scan",
    "load_history",
    "save_log",
    "clear_history",
    "flatten_entry",
    "export_history",
    "history_to_json",
    "history_to_csv",
]
