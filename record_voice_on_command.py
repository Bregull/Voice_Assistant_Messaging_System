from gtts import gTTS
import playsound
import speech_recognition as sr
from dlby_io_API import dlby_API
from datetime import datetime
import os, errno

def speak(text):
    tts = gTTS(text=text, lang='en')
    file_name = 'recording.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)


def record(r, source, name):
    r.adjust_for_ambient_noise(source, duration=0.2)
    audio = r.listen(source)
    with open('./recorded/' + name, 'wb') as f:
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
            audio = r.listen(source, phrase_time_limit=2)
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
                name = names()
                print("HI")
                playsound.playsound('listening.mp3')
                record(r, source, name)
                dlby_API('./recorded/' + name, 'dlb://input/' + name, 'dlb://output/' + name, './enhanced/enhanced_' +  name)
                print('stoped')
                # to_text(r)
        except Exception as e:
            print(e)
    else:
        pass

def names():
    now = datetime.now()
    now_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    filename = web_name + '_' + now_string + '.wav'
    return filename

def create_directory():
    try:
        os.makedirs('recorded')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    try:
        os.makedirs('enhanced')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def personal_ID():
    filename = 'ID.txt'
    if os.path.exists(filename):
        file = open(filename, 'r')
        name = file.readline()
        return name
    else:
        file = open(filename, 'w')
        name = input('Your name: ')
        file.write(name)
        file.close()
        return name




web_name = personal_ID()
r = sr.Recognizer()
mic = sr.Microphone()
create_directory()
r.pause_threshold = 1.5
with mic as source:
    r.adjust_for_ambient_noise(source)
while True:
    print('waiting')
    get_audio()




