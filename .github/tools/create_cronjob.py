import json
import requests
import os
from argparse import ArgumentParser

ENDPOINT = 'https://api.cron-job.org'
headers = {
    'Authorization': 'Bearer ' + os.getenv('CRONJOB_API_KEY'),
    'Content-Type': 'application/json'
}

def createParser ():
    parser = ArgumentParser()

    parser.add_argument('-t', '--title', required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--hours', required=True, type=int, nargs='+')

    return parser

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

def removeDuplicatedJobs(jobs):
    while len(jobs) > 1:
        job = filtered_jobs.pop()

        deleteJob(job['jobId'])

        print('Successfully deleted job {}'.format(job['jobId']))

def updateJob(target_job, jobs):
    removeDuplicatedJobs(jobs)

    job_info = getJobInfo(jobs[0]['jobId'])

    job_info['jobDetails'] = {
        key: value for key, value in job_info['jobDetails'].items() if key in target_job['job']
    }

    if target_job['job'] == job_info['jobDetails']:
        updateJob(filtered_jobs[0]['jobId'], job_info_create)

        return True

    return False

def main():
    parser = createParser()
    options = parser.parse_args()
    job_info_create = createJobDetails()

    result = getJobs()

    filtered_jobs = list(filter(lambda job: job['title'] == options.title, result['jobs']))

    if not filtered_jobs:
        jobId = createJob(job_info_create)

        print('Successfully created job {}'.format(jobId))
    elif updateJob(job_info_create, filtered_jobs):
        print('Successfully patched job {}'.format(filtered_jobs[0]['jobId']))
    else:
        print('Job {} is already present'.format(filtered_jobs[0]['jobId']))

if __name__ == "__main__":
    main()
