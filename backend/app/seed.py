import csv
from .database import SessionLocal, Base, engine
from .models import ExchangeRate
import os


def run_seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    data_file = os.path.join(os.path.dirname(__file__), "data", "EXR.csv")

    with open(data_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year, month = map(int, row["TIME_PERIOD"].split("-"))
            average_rate = float(row["OBS_VALUE"])

            exists = (
                db.query(ExchangeRate)
                .filter_by(year=year, month=month)
                .first()
            )
            if not exists:
                db.add(ExchangeRate(
                    year=year,
                    month=month,
                    average_rate=average_rate
                ))

    db.commit()
    db.close()
    print("Seed finished!")


if __name__ == "__main__":
    run_seed()
