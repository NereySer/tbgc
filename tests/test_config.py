from modules.config import Config
from datetime import datetime

def test_work():
    now = datetime.now().isoformat()
    config = Config()

    config.last_send = now

    assert config.last_send == now
    
    config.last_send = '0000-00-00T00:00:00'
    
