from .database import get_db
from .db_utils import fetch_exchange_rates
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .serializers import serialize_rates
from .startup import startup_event

logger = logging.getLogger(__name__)

app = FastAPI(title="PTC Exchange Checker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/rates")
def get_rates(db=Depends(get_db)):
    rates = fetch_exchange_rates(db)
    return serialize_rates(rates)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.add_event_handler("startup", startup_event)
