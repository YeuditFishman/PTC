def serialize_rates(rates):
    return [
        {
            "year": r.year,
            "month": r.month,
            "average_rate": r.average_rate
        } for r in rates
    ]
