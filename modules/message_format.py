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

def findCommon(list1, list2) -> (bool, list):
    retVal = []
    equal = len(list1) == len(list2)

    for i in range(min(len(list1), len(list2))):
        if list1[i] == list2[i]:
            retVal.append(list1[i])
        else:
            equal = False

            break

    return (equal, retVal)

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
        event_summary = pattern.split(event['summary'])

        if total_summary == None:
            total_summary = event_summary
        else:
            equal, common = findCommon(total_summary, event_summary)

            if (
                (equal != summaries_equal and len(common) == len(total_summary)) or
                (not equal and len(common) == len(event_summary))
            ):
                common.pop()

            summaries_equal &= equal
            total_summary = common

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
