import os
import requests
from typing import List, Dict

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_coingecko_items() -> List[Dict]:
    api_key = os.getenv("COINGECKO_API_KEY")
    if not api_key:
        raise ValueError("COINGECKO_API_KEY not set")

    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }

    headers = {
        "x-cg-pro-api-key": api_key
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
