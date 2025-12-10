from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import ETLRun
from sqlalchemy import desc

router = APIRouter(prefix="/stats", tags=["stats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("")
def get_stats(db: Session = Depends(get_db)):
    last_run = db.query(ETLRun).order_by(desc(ETLRun.id)).first()
    last_success = (
        db.query(ETLRun).filter(ETLRun.status == "success").order_by(desc(ETLRun.id)).first()
    )
    last_failure = (
        db.query(ETLRun).filter(ETLRun.status == "failed").order_by(desc(ETLRun.id)).first()
    )

    duration_ms = None
    if last_run and last_run.started_at and last_run.finished_at:
        duration_ms = int((last_run.finished_at - last_run.started_at).total_seconds() * 1000)

    return {
        "last_run_status": last_run.status if last_run else None,
        "last_run_records": last_run.records_processed if last_run else None,
        "last_run_duration_ms": duration_ms,
        "last_success": last_success.finished_at if last_success else None,
        "last_failure": last_failure.finished_at if last_failure else None,
        "error": last_run.error_message if last_run and last_run.status == "failed" else None,
    }
