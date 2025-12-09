from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from api.middleware.request_context import request_context_middleware
from api.routers.data import router as data_router
from api.routers.health import router as health_router
from services.etl_service import ETLService

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    interval_mins = 2
    scheduler.add_job(ETLService.run, "interval", minutes=interval_mins)
    scheduler.start()
    print(f"Scheduler started for {interval_mins} mins interval.")
    
    yield
    
    scheduler.shutdown()
    print("Scheduler stopped")

app = FastAPI(title="Kassparo Backend Assignment", lifespan=lifespan)

app.middleware("http")(request_context_middleware)
app.include_router(health_router)
app.include_router(data_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
