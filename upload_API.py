import os
import requests

# We have different environments but typically you'll
# always use this endpoint
api_url = 'https://api.dolby.com'


def get_upload_url(local_path, dolby_url, api_url, api_key):
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
        'url': dolby_url
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

# The api_key from your account, local_path to your file, a dolby_url of your choosing
api_key = 'b6tGyxR4AuO0CWefbrMyBwJ0fBBcYS81'
local_path = '/Users/jacekfica/Documents/GitHub/Voice_Assistant_Messaging_System/speech.wav'
dolby_url = 'dlb://input.wav'

# This is the sequence of uploading in 2 steps
upload_url = get_upload_url(local_path, dolby_url, api_url, api_key)
upload_file(local_path, upload_url)
print("You can now use {} as your input for Media APIs.".format(dolby_url))