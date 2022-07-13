import socket
import select

MAX_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

open_clients = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_clients, [], [])
    for r in rlist:
        if r is server_socket:
            (connection, client_address) = server_socket.accept()
            print(f"New client connected!\t{client_address}")
            open_clients.append(connection)
        else:
            data = r.recv(MAX_LENGTH).decode()
            if data == "":
                r.close()
                rlist.remove(r)
                print("Connection closed")
            else:
                print(data)
