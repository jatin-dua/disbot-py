import datetime

UNITS = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds"
}

def parse_time(time: str) -> datetime.timedelta:
    *qty, unit = time
    qty = float("".join(qty))

    time = UNITS.get(unit, "minutes")
    return datetime.timedelta(**{time: qty})