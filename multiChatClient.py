import tkinter
from threading import Thread
import socket
from gtts import gTTS
import playsound
import speech_recognition as sr
from dlby_io_API import dlby_API
from datetime import datetime
import record_voice_on_command
from dlby_io_API import download as dolby_download


r = sr.Recognizer()
mic = sr.Microphone()
web_name = ''
HOST = '192.168.1.8'
PORT = 5000
BUFSIZ = 1024


def submit_name():
    global web_name
    name_string = name.get()
    print(name_string)
    if name_string == '':
        pass
    else:
        web_name = record_voice_on_command.run_assistant(name_string)
        name_box.destroy()
        my_msg.set(web_name)
        send()
        r.listen_in_background(mic, callback)
        print('listening')


def callback(r, audio):
    try:
        you_said = r.recognize_google(audio)
        print("YOU SAID: " + you_said)
        if 'welcome' in you_said:
            name = names()
            record(name)
    except Exception as e:
        pass



def speak(text):
    tts = gTTS(text=text, lang='en')
    file_name = 'recording.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)


def record(name):
    print(name)
    playsound.playsound('listening.mp3')
    print('recording')
    audio = r.listen(mic, phrase_time_limit=2)
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
    now = datetime.now()
    now_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    filename = web_name + '_' + now_string + '.wav'
    return filename


top = tkinter.Tk()
top.title("Simple Chat Client v1.0")
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

ADDR = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(ADDR)

with mic as mic:
    r.adjust_for_ambient_noise(mic)

name_box = tkinter.Toplevel(top)
name_box.transient(top)
name_box.title("Enter Name")
name_box.geometry('100x100+200+200')
name = tkinter.Entry(name_box, bd=5)
name.pack()
name_submit = tkinter.Button(name_box, text='Submit', command=submit_name)
name_submit.pack(side = tkinter.BOTTOM)



receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
