# vpnActive/core/logger.py
import json
import os
import datetime
from config import LOG_FILE

def save_log(scan_data: dict):
    """
    Appends the current scan results to a JSON log file.
    """
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "scan_results": scan_data
    }

    data = []
    
    # Check if file exists and load valid JSON
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        except (json.JSONDecodeError, IOError):
            data = []

    data.append(entry)

    # Write back to file
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False
