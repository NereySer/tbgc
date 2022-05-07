from datetime import datetime, timezone, timedelta

DEFAULT_TIMEZONE = timezone(timedelta(hours=+3))
LATE_HOUR = 12
EVENING_HOUR = 17

def get_event_start_time(event) -> datetime:
    start_time = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
    
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo = DEFAULT_TIMEZONE)
        
    return start_time

def checkEvents(events, now):
    first_event_datetime = None
    last_event_datetime = None
    events_date = None
    
    for event in events:
        event_datetime = get_event_start_time(event)
        
        if now > event_datetime: 
            events.remove(event)
            
            continue
        
        if first_event_datetime is None or first_event_datetime > event_datetime:
            first_event_datetime = event_datetime
        
        if last_event_datetime is None or last_event_datetime < event_datetime:
            last_event_datetime = event_datetime
        
        if events_date is None:
            events_date = event_datetime.date()
        elif event_datetime.date() != events_date:
            raise Exception("Events in different days are not allowed")
        
    return (first_event_datetime, last_event_datetime)

def isTimeToRemind(events) -> (bool, datetime): 
    now = datetime.now(DEFAULT_TIMEZONE)
    
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
