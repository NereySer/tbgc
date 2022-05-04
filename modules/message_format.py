from jinja2 import Template

template = None

def initTemplate():
    global template
    if template is None:
        j2 = open('templates/telegram_message.j2').read()
        template = Template(j2)

def format(events) -> str:
    initTemplate()
    
    return template.render(events=events)
