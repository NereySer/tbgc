import pytest

from modules import message_format
from datetime import datetime, timedelta

def generate_event(hour, text):
    return {
        'summary': text,
        'start': {
            'dateTime': '2022-05-03T$(hour):00:00+03:00'
        }
    }
    
@pytest.mark.parametrize("events, diff, expected", [
    ([
        generate_event(19, 'test')
    ], 0, 'Сегодня, вторник, test в 19:00'),
    ([
        generate_event(19, 'test')
    ], 1, 'Завтра, вторник, test в 19:00'),
    ([
        generate_event(19, 'test'),
        generate_event(20, 'second_test')
    ], 0, 'Сегодня, вторник
19:00 - test
20:00 - second_test')
])
def test_work(events, diff, expected):
    message_format.telegram(events, diff) == expected
