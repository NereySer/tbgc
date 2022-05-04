
def format(events) -> str:
    return render_template('templates/telegram_message', events=events)
