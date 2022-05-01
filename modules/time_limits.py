from datetime import datetime, timezone, timedelta

DEFAULT_TIMEZONE = timezone(timedelta(hours=+3))

def getStart():
    return datetime.utcnow().isoformat() + 'Z'

def getEnd(): 
    now = datetime.now(DEFAULT_TIMEZONE)
    
    if now.hour > 12:
        end_day = now + timedelta(days = 1)
    else:
        end_day = now
    
    end_day = end_day.replace(hour=23, minute=59, second=59, microsecond=0)

    return end_day.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + 'Z'
