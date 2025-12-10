from fastapi import APIRouter, HTTPException, Header
from services.etl_service import ETLService
import os, threading

router = APIRouter(prefix="/internal", tags=["internal"])

@router.post("/run-etl")
def run_etl_internal(x_api_key: str = Header(None)):
    secret = os.getenv("CRON_SECRET")

    if x_api_key != secret:
        raise HTTPException(status_code=401, detail="Unauthorized")

    threading.Thread(target=ETLService.run).start()
    return {"status": "ok", "message": "ETL triggered"}

