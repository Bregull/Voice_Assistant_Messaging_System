import os
import time
import json
import requests

# We have different environments but typically you'll
# always use this endpoint
api_url = 'https://api.dolby.com'

# A limit on how long to poll for results
MAX_WAIT = 50

def job_start(api_url, api_key, dolby_in_url, dolby_out_url):
    """
    POST request will start a job to process your media.  This
    simple example only uses input / output parameters but check
    the API Reference documentation since many of the APIs allow
    additional parameters.
    """
    headers = {
        'x-apikey': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

    body = {
            'input' : dolby_in_url,
            'output': dolby_out_url,
        }

    response = requests.post(api_url, json=body, headers=headers)
    data = response.json()

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(json.dumps(data, indent=4, sort_keys=True))
        print(err)
        raise

    return data


def job_result(api_url, api_key, job_id, wait=0, noretry=False):
    """
    GET request to determine the status of a running process.  You
    use a job_id returned from job_start and wait for Success.
    To avoid running indefinitely, a wait parameter is used to delay
    additional polling calls.
    """
    headers = {
        'x-apikey': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

    params = {
        'job_id' : job_id,
        }

    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if noretry:
            return data

        # Retry with progressive backoff while job is being worked on
        if 'status' in data and data['status'] in ['Pending', 'Running']:
            # Limit how long and how many attempts we'll make
            if wait > MAX_WAIT:
                raise ValueError("Giving up after multiple attempts")

            wait = wait + 1
            time.sleep(wait)
            print('.')
            return job_result(api_url, api_key, job_id, wait=wait)

        return data
    else:
        print(job_id)

    response.raise_for_status()

def noise(dolby_in_url, dolby_out_url, api_url, api_key):
    url = api_url + '/media/enhance'

    result = job_start(url, api_key, dolby_in_url, dolby_out_url)
    job_id = result['job_id']
    print("Running job {}".format(job_id))

    data = job_result(url, api_key, job_id)
    print(json.dumps(data, indent=4, sort_keys=True))




# The api_key from your account, dolby dlb:// url created in an earlier step, and
# a dolby dlb:// url that will created on-the-fly to output your result
api_key = 'b6tGyxR4AuO0CWefbrMyBwJ0fBBcYS81'
dolby_in_url = 'dlb://input.wav'
dolby_out_url = 'dlb://output.wav'

noise(dolby_in_url, dolby_out_url, api_url, api_key)
print("If successful, you can call /media/output with {} to download and hear the results.".format(dolby_out_url))