from website.client.client import Client
import time
from threading import Thread


c1 = Client('Guliaa')
c2 = Client("Paulos")


def update_messages():
    msgs = []
    run = True
    while run:
        time.sleep(0.1) # update messages displayed
        new_messages = c1.get_messages()
        msgs.extend(new_messages)
        for msg in new_messages:
            print(msg)
            if msg == '{quit}':
                run = False
                break


Thread(target=update_messages).start()


c1.send_message("sup")
time.sleep(3)
c2.send_message('it ok')
time.sleep(3)
c1.send_message('cool')
time.sleep(3)
c2.send_message('so cool')
time.sleep(3)

c1.disconnect()
time.sleep(2)
c2.disconnect()