import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


clients = {}
addresses = {}

HOST = '127.0.0.1' #localhost
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
        elif("vki.html?" in msg.decode("utf8")):

            name= msg.decode("utf8").split("?")[1]
            client_address = addresses[client][0]  # İstemcinin IP adresini alıyoruz
            client_port = addresses[client][1]  # İstemcinin port numarasını alıyoruz
            print(addresses[client][1])
            with open("vki.html", 'r') as file:
                content = file.read()
                modified_content = content.replace("{name_placeholder}", name)
                modified_content = modified_content.replace("{client_address_placeholder}", client_address)
                modified_content = modified_content.replace("{client_port_placeholder}", str(client_port))
                response = modified_content.encode("utf-8")
                client.send(response)
            # print(name)


        if(msg == bytes("{quit}", "utf8")):
            client.send(bytes("{quit}", "utf8"))
            a = addresses[client][0]
            print("{} logged out.".format(a))
            del addresses[client]
            client.close()
            break


if __name__ == "__main__":
    SERVER.listen(5) # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
