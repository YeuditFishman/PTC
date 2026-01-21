from app.database import SessionLocal
from app.update_exchange import update_latest_month
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


def run_monthly_update():
    db = SessionLocal()
    try:
        update_latest_month(db)
        logger.info("Monthly update completed successfully.")
    except Exception as error:
        logger.error(f"Error during monthly update: {error}")
    finally:
        db.close()


def wait_for_monthly_update():
    while True:
        now = datetime.now()
        if now.day == 1 and now.hour == 0:
            logger.info("Running monthly update...")
            run_monthly_update()
            time.sleep(24 * 60 * 60)
        else:
            time.sleep(60 * 60)


if __name__ == "__main__":
    wait_for_monthly_update()
