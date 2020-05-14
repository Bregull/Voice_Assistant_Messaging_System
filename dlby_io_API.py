import os
import requests
import time
import json


api_url = 'https://api.dolby.com'


def get_upload_url(local_path, dolby_in_url, api_url, api_key):
    """
    get_upload_url returns a pre-signed URL for a cloud storage
    provider such as S3 or GCS where you will be able to PUT
    the contents of your file
    """
    url = api_url + '/media/input'

    # You need your api key as a header
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # This defines a url like dlb://foo that is temporary (~24h)
    # and only available to you with your api key
    body = {
        'url': dolby_in_url
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        data = response.json()

        return data['url']

    response.raise_for_status()

def upload_file(local_path, upload_url):
    """
    upload_file is the actual file upload, reading a local path
    on disk and putting it to the upload url returned from
    https://api.dolby.com/file/upload
    """
    with open(local_path, 'rb') as file_content:
        try:
            requests.put(upload_url, data=file_content)
        except ValueError as e:
            print(e)
            raise

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


def download(dolby_out_url, api_url, api_key, new_file_name):

    url = api_url + '/media/output' + '?url=' + dolby_out_url
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers, stream=True, allow_redirects=True)  # to get content after redirection
    print(response)
    if response.status_code == 200:
        with open(new_file_name, 'wb') as f:
            f.write(response.content)


# This is the function which includes every step
def dlby_API(local_path, dolby_in_url, dolby_out_url, new_file_name):
    #upload
    api_key = 'b6tGyxR4AuO0CWefbrMyBwJ0fBBcYS81'
    upload_url = get_upload_url(local_path, dolby_in_url, api_url, api_key)
    upload_file(local_path, upload_url)
    print("You can now use {} as your input for Media APIs.".format(dolby_in_url))
    #enhance
    noise(dolby_in_url, dolby_out_url, api_url, api_key)
    print("If successful, you can call /media/output with {} to download and hear the results.".format(dolby_out_url))
    #download
    download(dolby_out_url,api_url, api_key, new_file_name)

# The api_key from your account, local_path to your file, a dolby_url of your choosing
'''
local_path = '../../speech.wav'
dolby_in_url = 'dlb://input.wav'
dolby_out_url = 'dlb://output.wav'
new_file_name = 'new_speech.wav'
'''


def run_dlby_io():
    dlby_API()