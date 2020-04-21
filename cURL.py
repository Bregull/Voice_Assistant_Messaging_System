import requests

headers = {"x-api-key": "b6tGyxR4AuO0CWefbrMyBwJ0fBBcYS81"}
data = '{"url": "dlb://in/speech.wav"}'
response = requests.post('https://api.dolby.com/media/input', headers=headers, data=data)

print(response)
print(response.json())

url = response.json()['url']
response = requests.put(url, headers=headers, data='./speech.wav')

print(response)

data = '{\n          "input": "dlb://in/speech.wav",\n          "output": "dlb://out/output.wav"\n          }'
response = requests.post('https://api.dolby.com/media/enhance', headers=headers, data=data)

print(response)
print(response.json())

data = response.json()
response = requests.get('https://api.dolby.com/media/enhance', headers=headers, params=data)

print(response)

data = '{"url": "dlb://out/output.wav"}'
response = requests.get('https://api.dolby.com/media/output?url=dlb://out/output.wav', headers=headers, allow_redirects=True, stream=False)

print(response)
print(response.json())