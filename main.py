from gtts import gTTS
import playsound
import speech_recognition as sr
import pyaudio
import requests

def dlby_io():
    headers = {
        'x-api-key': 'b6tGyxR4AuO0CWefbrMyBwJ0fBBcYS81',
    }

    data = '{\n          "url": "dlb://in/speech.wav"\n          }'

    response = requests.post('https://api.dolby.com/media/input', headers=headers, data=data)
    print(response)
    print(response.json())

    url = 'https://generic-prod-dlbops-cloud-files.s3-accelerate.amazonaws.com/04e30ada-5785-4819-be06-71dfeb4a1dd3/in/speech.wav?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA2N2ZL3VQIHNJAXFJ%2F20200415%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200415T065247Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEG8aCXVzLXdlc3QtMiJGMEQCIFn%2F2JfDnqt7jUdk2Wex4nsPM4b3UUHl5DRJe782Q%2Bk%2BAiA2y3nm66rfc3fTbLpXT%2Bb47GpUptkDOqe59JqvQfdfKCrgAQiI%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDcxNjkxMDA5MTYxNiIM5RUfRS8yDdHBhal1KrQB%2FceDIwUow5iZIhfwws0TaTZTEBZSJXs0aDAQBzZ5vp1h2Yx8TneCdr2r0JJHw%2BT6YeZ7tm72bGDHNt4egQkrEfs9b7ppwKw0nCXPNvGcbNhhrdOmWxkstkoXv0%2FqJcnLaY4uYbLWSXVyL%2F6APrzp94LDuzeKj8gGziyt1SQCAv%2BHFNZ99kkYgJ4k4zVheZ250SbVK0Ha2rvjCCnIdtGWh9N5sqBp2NYrftKcEbWsjMbUBa%2FbML7e2vQFOuEBqltfBqfAjLUc80VC%2B331xbcQoTDrDQLrEqZwxP1wTX2LCpPhETkWuDcmQDVfjDHvwl7ADijt9m1j0ubcuxAhYHp3tmG1EqavKdCzgaG%2BwwQ18Iyf9pZqnxe5%2BD1CitvpTs43IIzuA%2B5n5Is1583ZCf9LV5EiuaE%2BfOkhuyj9TDqaopOeHtNHLZo3PqnTsi6LjyPhIrKgRE%2B7KI4T1w48PPeYTDc4lfe%2FQ%2B9%2F67J3n5ehBfn2woqmzTtMcTIh52hJIhR75Ol1Cs%2Blz0CxQqVCANDm%2F9S4Uaxi25Yrmk%2FIe3By&X-Amz-Signature=38328b28f70307ce7acdbfd5e4f0e3311c258defa58ecd18c76c9b7ef1373074&X-Amz-SignedHeaders=host'
    response = requests.put(url, headers=headers, data='./speech.wav')
    print(response)

    data = '{\n          "input": "dlb://speech.wav",\n          "output": "dlb://output.wav"\n          }'

    response = requests.post('https://api.dolby.com/media/enhance', headers=headers, data=data)
    print(response)
    print(response.json())

    params = (
        ('url', 'dlb://example/output.wav'),
    )

    response = requests.get('https://api.dolby.com/media/output', headers=headers, params=params)
    print(response)

    params = (
        ('url', 'dlb://out/output.wav'),
    )

    response = requests.get('https://api.dolby.com/media/output', headers=headers, params=params)

    print(response)


def speak(text):
    tts = gTTS(text=text, lang='en')
    file_name = 'recording.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)
 
def record(r, source):
    audio = r.listen(source)
    with open('speech.wav', 'wb') as f:
        f.write(audio.get_wav_data())

def to_text(r):
    demo = sr.AudioFile('speech.wav')
    with demo as source:
        r.adjust_for_ambient_noise(source, offset=0.5)
        audio = r.record(source)
        f = open('speech_text.txt', "w", encoding="utf-8")
        text = r.recognize_google(audio)
        f.write(text)
        f.close()

def get_audio():
    r = sr.Recognizer()

    while 1:
        print('listening')
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio)
                if 'hey' in said:
                    print("HI")
                    playsound.playsound('im_listening.mp3')
                    record(r, source)
                    to_text(r)
                    break
                else:
                    print('error')
                    continue
            except Exception as e:
                print(e)


#get_audio()
dlby_io()