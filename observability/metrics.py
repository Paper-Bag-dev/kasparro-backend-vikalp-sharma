from prometheus_client import Counter, Gauge

etl_runs_total = Counter(
    "etl_runs_total",
    "Total number of ETL runs executed"
)

etl_failures_total = Counter(
    "etl_failures_total",
    "Total number of failed ETL runs"
)

etl_last_run_timestamp = Gauge(
    "etl_last_run_timestamp",
    "Timestamp of last ETL run started"
)

etl_last_success_timestamp = Gauge(
    "etl_last_success_timestamp",
    "Timestamp of last successful ETL finish"
)

etl_last_failure_timestamp = Gauge(
    "etl_last_failure_timestamp",
    "Timestamp of last failed ETL finish"
)

etl_records_processed_total = Gauge(
    "etl_records_processed_total",
    "Records processed in the last ETL run"
)

etl_last_run_duration_ms = Gauge(
    "etl_last_run_duration_ms",
    "Duration (ms) of the last ETL run"
)
