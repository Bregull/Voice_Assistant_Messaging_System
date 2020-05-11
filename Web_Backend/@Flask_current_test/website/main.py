from flask import jsonify, Flask, render_template, url_for, session, redirect, request
from client import Client
from threading import Thread
import time

NAME_KEY = 'name'
client = None
messages = []

app = Flask(__name__)
app.secret_key = 'hello'


def disconnect():
    global client
    if client:
        client.disconnect()


@app.route('/login', methods=['POST', 'GET'])
def login():
    disconnect()
    if request.method == "POST":
        session[NAME_KEY] = request.form['inputName']
        return redirect(url_for('home'))

    return render_template('login.html', **{'session': 'session'})


@app.route('/logout')
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
def home():
    global client

    if NAME_KEY not in session:
        return redirect(url_for('login'))

    client = Client(session[NAME_KEY])
    return render_template('index.html', **{'login': True, 'session': session})


@app.route('/send_message', methods=['GET'])
def send_message(url=None):
    global client

    msg = request.args.get('val')
    if client:
        client.send_message(msg)
    return 'none'


@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})


def update_messages():
    global messages
    run = True
    while run:
        time.sleep(0.1)  # update messages displayed
        if not client: continue
        new_messages = client.get_messages()
        messages.extend(new_messages)

        for msg in new_messages:
            print(msg)
            if msg == '{quit}':
                run = False
                break


if __name__ == '__main__':
    Thread(target=update_messages).start()
    app.run()
