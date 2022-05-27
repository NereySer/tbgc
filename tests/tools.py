from datetime import datetime, timedelta
from modules.time_checks import DEFAULT_TIMEZONE

def g_cal_event(hour, days_add = 0, text = '', duration = 1, transparent = False, base_date = None):
    assert hour >= 0

    if base_date is None:
        base_date = datetime.now(DEFAULT_TIMEZONE)

    retVal = {
        'summary': text,
        'transparency': ('transparent' if transparent else 'opaque')
    }

    start_time = base_date.replace(hour=hour) + timedelta(days = days_add)

    retVal['start'] = start_time
    retVal['end'] = (start_time + timedelta(hours = duration))

    return retVal
