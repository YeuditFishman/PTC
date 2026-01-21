from .database import Base
from sqlalchemy import Column, Float, Integer, UniqueConstraint


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    average_rate = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "year",
            "month",
            name="_year_month_uc",
        ),
    )
