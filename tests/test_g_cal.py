from datetime import datetime, timedelta
from modules.time_checks import DEFAULT_TIMEZONE
from tests.tools import g_cal_event
import pytest

from modules import g_cal

def google_event(hour, days_add = 0, text = '', duration = 1, transparent = False, base_date = None):
    if base_date is None:
        base_date = datetime.now(DEFAULT_TIMEZONE)

    retVal = {
        'summary': text,
        'transparency': ('transparent' if transparent else 'opaque')
    }

    if hour == -1:
        start_time = base_date.date() + timedelta(days = days_add)

        delta_duration = timedelta(days = duration)

        key_name = 'date'
    else:
        start_time = base_date.replace(hour=hour) + timedelta(days = days_add)

        delta_duration = timedelta(hours = duration)

        key_name = 'dateTime'

    retVal['start'] = {
            key_name: start_time.isoformat()
    }

    retVal['end'] = {
            key_name: (start_time + delta_duration).isoformat()
    }

    return retVal

def test_work():
    assert g_cal.get_incomig_events(
        begin = datetime.utcnow(),
        end = datetime.utcnow().replace(hour=23, minute=59, second=59)
    ) is not None

    with pytest.raises(Exception):
        g_cal.get_incomig_events(
            begin = datetime.utcnow(),
            end = datetime.utcnow() + timedelta(days=1)
        )

base_date = datetime.now(DEFAULT_TIMEZONE)
@pytest.mark.parametrize("google_events, expected", [
    (
        [],
        ([], [])
    ),
    (
        [google_event(10, text='test', base_date = base_date)],
        ([], [g_cal_event(10, text='test', base_date = base_date)])
    ),
    (
        [google_event(-1, text='test')],
        (['test'], [])
    ),
])
def test_mock(monkeypatch, google_events, expected):
    class mock_event_result:
        @classmethod
        def get(self, par1, par2):
            return google_events

    class mock_list:
        @classmethod
        def execute(self):
            return mock_event_result

    class mock_events:
        @classmethod
        def list(self,
            calendarId,
            timeMin, timeMax,
            singleEvents,
            orderBy
        ):
            return mock_list

    class mock_g_service:
        @classmethod
        def events(self):
            return mock_events

    monkeypatch.setattr(g_cal, 'g_service', mock_g_service)

    now = datetime.utcnow()
    events = g_cal.get_incomig_events(
        begin = now,
        end = now.replace(hour=23, minute=59, second=59)
    )

    assert events.total == expected[0]
    assert events.timed == expected[1]
    assert events.date == now
