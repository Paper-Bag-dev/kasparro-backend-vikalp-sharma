from fastapi import APIRouter, Request
from sqlalchemy import text
from core.db import engine
from services.etl_state import get_last_etl_run

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "up"
    except:
        db_status = "down"

    return {
        "status" : "ok",
        "db" : db_status,
        "last_etl_run" : str(get_last_etl_run()),
        "request_id" : request.state.request_id,
    }