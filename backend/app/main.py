from .database import Base, engine, SessionLocal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ExchangeRate
import time

app = FastAPI(title="PTC Exchange Checker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    retries = 5
    while retries:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except Exception:
            retries -= 1
            time.sleep(2)
    if retries == 0:
        raise RuntimeError("Database is not available")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/rates")
def get_rates():
    db = SessionLocal()
    try:
        rates = (
            db.query(ExchangeRate)
            .order_by(
                ExchangeRate.year,
                ExchangeRate.month,
            )
            .all()
        )
        return [
            {
                "year": r.year,
                "month": r.month,
                "average_rate": r.average_rate,
            }
            for r in rates
        ]
    finally:
        db.close()
