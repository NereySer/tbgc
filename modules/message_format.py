from flask import render_template

def format(events) -> str:
    return render_template('templates/telegram_message', events=events)
