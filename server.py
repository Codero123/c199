import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []

print("Server has started...")

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print ("<" + addr[0] + "> " + message)

                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()
