from jinja2 import Template

templates = {}

def initTemplate(name: str):
    global templates
    
    if templates[name] is None:
        j2 = open(f'templates/{name}.j2').read()
        
        templates[name] = Template(j2, trim_blocks=True, lstrip_blocks=True)
    
    return templates[name]

def format(events) -> str:
    template = initTemplate('telegram_message')
    
    return template.render(events=events)
