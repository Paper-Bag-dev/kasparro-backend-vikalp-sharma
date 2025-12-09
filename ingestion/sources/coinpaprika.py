import httpx
from typing import List, Dict
import os

def fetch_coinpaprika_items() -> List[Dict]:
    url = "https://api.coinpaprika.com/v1/tickers"
    api_key = os.getenv("COINPAPRIKA_API_KEY")

    try:    
        headers = {}
        if api_key:
            headers = {"Authorization": f"Bearer {api_key}"}
        
        with httpx.Client(timeout=10.0, headers=headers) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
    
    except httpx.HTTPError as e:
        print(f"[CoinPaprika] Encountered HTTP error: {e}")
        return []
    except Exception as e:
        print(f"[CoinPaprika] Encountered HTTP error: {e}")
        return []