import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


clients = {}
addresses = {}

HOST = '192.168.43.181' #localhost
PORT = 33000
BUFSIZ = 4096
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." %client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    """Handles a single client connection."""

    while True:
        msg = client.recv(BUFSIZ)

        # If the msg ends with .html, send the html file in the project directory that matches the name before .html to the client.
        if msg.decode("utf8").endswith(".html"):
            try:
                with open(msg.decode("utf8"), 'rb') as file:
                    content = file.read()
                    response = b'%s' % content  # Başarılı yanıt ve içerik
                    client.send(response)
            except FileNotFoundError:
                response = b'HTTP/1.1 404 Not Found\n\nFile Not Found'


        elif msg != bytes("{quit}", "utf8"):
            broadcast(msg,": ")

        else:
            client.send(bytes("{quit}", "utf8"))
            a = addresses[client][0]
            print("{} logged out.".format(a))
            del addresses[client]
            client.close()
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5) # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
