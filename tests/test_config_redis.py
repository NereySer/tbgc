from modules.config_redis import Config
from datetime import datetime

def test_work():
    now = datetime.now().isoformat()
    config = Config('autotests')
    
    tmp = config.last_time

    assert tmp == '0001-01-01T00:00:00+00:00'

    config.last_time = now

    assert config.last_time == now
    
    config.last_time = tmp
