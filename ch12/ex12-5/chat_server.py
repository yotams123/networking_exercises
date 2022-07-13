import socket
import select

MAX_LENGTH = 1024
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

open_clients = []
pending_msgs = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_clients, open_clients, [])
    for client in rlist:
        if client is server_socket:
            (connection, addr) = server_socket.accept()
            print(f"New client {addr} connected!")
            open_clients.append(connection)
        else:
            data = client.recv(MAX_LENGTH).decode()
            if data == "":
                open_clients.remove(client)
                client.close()
                pending_msgs.append((f"Client {client.getpeername()} disconnected", open_clients))
                print(f"Client {client.getpeername()} disconnected")
            else:
                print("Data received: ", data)
                p = open_clients.copy()
                p.remove(client)
                pending_msgs.append((data, p))
    for data, receivers in pending_msgs:
        for receiver in receivers:
            if receiver in wlist:
                receiver.send(f"{receiver.getpeername()}:\t{data}".encode())
                receivers.remove(receiver)
        if not receivers:
            pending_msgs.remove((data, receivers))

