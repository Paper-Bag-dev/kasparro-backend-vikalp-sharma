import pytest
from services.etl_service import run_etl

def test_etl_failure(monkeypatch):
    def mock_fetch():
        raise Exception("Boom")

    monkeypatch.setattr("ingestion.sources.coinpaprika.fetch_coinpaprika_items", mock_fetch)

    try:
        run_etl()
        assert True
    except Exception:
        assert False, "ETL should not crash on fetch failure"
