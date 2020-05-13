from gtts import gTTS
import playsound
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()


def speak(text):
    tts = gTTS(text=text, lang='en')
    file_name = 'recording.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)


def record(r, source):
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    with open('speech1.wav', 'wb') as f:
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

def activate(phrase = 'welcome'):
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            transcript = r.recognize_google(audio)
            if transcript.lower() == phrase:
                return True
            else:
                return False
    except:
        pass


def get_audio():
    if activate() == True:
        try:
            with mic as source:
                print("HI")
                playsound.playsound('listening.mp3')
                record(r, source)
                # to_text(r)
        except Exception as e:
            print(e)
    else:
        pass



while True:
    get_audio()



