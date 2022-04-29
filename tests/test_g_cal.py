import unittest

from datetime import datetime, timezone, timedelta
from modules import g_cal

def test_work():
    assertIsNotNone( g_cal.get_incomig_events() )
