from app.models import ExchangeRate
from app.serializers import serialize_rates


def test_serialize_rates():
    rates = [ExchangeRate(year=2026, month=1, average_rate=3.12)]
    serialized = serialize_rates(rates)
    assert serialized == [{"year": 2026, "month": 1, "average_rate": 3.12}]
