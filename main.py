from gtts import gTTS
import playsound
import speech_recognition as sr
import pyaudio
import requests

def dlby_io():
    headers = {"x-api-key": "b6tGyxR4AuO0CWefbrMyBwJ0fBBcYS81"}

    data = '{"url": "dlb://in/speech.wav"}'

    response = requests.post('https://api.dolby.com/media/input', headers=headers, data=data)
    print(response)
    print(response.json())

    url = response.json()['url']
    response = requests.put(url, headers=headers, data='./speech.wav')
    print(response)

    data = '{\n          "input": "dlb://speech.wav",\n          "output": "dlb://output.wav"\n          }'

    response = requests.post('https://api.dolby.com/media/enhance', headers=headers, data=data)
    print(response)
    print(response.json())

    data = response.json()

    response = requests.get('https://api.dolby.com/media/enhance', headers=headers, params=data)
    print(response)

    data = '{"url": "dlb://output.wav"}'

    response = requests.get('https://api.dolby.com/media/output?url=dlb://output.wav', headers=headers, stream=True)

    print(response)
    print(response.json())


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