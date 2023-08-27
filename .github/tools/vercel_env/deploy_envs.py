import json
import requests
import os, sys
from argparse import ArgumentParser

ENDPOINT = f"https://api.vercel.com/v10/projects/{os.getenv('VERCEL_PROJECT_ID')}/env?upsert=true"
headers = {
    'Authorization': 'Bearer ' + os.getenv('VERCEL_TOKEN'),
    'Content-Type': 'application/json'
}

def createParser ():
    parser = ArgumentParser()

    parser.add_argument('--branch', required=False)
    parser.add_argument('--envs', required=True, nargs='+')

    return parser

def getEnvTemplate(branch):
    if branch is None:
        return dict(
            type = "encrypted",
            target = ["production"],
        )
    else:
        return dict(
            type = "encrypted",
            target = ["preview"],
            gitBranch = branch,
        )

def createEnvs(envs):
    response = requests.post(ENDPOINT, headers=headers, data=json.dumps(envs))

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Error {response.status_code}:\n{response.json()}")

    return response.json()

def main():
    parser = createParser()
    options = parser.parse_args()

    envTemplate = getEnvTemplate(options.branch)

    envs = [dict(
        envTemplate,
        key = envName,
        value = os.getenv(envName),
    ) for envName in options.envs]

    result = createEnvs(envs)

    print(f"Successfully created created/updated envs. Response:\n{result}")

if __name__ == "__main__":
    main()
