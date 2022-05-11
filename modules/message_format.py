from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import re

templates = {}
env = None

def initTemplate(name: str):
    global templates, env

    if env is None:
        env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    if name not in templates:
        templates[name] = env.get_template(f'{name}.j2')
    
    return templates[name]

def splitCommonSummary(events):
    total_summary = None
    summaries_equal = True
    pattern = re.compile('(?<=(?:- )|(?:, )|(?:: ))')

    for event in events:
        if total_summary == None:
            total_summary = pattern.split(event['summary'])
        else:
            event_summary = pattern.split(event['summary'])

            if len(total_summary) < len(event_summary):
                if summaries_equal:
                    total_summary.pop()

                summaries_equal = False

            if len(total_summary) > len(event_summary):
                summaries_equal = False
                while len(total_summary) >= len(event_summary):
                    total_summary.pop()

            for i, part in enumerate(total_summary):
                if part != event_summary[i]:
                    while len(total_summary) > i:
                        total_summary.pop()

                    summaries_equal = False

    total_summary = ''.join(total_summary)

    retEvents = []
    for event in events:
        event = event.copy()

        event['summary'] = event['summary'][len(total_summary):]

        retEvents.append(event)

    if not summaries_equal:
        total_summary = total_summary.strip()[:-1]

    return (total_summary.strip(), retEvents)

def telegram(events, diff) -> str:
    total_summary, events = splitCommonSummary(events)

    template = initTemplate('telegram_message')
    
    return template.render(total_summary=total_summary, events=events, diff=diff, datetime=datetime)

def web(content, html:bool=True):
    template = initTemplate('raise.html' if html else 'raise')
    
    return template.render(content=content)
