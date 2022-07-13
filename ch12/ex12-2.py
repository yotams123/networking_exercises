import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
MSG_LENGTH = 1024

client_socket = socket.socket()
client_socket.connect((SERVER_IP, SERVER_PORT))

msg = input("> ")

while msg != "":
    client_socket.send(msg.encode())
    print(client_socket.recv(MSG_LENGTH).decode())
    msg = input("> ")


client_socket.close()
