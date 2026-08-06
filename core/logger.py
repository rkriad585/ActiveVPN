# ActiveVPN/core/logger.py
"""Backward-compatible shim.

The real implementation moved to ``activevpn.logger``. This module re-exports
everything so existing imports like ``from core.logger import save_log`` keep
working. Prefer ``from activevpn import ...`` in new code.
"""
from activevpn.logger import (  # noqa: F401
    clear_history,
    export_history,
    flatten_entry,
    history_to_csv,
    history_to_json,
    load_history,
    save_log,
)
