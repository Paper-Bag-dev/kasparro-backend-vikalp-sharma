import os
from typing import List, Dict
from observability.http_client import request_with_retry
from observability.rate_limiter import enforce_rate_limit
from observability.logger import log_json

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_coingecko_items() -> List[Dict]:
    enforce_rate_limit("coingecko")

    api_key = os.getenv("COINGECKO_API_KEY")
    if not api_key:
        log_json(
            "coingecko_missing_api_key",
            level="ERROR",
            error="COINGECKO_API_KEY not set"
        )
        raise ValueError("COINGECKO_API_KEY not set")

    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false",
    }

    headers = {"x-cg-api-key": api_key}

    try:
        response = request_with_retry(
            "GET",
            url,
            params=params,
            headers=headers,
            timeout=10.0,
        )
        data = response.json()

        log_json(
            "coingecko_fetch_success",
            count=len(data)
        )

        return data

    except Exception as e:
        log_json(
            "coingecko_fetch_error",
            level="ERROR",
            error=str(e),
            url=url
        )
        return []
