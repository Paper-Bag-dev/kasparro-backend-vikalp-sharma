from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import RawCoinPaprika, NormalizedCoins, RawCsvCoin
from ingestion.sources.coinpaprika import fetch_coinpaprika_items
from ingestion.sources.csv_source import fetch_csv_rows
from ingestion.transforms import normalize_coinpaprika, normalize_csv_item
import os


CSV_PATH = os.getenv("CSV_PATH")


def run_etl():
    print("~ Running ETL Pipeline ~")

    db: Session = SessionLocal()

    try:
        """
        Extract, Transform & Load - CoinPaprika
        """
        api_items = fetch_coinpaprika_items()
        print(f"Fetched {len(api_items)} items from CoinPaprika")

        for item in api_items:
            raw = RawCoinPaprika(
                source_record_id=item.get("id"),
                payload=item
            )
            db.add(raw)

            norm = normalize_coinpaprika(item)
            db.add(NormalizedCoins(**norm.model_dump()))

        """
        Extract, Transform & Load - CSV
        """
        if CSV_PATH and os.path.exists(CSV_PATH):
            csv_items = fetch_csv_rows(CSV_PATH)
            print(f"Fetched {len(csv_items)} items from CSV")

            for item in csv_items:
                raw = RawCsvCoin(
                    source_record_id=item.get("id"),
                    payload=item
                )
                db.add(raw)

                norm = normalize_csv_item(item)
                db.add(NormalizedCoins(**norm.model_dump()))
        else:
            print("CSV not found or CSV_PATH not set — skipping CSV ingestion.")

        db.commit()
        print("ETL Completed Successfully")

    except Exception as e:
        print("[ETL ERROR]:", e)
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    run_etl()