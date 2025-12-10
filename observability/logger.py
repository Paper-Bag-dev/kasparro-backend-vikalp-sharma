import json
import sys
import time


def log_json(event: str, level: str = "INFO", **kwargs):
    """
    Emit a single JSON log line to stdout.
    No Python logging module. Tests require clean JSON per line.
    """
    entry = {
        "timestamp": time.time(),
        "level": level,
        "event": event,
        **kwargs,
    }

    sys.stdout.write(json.dumps(entry) + "\n")
    sys.stdout.flush()
