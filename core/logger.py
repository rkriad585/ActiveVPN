# ActiveVPN/core/logger.py
import csv
import datetime
import io
import json
import os

from config import LOG_FILE


def load_history():
    """Returns the list of past scan entries (or [] if none/invalid)."""
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError, UnicodeDecodeError):
        return []


def save_log(scan_data: dict):
    """
    Appends the current scan results to a JSON log file.
    """
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "scan_results": scan_data,
    }

    data = load_history()
    data.append(entry)

    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False


def clear_history():
    """Deletes the scan history file. Returns True on success."""
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        return True
    except OSError:
        return False


def flatten_entry(entry: dict) -> dict:
    """Flattens a history entry into a flat dict for CSV/JSON export."""
    scan = entry.get("scan_results", {})
    ip_data = scan.get("public_ip") or {}
    dns_data = scan.get("dns_leak") or {}
    verdict = scan.get("verdict") or {}

    return {
        "timestamp": entry.get("timestamp", ""),
        "verdict": verdict.get("label", ""),
        "score": verdict.get("score", 0),
        "interfaces": ", ".join(scan.get("interfaces", [])),
        "vpn_processes": ", ".join(
            p.get("name", "") for p in scan.get("vpn_processes", [])
        ),
        "tor_processes": ", ".join(
            p.get("name", "") for p in scan.get("tor_processes", [])
        ),
        "public_ip": ip_data.get("query", ip_data.get("ip", "")),
        "isp": ip_data.get("isp", ip_data.get("org", "")),
        "country": ip_data.get("country", ""),
        "dns_ip": dns_data.get("ip", ""),
        "ipv4": scan.get("ipv4", ""),
        "ipv6": scan.get("ipv6", ""),
    }


def export_history(export_format: str = "json", path: str = None):
    """Exports scan history to the given format. Returns the file path used."""
    if path is None:
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"activevpn_export_{stamp}.{export_format}"

    rows = [flatten_entry(e) for e in load_history()]

    if export_format == "csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    elif export_format == "txt":
        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, indent=2) + "\n")
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=4)

    return path


def history_to_json(history):
    """Serializes history to a JSON string (used by --export -)."""
    return json.dumps(history, indent=4)


def history_to_csv(history):
    """Serializes history to a CSV string."""
    rows = [flatten_entry(e) for e in history]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()
