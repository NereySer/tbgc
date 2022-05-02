from modules import message_format

def test_work():
    assert message_format.format([
        {
            'summary': 'test',
            'start': {
                'datetime': '2022-05-03T19:00:00+03:00'
            }
        }
    ]) == '2022-05-03T19:00:00+03:00 test\n'
    
