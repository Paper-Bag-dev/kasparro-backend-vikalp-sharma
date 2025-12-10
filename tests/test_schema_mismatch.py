import pytest
from ingestion.transforms import normalize_coinpaprika
from pydantic import ValidationError

def test_schema_mismatch():
    invalid_item = {
        "id": "btc-bitcoin",
        "symbol": "BTC"
    }

    with pytest.raises(ValidationError):
        normalize_coinpaprika(invalid_item)
