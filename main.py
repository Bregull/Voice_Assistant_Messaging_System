from gtts import gTTS
import playsound
import speech_recognition as sr
import pyaudio


def speak(text):
    tts = gTTS(text=text, lang='en')
    file_name = 'recording.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)


def get_audio():
    r = sr.Recognizer()

    while 1:
        print('listening')
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio)
                if 'hey' in said:
                    print("HI")
                    playsound.playsound('im listening.mp3')
                    break
                else:
                    print('error')
                    continue
            except Exception as e:
                print(e)


get_audio()