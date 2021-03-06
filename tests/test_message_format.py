import pytest

from modules import message_format
from modules.g_cal import Events
from datetime import datetime, timedelta
from tests.tools import g_cal_event

class Content(object):
    pass

def generate_event(hour, text, transparent = False):
    return g_cal_event(hour, text=text, transparent = transparent, base_date = datetime.now().replace(minute=0))

@pytest.mark.parametrize("events, diff, expected", [
    ([
        generate_event(19, 'test')
    ], 0, 'Сегодня вторник, test в 19:00'),
    ([
        generate_event(19, 'test')
    ], 1, 'Завтра среда, test в 19:00'),
    ([
        generate_event(19, 'test'),
        generate_event(20, 'second_test')
    ], 0, 'Сегодня вторник\n19:00 - test\n20:00 - second_test'),
    #Test agregation
    ([
        generate_event(19, 'test'),
        generate_event(20, 'test')
    ], 0, 'Сегодня вторник, test в 19:00 и 20:00'),
    ([
        generate_event(11, 'test'),
        generate_event(15, 'test'),
        generate_event(19, 'test'),
        generate_event(20, 'test')
    ], 0, 'Сегодня вторник, test в 11:00, 15:00, 19:00 и 20:00'),
    ([
        generate_event(19, 'test - first'),
        generate_event(20, 'test - second_test')
    ], 0, 'Сегодня вторник, test\n19:00 - first\n20:00 - second_test'),
    ([
        generate_event(19, 'test - t - first'),
        generate_event(20, 'test - t - second_test'),
        generate_event(21, 'test - 3_test'),
        generate_event(22, 'test - 4_test')
    ], 0, 'Сегодня вторник, test\n19:00 - t - first\n20:00 - t - second_test\n21:00 - 3_test\n22:00 - 4_test'),
    ([
        generate_event(19, 'test: first'),
        generate_event(20, 'test: second_test')
    ], 0, 'Сегодня вторник, test\n19:00 - first\n20:00 - second_test'),
    #Test events with displaying end time
    ([
        generate_event(11, 'test'),
        generate_event(15, 'test', True),
        generate_event(19, 'test'),
        generate_event(20, 'test')
    ], 0, 'Сегодня вторник, test в 11:00, с 15:00 до 16:00, в 19:00 и 20:00'),
    ([
        generate_event(11, 'test', True),
        generate_event(15, 'test'),
        generate_event(19, 'test'),
        generate_event(20, 'test'),
    ], 0, 'Сегодня вторник, test с 11:00 до 12:00, в 15:00, 19:00 и 20:00'),
    ([
        generate_event(19, 'test: first', True),
        generate_event(20, 'test: second_test', True),
    ], 0, 'Сегодня вторник, test\n19:00-20:00 - first\n20:00-21:00 - second_test'),
    ([
        generate_event(19, 'test: first'),
        generate_event(20, 'test: second_test', True),
    ], 0, 'Сегодня вторник, test\n19:00 - first\n20:00-21:00 - second_test'),
    #Test whole day events
    ([
        generate_event(-1, 'whole day'),
    ], 0, 'Сегодня вторник, whole day'),
    ([
        generate_event(-1, 'whole day'),
        generate_event(-1, 'test'),
        generate_event(19, 'test'),
        generate_event(20, 'test'),
    ], 0, 'Сегодня вторник\nwhole day\ntest\ntest в 19:00 и 20:00'),
    ([
        generate_event(-1, 'test'),
        generate_event(-1, 'test2'),
    ], 0, 'Сегодня вторник\ntest\ntest2'),
])
def test_work(events, diff, expected):
    base_date=datetime.fromisoformat("2022-05-03T00:00:00+03:00")

    content = Content()

    content.events = Events(events, base_date + timedelta(days=diff))
    content.time = base_date

    assert message_format.telegram(content) == expected
