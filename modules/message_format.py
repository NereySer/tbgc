from jinja2 import Template

template = None

def initTemplate():
    if template == None:
        html = open('foopkg/templates/0.hello.html').read()
        template = Template(html)

def format(events) -> str:
    initTemplate()
    
    return template.render(events=events)
