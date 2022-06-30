import socket
import random

PORT = 8820

msg_sent = ""
msg_rcv = ""

while msg_sent[5:].upper() != "EXIT":
    # act as server
    socket_b = socket.socket()
    socket_b.bind(('0.0.0.0', PORT))
    socket_b.listen()
    print(f"user B is listening to port {PORT}")
    (socket_a, socket_a_address) = socket_b.accept()
    PORT = socket_a.recv(5).decode()
    msg_rcv = socket_a.recv(1024).decode()
    print(f"User A: {msg_rcv}")
    socket_b.close()
    if msg_rcv.upper() == "EXIT":
        break

    print()

    # act as client
    socket_b = socket.socket()
    socket_b.connect(("127.0.0.1", int(PORT)))
    print("User B is connected to port PORT")
    PORT = random.randint(0, 65535)
    msg_sent = input("> ")
    msg_sent = f"{str(PORT).zfill(5)}{msg_sent}"
    socket_b.send(msg_sent.encode())
    socket_b.close()

    print()
