from .models import ExchangeRate


def fetch_exchange_rates(db):
    return db.query(ExchangeRate).order_by(
        ExchangeRate.year, ExchangeRate.month
    ).all()


def insert_exchange_rates(db, data):
    for year, month, average_rate in data:
        exists = db.query(ExchangeRate).filter_by(
            year=year,
            month=month
        ).first()
        if not exists:
            new_rate = ExchangeRate(
                year=year,
                month=month,
                average_rate=average_rate
            )
            db.add(new_rate)
    db.commit()


def run_seed(db, data):
    insert_exchange_rates(db, data)
