import os
from typing import List, Dict
from observability.http_client import request_with_retry
from observability.rate_limiter import enforce_rate_limit

def fetch_coinpaprika_items() -> List[Dict]:
    enforce_rate_limit("coingecko")
    url = "https://api.coinpaprika.com/v1/tickers"
    api_key = os.getenv("COINPAPRIKA_API_KEY")

    headers = {}
    if api_key:
        headers = {"Authorization": f"Bearer {api_key}"}

    response = request_with_retry(
        "GET",
        url,
        headers=headers,
        timeout=10.0,
    )

    return response.json()
