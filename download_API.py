import requests

api_url = 'https://api.dolby.com'

headers = {
        'x-api-key': 'b6tGyxR4AuO0CWefbrMyBwJ0fBBcYS81',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

url = api_url + '/media/output' + '?url=dlb://output.wav'

#response = requests.get(url, headers=headers, allow_redirects=False)

#print(response.url)

response = requests.get(url, headers=headers, stream=True, allow_redirects=True)  # to get content after redirection
print (response)
if response.status_code == 200:
    with open('new_speech.wav', 'wb') as f:
        f.write(response.content)

