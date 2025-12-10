from sqlalchemy import func
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import RawCoinPaprika, NormalizedCoins, RawCsvCoin, RawCoinGecko
from ingestion.sources.coinpaprika import fetch_coinpaprika_items
from ingestion.sources.csv_source import fetch_csv_rows
from ingestion.sources.coingecko import fetch_coingecko_items
from ingestion.transforms import normalize_coinpaprika, normalize_csv_item, normalize_coingecko
from services.etl_state import update_last_run
from core.db import Base, engine
from core.models import ETLRun
from observability.logger import log_json
import time
import os

CSV_PATH = os.getenv("CSV_PATH")


def run_etl():
    from observability.metrics import (
        etl_runs_total,
        etl_failures_total,
        etl_last_run_timestamp,
        etl_last_success_timestamp,
        etl_last_failure_timestamp,
        etl_records_processed_total,
        etl_last_run_duration_ms
    )

    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    log_json("etl_start", message="Starting ETL pipeline")

    run_entry = ETLRun(source="all", status="running")
    last_run = db.query(ETLRun).order_by(ETLRun.id.desc()).first()

    if last_run and last_run.status == "failed":
        log_json("resume_previous_failure", level="WARNING", message="Resuming failed ETL run")

    start_time = time.time()
    etl_runs_total.inc()
    etl_last_run_timestamp.set(start_time)

    db.add(run_entry)
    db.commit()
    db.refresh(run_entry)

    records_processed = 0

    try:
        # --------------------------
        # CoinPaprika
        # --------------------------
        log_json("extract_start", source="coinpaprika")
        api_items = fetch_coinpaprika_items()
        log_json("extract_complete", source="coinpaprika", count=len(api_items))

        for item in api_items:
            norm = normalize_coinpaprika(item)
            last_ts = db.query(func.max(NormalizedCoins.ts)).filter(
                NormalizedCoins.source_record_id == norm.source_record_id
            ).scalar()

            if last_ts and norm.ts and norm.ts <= last_ts:
                log_json("skip_record", source="coinpaprika", reason="up_to_date", symbol=norm.symbol)
                continue

            db.add(RawCoinPaprika(source_record_id=item.get("id"), payload=item))
            db.add(NormalizedCoins(**norm.model_dump()))
            records_processed += 1

        # --------------------------
        # CSV Source
        # --------------------------
        if CSV_PATH and os.path.exists(CSV_PATH):
            log_json("extract_start", source="csv")
            csv_items = fetch_csv_rows(CSV_PATH)
            log_json("extract_complete", source="csv", count=len(csv_items))

            for item in csv_items:
                norm = normalize_csv_item(item)
                last_ts = db.query(func.max(NormalizedCoins.ts)).filter(
                    NormalizedCoins.source_record_id == norm.source_record_id
                ).scalar()

                if last_ts and norm.ts and norm.ts <= last_ts:
                    log_json("skip_record", source="csv", reason="up_to_date", symbol=norm.symbol)
                    continue

                db.add(RawCsvCoin(source_record_id=item.get("id"), payload=item))
                db.add(NormalizedCoins(**norm.model_dump()))
                records_processed += 1
        else:
            log_json("csv_missing", level="WARNING", message="CSV path not found or missing")

        # --------------------------
        # CoinGecko
        # --------------------------
        try:
            log_json("extract_start", source="coingecko")
            gecko_items = fetch_coingecko_items()
            log_json("extract_complete", source="coingecko", count=len(gecko_items))

            for item in gecko_items:
                norm = normalize_coingecko(item)
                last_ts = db.query(func.max(NormalizedCoins.ts)).filter(
                    NormalizedCoins.source_record_id == norm.source_record_id
                ).scalar()

                if last_ts and norm.ts and norm.ts <= last_ts:
                    log_json("skip_record", source="coingecko", reason="up_to_date", symbol=norm.symbol)
                    continue

                db.add(RawCoinGecko(source_record_id=item.get("id"), payload=item))
                db.add(NormalizedCoins(**norm.model_dump()))
                records_processed += 1

        except Exception as ge:
            log_json("extract_error", level="ERROR", source="coingecko", error=str(ge))

        # --------------------------
        # SUCCESS BLOCK
        # --------------------------
        run_entry.status = "success"
        run_entry.records_processed = records_processed
        run_entry.finished_at = func.now()
        db.commit()

        update_last_run()

        finish = time.time()
        duration_ms = (finish - start_time) * 1000

        etl_last_success_timestamp.set(finish)
        etl_records_processed_total.set(records_processed)
        etl_last_run_duration_ms.set(duration_ms)

        log_json(
            "etl_success",
            message="ETL completed successfully",
            records=records_processed,
            duration_ms=duration_ms
        )

    except Exception as e:
        # --------------------------
        # FAILURE BLOCK
        # --------------------------
        log_json("etl_failure", level="ERROR", error=str(e))

        run_entry.status = "failed"
        run_entry.error_message = str(e)
        run_entry.finished_at = func.now()
        db.commit()
        db.rollback()

        fail_time = time.time()
        duration_ms = (fail_time - start_time) * 1000

        etl_failures_total.inc()
        etl_last_failure_timestamp.set(fail_time)
        etl_last_run_duration_ms.set(duration_ms)

    finally:
        db.close()
        log_json("etl_end", message="ETL pipeline finished", records=records_processed)
