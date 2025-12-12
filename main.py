from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from api.middleware.request_context import request_context_middleware
from api.routers.data import router as data_router
from api.routers.health import router as health_router
from api.routers.stats import router as stats_router
from api.routers.admin import router as admin_router
from services.etl_service import ETLService
from api.routers.metrics import router as metrics_router
import os

scheduler = None
APP_ENV = os.getenv("APP_ENV", "local")
ETL_FETCH_INTERVAL = os.getenv("ETL_FETCH_INTERVAL", 2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    
    if APP_ENV == "local":
        scheduler = BackgroundScheduler()
        scheduler.add_job(ETLService.run, "interval", minutes=ETL_FETCH_INTERVAL)
        scheduler.start()
        print("Local scheduler started.")
    else:
        print("Cloud mode — scheduler disabled. ETL only triggered via /internal/run-etl")
    
    yield

    if scheduler:
        scheduler.shutdown()
        print("Scheduler stopped")


app = FastAPI(title="Kassparo Backend Assignment", lifespan=lifespan)

app.middleware("http")(request_context_middleware)
app.include_router(health_router)
app.include_router(data_router)
app.include_router(stats_router)
app.include_router(admin_router)
app.include_router(metrics_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
