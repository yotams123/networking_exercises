import socket
import select
import msvcrt

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
MAX_LENGTH = 1024

client_socket = socket.socket()
client_socket.connect((SERVER_IP, SERVER_PORT))


msg = ""
while True:
    rlist, wlist, xlist = select.select([client_socket], [client_socket], [])
    if msvcrt.kbhit():
        char = msvcrt.getch()
        if char == b'\r':
            if client_socket in wlist:
                if msg == "":
                    client_socket.close()
                    break
                else:
                    client_socket.send(msg.encode())
                    msg = ""
                print()
        else:
            if len(msg) == 0:
                print("You:\t", end='')
            char = char.decode()
            print(char, end='')
            msg += char
    if client_socket in rlist:
        data = client_socket.recv(MAX_LENGTH).decode()
        print(data)
