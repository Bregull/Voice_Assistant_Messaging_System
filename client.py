import tkinter
from threading import Thread
import socket
from gtts import gTTS
import playsound
import speech_recognition as sr
from dlby_io_API import dlby_API
from datetime import datetime
import prepare_os_files
from dlby_io_API import download as dolby_download
import platform
import notification_win

### OBUDUJ W KLASE NA DOLE, CZY TEŻ W FUNKCJE! ###


'''
Globals
'''
r = sr.Recognizer()
mic = sr.Microphone()
web_name = ''
HOST = '192.168.1.8' #Default IP Adress -> changes below
PORT = 5000
BUFSIZ = 1024
phrase = 'welcome'


def submit_name():
    '''
    opens a window where you input your name, which is later used for communication later on.
    afetr that it runs the voice recognition in the background
    :return: none
    '''
    global web_name
    name_string = name.get()
    print(name_string)
    if name_string == '':
        pass
    else:
        web_name = prepare_os_files.run_assistant(name_string)
        name_box.destroy()
        my_msg.set(web_name)
        send()

        r.listen_in_background(mic, callback, phrase_time_limit=2)
        print('listening')


def callback(r, audio):
    '''
    Takes the microphone input from the background listener and recognizes it.
    then takes your name as string and prepares it for recording
    :param r: recognizes audio input
    :param audio: audio source
    :return: none
    '''
    try:
        you_said = r.recognize_google(audio)
        print("YOU SAID: " + you_said)
        if phrase in you_said:
            name = names()
            record(name)
    except Exception as e:
        pass



def speak(text):
    '''
    speech to text -> may come useful
    :param text:
    :return:
    '''
    tts = gTTS(text=text, lang='en')
    file_name = 'recording.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)


def record(name):
    '''
    records audio after keyword has been said
    :param name:
    :return:
    '''
    print(name)
    playsound.playsound('listening.mp3')
    print('recording')
    audio = r.listen(mic)
    with open('./recorded/' + name, 'wb') as f:
        f.write(audio.get_wav_data())
    print('done recording')

    message = str(dlby_API('./recorded/' + name, 'dlb://input/' + name, 'dlb://output/' + name,
                         './enhanced/enhanced_' + name))

    my_msg.set(message)
    send()


def receive():
    """ Handles receiving of messages. """
    while True:
        try:
            msg = sock.recv(BUFSIZ).decode("utf8")
            #print(msg)
            this_message_list = msg.split()
            print(this_message_list)
            msg_list.insert(tkinter.END, msg)
            if 'dlb://' in msg:
                dolby_download(this_message_list[1], this_message_list[2], this_message_list[3], this_message_list[4])
                if platform.system() == 'Windows':
                    notification_win.windows_notification(this_message_list[0], this_message_list[4])



        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):
    """ Handles sending of messages. """
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    sock.send(bytes(msg, "utf8"))
    if msg == "#quit":
        sock.close()
        top.quit()


def on_closing(event=None):
    """ This function is to be called when the window is closed. """
    my_msg.set("#quit")
    send()


def names():
    '''
    prepares a string for naming the wav you want to send
    :return: name in a format 'yourName_day_month_year_hour_minute_second.wav'
    '''
    now = datetime.now()
    now_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    filename = web_name + '_' + now_string + '.wav'
    return filename


'''
GUI SECTION
'''

top = tkinter.Tk()
top.title("Voice_Assistant_Messaging_System v1.0")
messages_frame = tkinter.Frame(top)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

quit_button = tkinter.Button(top, text="Quit", command=on_closing)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

name_box = tkinter.Toplevel(top)
name_box.transient(top)
name_box.title("Enter Name")
name_box.geometry('200x200+200+200')
name = tkinter.Entry(name_box, bd=5)
name.pack()
name_submit = tkinter.Button(name_box, text='Submit', command=submit_name)
name_submit.pack(side = tkinter.BOTTOM)

'''
Socket connection section
'''

HOST = input("Enter host IP adress: ") # MUST BE DONE VIA TERMINAL
ADDR = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(ADDR)

with mic as mic:
    r.adjust_for_ambient_noise(mic) #sets up ambient noise

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
