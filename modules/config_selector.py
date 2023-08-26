import os
from . import config, config_redis

def Config():
    if 'KV_URL' in os.environ and \
        'KV_REST_API_URL' in os.environ and \
        'DEPLOY' in os.environ:
        return config_redis.Config(os.getenv('DEPLOY'))
    elif 'DATABASE_URL' in os.environ:
        return config.Config()
    else:
      raise Exception('No connection for database specified')
