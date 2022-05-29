import json
import requests
import os
from argparse import ArgumentParser

def createParser ():
    parser = ArgumentParser()

    parser.add_argument('-t', '--title', required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--hours', required=True, type=int, nargs='+')

    return parser

ENDPOINT = 'https://api.cron-job.org'

def getLink(jobId = None):
    if jobId is None:
        return '{}/jobs'.format(ENDPOINT)
    else:
        return '{}/jobs/{}'.format(ENDPOINT, jobId)

def createJobDetails():
    return {
        "job": {
            'enabled': True,
            'title': options.title,
            'saveResponses': True,
            'url': options.url,
            'auth': {
                'enable': False,
                'user': '',
                'password': ''
            },
            'notification': {
                'onFailure': True,
                'onSuccess': True,
                'onDisable': True
            },
            'extendedData': {
                'headers': [],
                'body': ''
            },
            'type': 0,
            'requestTimeout': 30,
            'redirectSuccess': False,
            'schedule': {
                'timezone': 'Europe/Moscow',
                'hours': options.hours,
                'mdays': [-1],
                'minutes': [0],
                'months': [-1],
                'wdays': [-1]
            },

            'requestMethod': 0
        }
    }

headers = {
    'Authorization': 'Bearer ' + os.getenv('CRONJOB_API_KEY'),
    'Content-Type': 'application/json'
}

def getJobs():
    return requests.get(getLink(), headers=headers).json()

def deleteJob(jobId):
    response = requests.delete(getLink(jobId), headers=headers)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception('Error {} while deleting {}'.format(response.status_code, job['jobId']))

def getJobInfo(jobId):
    return requests.get(getLink(jobId), headers=headers).json()

def updateJob(jobId, jobInfo):
    response = requests.patch(getLink(jobId), headers=headers, data=json.dumps(jobInfo))

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception('Error {} while patching {}'.format(response.status_code, jobId))

def createJob(jobInfo):
    response = requests.put(getLink(), headers=headers, data=json.dumps(jobInfo))

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception('Error {} while creating'.format(response.status_code))

    return response.json()['jobId']

parser = createParser()
options = parser.parse_args()
job_info_create = createJobDetails()

result = getJobs()

filtered_jobs = list(filter(lambda job: job['title'] == options.title, result['jobs']))

if filtered_jobs:
    while len(filtered_jobs) > 1:
        job = filtered_jobs.pop()

        deleteJob(job['jobId'])

        print('Successfully deleted job {}'.format(job['jobId']))

    job_info = getJobInfo(filtered_jobs[0]['jobId'])

    job_info['jobDetails'] = {
        key: value for key, value in job_info['jobDetails'].items() if \
        not key.startswith('last') and
        not key.startswith('next') and
        key != 'jobId'
    }

    if job_info_create['job'] == job_info['jobDetails']:
        print('Job {} is already present'.format(filtered_jobs[0]['jobId']))

        exit()

    updateJob(filtered_jobs[0]['jobId'], job_info_create)

    print('Successfully patched job {}'.format(filtered_jobs[0]['jobId']))
else:
    jobId = createJob(job_info_create)

    print('Successfully created job {}'.format(jobId))
