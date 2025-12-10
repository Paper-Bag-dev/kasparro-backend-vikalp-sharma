from ingestion.etl_runner import run_etl
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import NormalizedCoins

def test_incremental_ingestion():
    db: Session = SessionLocal()

    # Before first run
    run_etl()
    count_before = db.query(NormalizedCoins).count()

    # Second run
    run_etl()
    count_after = db.query(NormalizedCoins).count()

    assert count_before == count_after
