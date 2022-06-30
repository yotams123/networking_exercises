import socket
import random

PORT = 8820

msg_sent = ''
msg_rcv = ""

while msg_rcv.upper() != "EXIT":
    # act as client
    socket_a = socket.socket()
    socket_a.connect(('127.0.0.1', int(PORT)))
    print(f"User A is connected to port {PORT}")
    PORT = random.randint(0, 65535)
    msg_sent = input("> ")
    msg_sent = f"{str(PORT).zfill(5)}{msg_sent}"
    socket_a.send(msg_sent.encode())
    socket_a.close()
    if msg_sent[5:].upper() == 'EXIT':
        break
    print()

    # act as server
    socket_a = socket.socket()
    socket_a.bind(('0.0.0.0', PORT))
    socket_a.listen()
    print(f"user A is listening to port {PORT}")
    (socket_b, socket_b_address) = socket_a.accept()
    PORT = socket_b.recv(5).decode()
    msg_rcv = socket_b.recv(1024).decode()
    print(f"User B: {msg_rcv}")
    socket_a.close()

    print()

