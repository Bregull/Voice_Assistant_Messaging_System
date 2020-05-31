import os


# The notifier function
def notify(title, subtitle, message, open):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    o = '-open {!r}'.format(open)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s, o])))


# Calling the function
notify(title = 'Nowa wiadomość',
       subtitle = 'with python',
       message = 'Hello, this is me, notifying you!',
       open = 'https://www.bbc.com/')

