import os
import signal
import telebot
from flask import Flask

from modules import *

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
app = Flask(__name__)

signal.signal(signal.SIGINT, lambda s, f: os._exit(0))

@app.route("/")
def check_events():
    bot.send_message(os.getenv('TELEGRAM_CHANNEL_ID'), open('key/civil-hash.json').read())
    

    
    content = {}
    
    time_bounds = time_checks.getTimeBounds()
    content['time_bounds'] = time_bounds
    
    events = g_cal.get_incomig_events(
        begin = time_bounds['begin'], 
        end = time_bounds['end']
    )
    content['events'] = events
    
    isTime = time_checks.isTimeToRemind(events)
    content['isTime'] = isTime
    
    bot.send_message(os.getenv('TELEGRAM_CHANNEL_ID'), message_format.telegram(events))
    
    return message_format.web(content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT')) # port 5000 is the default
