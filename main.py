from gtts import gTTS
import playsound
import speech_recognition as sr
import pyaudio


def speak(text):
    tts = gTTS(text=text, lang='en')
    file_name = 'recording.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)
 
def record(r, source):
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    with open('speech.wav', 'wb') as f:
        f.write(audio.get_wav_data())

def record(r, source):
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    with open('speech.wav', 'wb') as f:
        f.write(audio.get_wav_data())


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
<<<<<<< HEAD
                    playsound.playsound('im_listening.mp3')
=======
                    playsound.playsound('im listening.mp3')
>>>>>>> 8fcda1d0dea1f093ee451208d6fdbaa2432d5c77
                    record(r, source)
                    break
                else:
                    print('error')
                    continue
            except Exception as e:
                print(e)


get_audio()
