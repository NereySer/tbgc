import os
import signal
import telebot
from flask import Flask, request

from datetime import datetime, timedelta

from modules import *

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
app = Flask(__name__)

signal.signal(signal.SIGINT, lambda s, f: os._exit(0))

class Content(object):
    pass

@app.route("/")
def show_next_notification():
    content = Content()
    
    content.now = datetime.now(time_checks.DEFAULT_TIMEZONE)
    
    content.config = config.Config()

    content.time_bounds = time_checks.getTimeBounds(datetime.fromisoformat(content.config.last_time))

    while not (events := g_cal.get_incomig_events( *content.time_bounds )):
        if content.time_bounds[0] - content.now > timedelta(days = 7):
            break
            
        content.time_bounds[0] = time_checks.setDateToBeginOfDay(content.time_bounds[0] + timedelta(days = 1))
        content.time_bounds[1] = content.time_bounds[1] + timedelta(days = 1)
        
    if events:
        content.notification = message_format.telegram(events, (content.last_event.date()-content.now.date()).days)
        
        content.time = now
        
    return message_format.notifications(content)
        
@app.route("/check_events")
def check_events():
    if os.getenv('CHECK_KEY') != request.args.get('key', default = '', type = str):
        return 'Not found', 404
    
    content = Content()
    
    content.now = datetime.now(time_checks.DEFAULT_TIMEZONE)
    
    content.config = config.Config()
    
    content.time_bounds = time_checks.getTimeBounds()
    
    content.events = g_cal.get_incomig_events( *content.time_bounds )
    
    content.isTime, content.last_event = time_checks.isTimeToRemind(content.events)
    
    content.should_remind = content.isTime and datetime.fromisoformat(content.config.last_time) < content.last_event
    
    if content.should_remind:
        bot.send_message( os.getenv('TELEGRAM_CHANNEL_ID'), message_format.telegram(content.events, (content.last_event.date()-content.now.date()).days))
        
        content.config.last_time = str(content.last_event)
    
    return message_format.raise_notification(content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT')) # port 5000 is the default
