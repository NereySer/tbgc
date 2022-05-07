from datetime import datetime, timezone, timedelta

DEFAULT_TIMEZONE = timezone(timedelta(hours=+3))
LATE_HOUR = 12
EVENING_HOUR = 17

def get_event_start_time(event) -> datetime:
    start_time = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
    
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo = DEFAULT_TIMEZONE)
        
    return start_time

def removeOldEvents(events, now):
    if not events: return (now, now)

    for event in events:
        event_datetime = get_event_start_time(event)
        
        if now > event_datetime: 
            events.remove(event)

def checkEvents(events):
    if not events: return
        
    first_event_datetime = get_event_start_time(events[0])
    last_event_datetime = first_event_datetime
    events_date = first_event_datetime.date()

    for event in events:
        first_event_datetime = min(event_datetime, first_event_datetime)
        last_event_datetime = max(event_datetime, last_event_datetime)
        
        if event_datetime.date() != events_date:
            raise Exception("Events in different days are not allowed")
        
    return (first_event_datetime, last_event_datetime)

def isTimeToRemind(events) -> (bool, datetime): 
    now = datetime.now(DEFAULT_TIMEZONE)
    
    removeOldEvents(events, now)
    (first_event_datetime, last_event_datetime) = checkEvents(events, now)
    if not events: return (False, now)
    
    if first_event_datetime.date() > now.date() + timedelta(days = 1): 
        #Day after tomorrow no sense to remind
        return (False, last_event_datetime)
    
    if first_event_datetime.date() == now.date(): 
        #Today morning reminder OR daytime reminder
        return (first_event_datetime.hour < EVENING_HOUR or now.hour >= LATE_HOUR - 1, last_event_datetime)
    else:
        #Evening reminder for early tomorrow events
        return (now.hour > LATE_HOUR and first_event_datetime.hour < LATE_HOUR, last_event_datetime)
    
    raise Exception("Something wrong occured")

def getTimeBounds():
    begin = datetime.now(DEFAULT_TIMEZONE)

    if begin.hour > LATE_HOUR:
        #Too late to remind about today's events, so let's look for tomorrow
        begin += timedelta(days = 1)
        begin = begin.replace(hour=0, minute=0, second=0, microsecond=0)
    
    end = begin.replace(hour=23, minute=59, second=59, microsecond=0)

    return {
        'begin': begin, 
        'end': end    
    }
