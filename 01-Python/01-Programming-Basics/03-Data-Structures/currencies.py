# pylint: disable=missing-docstring

RATES = {"USDEUR": 0.85, "GBPEUR": 1.13, "CHFEUR": 0.86, "EURGBP": 0.885}

def convert(amount, currency):
    """returns the converted amount in the given currency
    amount is a tuple like (100, "EUR")
    currency is a string
    """
    rate = RATES.get(amount[1]+currency)
    if RATES.get(amount[1]+currency) is None:
        return None
    new_amount = rate*amount[0]
    return round(new_amount)
