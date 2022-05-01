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
    
def test_time_difference(monkeypatch):
    def mock_datetime_now(tzinfo: timezone):
        return ( datetime.now(tzinfo).replace(hour=10) )

    monkeypatch.setattr(time_limits.datetime, "now", mock_datetime_now)
    
    timeStart = time_limits.getStart()
    timeEnd = time_limits.getEnd()
    
    timeStart = datetime.fromisoformat(timeStart[:-1]).replace(tzinfo=timezone.utc).astimezone(time_limits.DEFAULT_TIMEZONE)
    timeEnd = datetime.fromisoformat(timeEnd[:-1]).replace(tzinfo=timezone.utc).astimezone(time_limits.DEFAULT_TIMEZONE)
    
    assert timeEnd.hour==10
    assert timeEnd > timeStart
    assert (timeEnd - timeStart) < timedelta(days = 1)
