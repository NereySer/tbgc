import unittest

from datetime import datetime, timezone, timedelta

from modules import time_limits

def test_start_time():
    timeStart = time_limits.getStart()

    assert timeStart[-1]=='Z'
    
    timeStart = datetime.fromisoformat(timeStart[:-1])
    
    assert timeStart.tzinfo==None
    
    assert abs(timeStart - datetime.utcnow()) < timedelta(seconds = 1)

def test_end_time():
    timeEnd = time_limits.getEnd()
    
    assert timeEnd[-1]=='Z'
    
    timeEnd = datetime.fromisoformat(timeEnd[:-1])

    assert timeEnd.tzinfo==None

    timeEnd = timeEnd.replace(tzinfo=timezone.utc).astimezone(time_limits.DEFAULT_TIMEZONE)
    
    assert timeEnd.hour==23
    assert timeEnd.minute==59
    assert timeEnd.second==59

@pytest.mark.parametrize("set_hour, days_diff", [(9, 0), (10, 0), (12, 0), (13, 1), (23, 1)])
def test_time_difference(monkeypatch, set_hour, days_diff):
    class mock_datetime:
        @classmethod
        def now(self, tz=None):
            return ( datetime.now(time_limits.DEFAULT_TIMEZONE).replace(hour=set_hour).astimezone(tz) )
        @classmethod
        def utcnow(self):
            return ( self.now(timezone.utc) )
    
    monkeypatch.setattr(time_limits, 'datetime', mock_datetime)
    
    timeStart = time_limits.getStart()
    timeEnd = time_limits.getEnd()
    
    timeStart = datetime.fromisoformat(timeStart[:-1]).replace(tzinfo=timezone.utc).astimezone(time_limits.DEFAULT_TIMEZONE)
    timeEnd = datetime.fromisoformat(timeEnd[:-1]).replace(tzinfo=timezone.utc).astimezone(time_limits.DEFAULT_TIMEZONE)
    timeEnd -= timedelta(days = days_diff)
    
    assert timeStart.hour==set_hour
    assert timeEnd > timeStart
    assert (timeEnd == timeStart) < timedelta(days = 1)
