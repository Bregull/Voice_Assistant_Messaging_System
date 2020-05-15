import speech_recognition as sr
import os, errno

r = sr.Recognizer()
mic = sr.Microphone()
web_name = ''

'''
Prepares OS files for recording
'''

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


def personal_ID(name = ''):
    filename = 'ID.txt'
    if os.path.exists(filename):
        file = open(filename, 'w')
        file.write(name)
        #name = file.readline()
        return name
    else:
        file = open(filename, 'w')
        if name == '':
            name = input('Your name: ')
        file.write(name)
        file.close()
        return name


def run_assistant(name):
    web_name = personal_ID(name)
    create_directory()
    return web_name
