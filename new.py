import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = "100.100.0.0"
port = 1111

server.bind((ip, port))
server.listen()

clients = []

print("server is running")

def remove(client):
    if client in clients:
        clients.remove(client)

def broadcast(message, connection):
    for i in clients:
        if(i != connection):
            try:
                i.send(message.encode("utf-8"))
            except:
                remove(i)


def clientThread(connection, address):
    connection.send("hi".encode("utf-8"))
    while(True):
        try:
            message = connection.recv(2048).decode("utf-8")
            if message:
                print("<" + address[0] + ">")
                print(message)
                broadcast("<" + address[0] + ">: " + message, connection)
            else:
                remove(connection)
        except:
            continue

while(True):

    connection, address = server.accept()
    clients.append(connection)
    
    print(address[0] + " connected")
    newThread = Thread(target=clientThread, args=(connection, address))
    newThread.start()



