import socket
import select
import msvcrt

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
MAX_LENGTH = 1024

USERNAME = input("Enter username: ")
while USERNAME[0] == '@':
    USERNAME = input("Enter username: ")

client_socket = socket.socket()
client_socket.connect((SERVER_IP, SERVER_PORT))
client_socket.send(f"{str(len(USERNAME)).zfill(2)}{USERNAME}".encode())
msg = ""


def protocol(message):
    print()
    while True:
        cmd = input("Enter type of command, between 1 and 5> ")
        try:
            if int(cmd) <= 5:
                break
        except ValueError:
            continue

    if cmd == '1':
        print()
        return f"{str(len(USERNAME)).zfill(2)}{USERNAME}{cmd}{str(len(message)).zfill(4)}{msg}"

    if cmd == '2':
        appointed = input("Enter user to appoint: ")
        return f"{str(len(USERNAME)).zfill(2)}{USERNAME}{cmd}{str(len(appointed)).zfill(2)}{appointed}"

    if cmd == '3':
        kicked = input("Enter user to kick: ")
        return f"{str(len(USERNAME)).zfill(2)}{USERNAME}{cmd}{str(len(kicked)).zfill(2)}{kicked}"

    if cmd == '4':
        mute = input("Enter user to mute/unmute: ")
        return f"{str(len(USERNAME)).zfill(2)}{USERNAME}{cmd}{str(len(mute)).zfill(2)}{mute}"

    if cmd == '5':
        rec = input("Enter recipient of private message: ")
        return f"{str(len(USERNAME)).zfill(2)}{USERNAME}{cmd}{str(len(rec)).zfill(2)}{rec}{str(len(msg)).zfill(4)}{msg}"


while True:
    rlist, wlist, xlist = select.select([client_socket], [client_socket], [])
    if msvcrt.kbhit():
        char = msvcrt.getch()
        if char == b'\r':
            if client_socket in wlist:
                client_socket.send(protocol(msg).encode())
                if msg == "quit":
                    client_socket.close()
                    break
                msg = ""
                print()
        else:
            char = char.decode()
            print(char, end='')
            msg += char
    if client_socket in rlist:
        data_length = client_socket.recv(4).decode()
        data = client_socket.recv(int(data_length)).decode()
        print(data)
