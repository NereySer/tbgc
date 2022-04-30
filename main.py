import os
import signal
import telebot
from flask import Flask

from buzz import generator

print( dir() )
import modules
print( dir() )
print( dir( modules ) )

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
app = Flask(__name__)

signal.signal(signal.SIGINT, lambda s, f: os._exit(0))

@app.route("/")
def generate_buzz():
    content = generator.generate_buzz() + '\n'
    content += modules.g_cal.get_incomig_events(
        begin = modules.time_limits.getStart(), 
        end = modules.time_limits.getEnd()
    )
    
    bot.send_message(os.getenv('TELEGRAM_CHANNEL_ID'), content)
    
    page = '<html><body><h1>'
    page += content.replace('\n', '</br>')
    page += '</h1></body></html>'
    return page

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT')) # port 5000 is the default
