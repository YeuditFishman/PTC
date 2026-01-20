from .database import Base, engine
import logging
import time

logger = logging.getLogger(__name__)


def startup_event():
    retries = 5
    while retries:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except Exception as error:
            logger.warning(f"DB creation failed, retries left {retries}: {error}")
            retries -= 1
            time.sleep(2)
    if retries == 0:
        raise RuntimeError("Database is not available")
