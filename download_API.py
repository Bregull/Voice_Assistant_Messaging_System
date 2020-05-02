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
if response.status_code == 200:
    with open('new_speech.wav', 'wb') as f:
        f.write(response.content)

print(response)
#print(response.url)  # http://github.com, not https.
#print(response.headers['Location'])
#print(response.raise_for_status())
#print(data=response.json())


#data = '{"url": "dlb://out/output.wav"}'

#response = requests.get('https://api.dolby.com/media/output?url=dlb://output.wav', headers=headers)

#data = response.json()
#print(data)
print(response)
#print(response.json())
print(response.content)