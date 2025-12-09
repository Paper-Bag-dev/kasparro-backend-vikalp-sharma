from ingestion.transforms import normalize_coinpaprika, normalize_csv_item

def test_normalize_coinpaprika():
    raw = {
        "id": "btc-bitcoin",
        "name": "Bitcoin",
        "symbol": "BTC",
        "last_updated": "2025-01-01T00:00:00Z",
        "quotes": {
            "USD": {
                "price": 45000.12,
                "market_cap": 900000000,
                "volume_24h": 30000000
            }
        }
    }

    normalized = normalize_coinpaprika(raw)

    assert normalized.source_name == "coinpaprika"
    assert normalized.source_record_id == "btc-bitcoin"
    assert normalized.symbol == "BTC"
    assert normalized.price == 45000.12
    assert normalized.market_cap == 900000000
    assert normalized.volume_24h == 30000000
    assert normalized.ts.isoformat() == "2025-01-01T00:00:00+00:00"


def test_normalize_csv_item():
    raw = {
        "id": "eth-ethereum",
        "name": "Ethereum",
        "symbol": "ETH",
        "price": 3000.5,
        "market_cap": 200000000,
        "volume_24h": 15000000,
        "last_updated": "2025-01-01T01:00:00Z"
    }

    normalized = normalize_csv_item(raw)

    assert normalized.source_name == "csv"
    assert normalized.symbol == "ETH"
    assert normalized.price == 3000.5
    assert normalized.ts.isoformat() == "2025-01-01T01:00:00+00:00"

