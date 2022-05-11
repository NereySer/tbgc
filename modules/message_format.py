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

def findCommon(list1, list2, strict) -> (bool, list):
    if len(list1) < len(list2):
        if strict:
            list1.pop()

        strict = False

    if len(list1) > len(list2):
        strict = False
        while len(list1) >= len(list2):
            list1.pop()

    for i, part in enumerate(list1):
        if part != list2[i]:
            while len(list1) > i:
                list1.pop()

            strict = False
     
    return (strict, list1)

def cutSummary(events, num):
    retEvents = []
    for event in events:
        event = event.copy()

        event['summary'] = event['summary'][num:]

        retEvents.append(event)
        
    return retEvents

def splitCommonSummary(events):
    total_summary = None
    summaries_equal = True
    pattern = re.compile('(?<=(?:- )|(?:, )|(?:: ))')

    for event in events:
        if total_summary == None:
            total_summary = pattern.split(event['summary'])
        else:
            summaries_equal, total_summary = findCommon(total_summary, pattern.split(event['summary']), summaries_equal)

    total_summary = ''.join(total_summary)

    retEvents = cutSummary(events, len(total_summary))

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
