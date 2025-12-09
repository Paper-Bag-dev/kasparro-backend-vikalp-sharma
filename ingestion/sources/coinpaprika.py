import httpx
from typing import List, Dict

def fetch_coinpaprika_items() -> List[Dict]:
    url = "https://api.coinpaprika.com/v1/tickers"
    try:    
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
    
    except httpx.HTTPError as e:
        print(f"[CoinPaprika] Encountered HTTP error: {e}")
        return []
    except Exception as e:
        print(f"[CoinPaprika] Encountered HTTP error: {e}")
        return []