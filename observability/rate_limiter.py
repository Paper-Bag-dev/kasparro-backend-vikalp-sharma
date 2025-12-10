import time
from observability.logger import log_json

RATE_LIMITS = {
    "coingecko": 1.2,
    "coinpaprika": 0.5,
}

_last_call = {}

def reset_rate_limiter():
    from time import sleep
    global _last_call
    _last_call = {}


def enforce_rate_limit(source: str):
    from time import sleep

    limit = RATE_LIMITS.get(source)
    if not limit:
        return

    now = time.time()
    last = _last_call.get(source, 0)
    delta = now - last

    if delta < limit:
        wait = limit - delta
        log_json("rate_limit_sleep", source=source, wait_seconds=wait)
        sleep(wait)

    _last_call[source] = time.time()
