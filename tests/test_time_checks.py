import pytest

from datetime import datetime, timezone, timedelta

from modules import time_checks
from modules.time_checks import DEFAULT_TIMEZONE, LATE_HOUR

def getTime(time):
    assert time.tzinfo==DEFAULT_TIMEZONE
    
    return time

def generate_event(hour, days_add):
    return {
        'start': {
            'dateTime': (datetime.now(DEFAULT_TIMEZONE).replace(hour=hour) + timedelta(days = days_add)).isoformat()
        }
    }

@pytest.mark.parametrize("set_hour, events, expected", [
    #Morning reminders
    (9, [generate_event(10, 0)], True),
    (9, [generate_event(11, 0)], True),
    (9, [generate_event(16, 0)], True),
    (9, [generate_event(17, 0)], False),
    #Daytime reminders
    (11, [generate_event(17, 0)], True),
    (12, [generate_event(17, 0)], True),
    (12, [generate_event(23, 0)], True),
    #Evening reminders
    (12, [generate_event(9, 1)], False),
    (13, [generate_event(9, 1)], True),
    (13, [generate_event(11, 1)], True),
    (13, [generate_event(12, 1)], False)
])
def test_isTimeToRemind_single_event(monkeypatch, set_hour, events, expected: bool):
    class mock_datetime:
        @classmethod
        def now(self, tz=None):
            return ( datetime.now(DEFAULT_TIMEZONE).replace(hour=set_hour).astimezone(tz) )
        @classmethod
        def utcnow(self):
            return ( self.now(timezone.utc) )
    
    monkeypatch.setattr(time_checks, 'datetime', mock_datetime)
    
    assert modules.isTimeToRemind(events) == expected
    

@pytest.mark.parametrize("set_hour", [9, 10, 12, 13, 23])
def test_time_bounds(monkeypatch, set_hour):
    days_diff = 1 if set_hour > LATE_HOUR else 0
    
    class mock_datetime:
        @classmethod
        def now(self, tz=None):
            return ( datetime.now(DEFAULT_TIMEZONE).replace(hour=set_hour).astimezone(tz) )
        @classmethod
        def utcnow(self):
            return ( self.now(timezone.utc) )
    
    monkeypatch.setattr(time_checks, 'datetime', mock_datetime)
    
    now = time_checks.datetime.now(DEFAULT_TIMEZONE)
    assert now.hour==set_hour

    time_bounds = time_checks.getTimeBounds()
    
    timeBegin = getTime(time_bounds['begin'])
    timeEnd = getTime(time_bounds['end'])
    
    if days_diff == 0:
        assert abs(timeBegin - now) < timedelta(seconds = 1)
    else:
        assert timeBegin.date() == now.date() + timedelta(days = days_diff)

        assert timeBegin.hour==0
        assert timeBegin.minute==0
        assert timeBegin.second==0
        
    assert timeEnd.hour==23
    assert timeEnd.minute==59
    assert timeEnd.second==59
    
    assert timeEnd > timeBegin
    assert timeEnd.date() == timeBegin.date()
    
