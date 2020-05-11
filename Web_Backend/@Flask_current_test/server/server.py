from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# global const
BUFSIZ = 512
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10

# global variable
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def broadcast(msg, name):
    '''
    send new messages to all clients
    :param msg: bytes['utf8']
    :param name: str
    :return:
    '''
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, 'utf8') + msg)
        except Exception as e:
            print('[EXCEPTION] ', e)


def client_communication(person):
    '''
    Thread to handle all messenges from clients
    :param client: socket
    :return:
    '''

    client = person.client
    addr = person.addr

    # get person name -> first message recieved = name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat", 'utf8')
    broadcast(msg, '')

    while True: # wait for messages
        try:
            msg = client.recv(BUFSIZ)

            if msg == bytes('{quit}', "utf8"):
                client.close()
                persons.remove(person)
                #client.send(bytes("{quit}", 'utf8'))
                broadcast(bytes(f"{name} has left the chat...", 'utf8'),'')
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name + ': ')
                print(f'{name}: ', msg.decode("utf"))
        except Exception as e:
            print("[EXCEPTION] ", e)
            break


def wait_for_connection(SERVER):
    '''
    Wait for connection from new cliewnts, start new thread once connected
    :param client: socket
    :return:
    '''

    while True:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE ", e)
            break
    print('SERVER CRASHED')



if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS) # Open server to listen for connections
    print('Waiting for connection...')
    ACCEPT_TREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_TREAD.start()
    ACCEPT_TREAD.join()
    SERVER.close()
