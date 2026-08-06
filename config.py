# ActiveVPN/config.py
"""Backward-compatible shim.

Real implementation moved to ``activevpn.config``. Re-exports the legacy
uppercase constants and the new typed :class:`Config` API.

New code should use ``from activevpn import load_config``.
"""
from activevpn.config import (  # noqa: F401
    APP_NAME,
    AUTHOR,
    VERSION,
    ORG_NAME,
    CONFIG_DIR,
    CONFIG_FILE,
    DATA_DIR,
    LOG_FILE,
    LEGACY_CONFIG_FILE,
    VPN_INTERFACE_PATTERNS,
    VPN_PROCESS_NAMES,
    TOR_PROCESS_NAMES,
    IP_API_URLS,
    DNS_LEAK_API_URL,
    IPV4_URLS,
    IPV6_URLS,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_INFO,
    COLOR_TITLE,
    SCORE_INTERFACE,
    SCORE_VPN_PROCESS,
    SCORE_TOR_PROCESS,
    SCORE_HOSTING,
    SCORE_PROXY,
    Config,
    load_config,
    load_config_file,
    resolve_config_path,
    save_config,
)
