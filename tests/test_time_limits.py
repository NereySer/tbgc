import unittest

from datetime import datetime, timezone, timedelta
from modules import time_limits as t

def test_start_time():
    startTime = t.getStart()

    assert timeStart[-1]=='Z'
    assert abs(datetime.fromisoformat(timeStart[:-1])-datetime.utcnow())<timedelta(seconds = 1)

def test_end_time():
    endTime = t.getEnd()
    
    assert timeStart[-1]=='Z'
    
    endTime = datetime.fromisoformat(endTime[:-1])
    
    assert endTime.hour==23
    assert endTime.minute==59
    assert endTime.second==59
    
def test_time_difference():
    startTime = t.getStart()
    endTime = t.getEnd()
    
    startTime = datetime.fromisoformat(startTime[:-1])
    endTime = datetime.fromisoformat(endTime[:-1])
    
    diff = endTime - startTime
    
    assert endTime >= startTime
    assert (endTime - startTime) < timedelta(days = 2)
