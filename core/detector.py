# ActiveVPN/core/detector.py
"""Backward-compatible shim.

The real implementation moved to ``activevpn.detector``. This module re-exports
everything so existing imports like ``from core.detector import NetworkDetector``
keep working. Prefer ``from activevpn import ...`` in new code.
"""
from activevpn.detector import (  # noqa: F401
    API_TIMEOUT,
    DNSInfo,
    IPInfo,
    NetworkDetector,
    ProcessInfo,
    ScanResult,
    Verdict,
    scan,
)
