# Kasparro Crypto ETL System — Submission Overview

This project implements a complete ETL + API backend for the Kasparro assignment.

## ✅ Completed Requirements
**P0 — Core ETL + API + Docker**  
**P1 — Fully runnable system (Dockerized, scheduler, internal trigger, migrations)**  
**P2.3 — Observability (structured JSON logging, metrics)**  
**P2.4 — GitHub Actions CI (tests + Postgres service)**  
**P2.5 — DevOps Enhancements (Docker Hub image publishing, clean Dockerfile)**  

## 🔧 Tech Stack
- FastAPI — API layer  
- PostgreSQL — storage  
- SQLAlchemy — ORM  
- Docker — runtime  
- APScheduler — ETL scheduler  
- httpx — retry + exponential backoff  
- Prometheus metrics — ETL observability  

---

## 📦 Docker Image (Final Submission)

Public Docker Hub image:  
👉 **https://hub.docker.com/r/aetherlover/kasparro-backend**

Pull it:

```
docker pull aetherlover/kasparro-backend:latest
```


---

# 🚀 Run Locally

## 1. Create `.env`

(Replace values)

#### ADD YOUR BLOCK HERE

Important variables:

- `DATABASE_URL`
- `COINGECKO_API_KEY`
- `CRON_SECRET`
- `CSV_PATH=./data/coins.csv`
- `APP_ENV=local`

---

## 2. Start the entire system

The repo already includes **Makefile + docker-compose**, so simply run:

```
make up
```
or 
```
make down
make test
```


API will be available at:

👉 **http://localhost:8000**

---

## 3. Trigger ETL Manually

```
curl -X POST http://localhost:8000/internal/run-etl
-H "x-api-key: <CRON_SECRET>"
```


# 📁 Endpoints

```
GET /health
GET /data
GET /stats
GET /metrics
```


This project completes all core and some advanced requirements in P2, including observability, CI, Docker image publishing, and a clean deployment-ready architecture.
