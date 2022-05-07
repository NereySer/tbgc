import pytest

from modules import message_format
from datetime import datetime, timedelta

@pytest.mark.parametrize("events", [
    ([
        {
            'summary': 'test',
            'start': {
                'dateTime': '2022-05-03T19:00:00+03:00'
            }
        }
    ]),
    ([
        {
            'summary': 'test',
            'start': {
                'dateTime': '2022-05-03T19:00:00+03:00'
            }
        }, 
        {
            'summary': 'second_test',
            'start': {
                'dateTime': '2022-05-03T20:00:00+03:00'
            }
        }
    ])
])
def test_work(events):
    message_format.telegram(events, 0)
    message_format.telegram(events, 1)
    message_format.telegram(events, 2)
