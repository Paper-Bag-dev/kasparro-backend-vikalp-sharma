from ingestion.etl_runner import run_etl
from services.etl_state import update_last_run

class ETLService:
    @staticmethod
    def run():
        print("[ETL]: Running scheduled ETL...")
        run_etl()
        update_last_run()