import socket
import select
import datetime

MAX_LENGTH = 1024
SERVER_IP = '0.0.0.0'
SERVER_PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

open_clients = []
pending_msgs = []  # messages that haven't reached everybody
admins = ['ysman']  # list of admins by username

clients = []
while True:
    rlist, wlist, xlist = select.select([server_socket] + open_clients, open_clients, [])
    for client in rlist:
        if client is server_socket:
            (connection, addr) = server_socket.accept()
            uname_length = connection.recv(2).decode()
            uname = connection.recv(int(uname_length)).decode()
            open_clients.append(connection)
            clients.append([connection, uname, False])
            pending_msgs.append((f"New client {uname} connected! ", open_clients.copy()))
        else:
            uname_length = client.recv(2).decode()
            uname = client.recv(int(uname_length)).decode()
            cmd = client.recv(1).decode()
            time = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')

            if cmd == '1':
                msg_length = client.recv(4).decode()
                data = client.recv(int(msg_length)).decode()
                if data != "quit" and data != 'view admins':
                    for i in clients:
                        if i[1] == uname and not i[2]:
                            if uname in admins:
                                pending_msgs.append((f"{time}\t@{uname}:\t{data}", open_clients.copy()))
                            else:
                                pending_msgs.append((f"{time}\t{uname}:\t{data}", open_clients.copy()))
                        elif i[1] == uname:
                            pending_msgs.append((f"You cannot speak here", [client]))
                elif data == 'view admins':
                    msg = admins[0]
                    for a in admins[1:]:
                        msg += ", " + a
                    pending_msgs.append((msg, [client]))
                else:
                    open_clients.remove(client)
                    client.close()
                    pending_msgs.append((f"{time}\t{uname} disconnected", open_clients.copy()))

            if cmd == '2':
                if uname not in admins:
                    pending_msgs.append(("Must be an admin to use this functionality", [client]))
                    client.recv(MAX_LENGTH)
                    continue
                appointed_length = client.recv(2).decode()
                appointed = client.recv(int(appointed_length)).decode()
                admins.append(appointed)
                rec = None
                for i in clients:
                    if i[1] == appointed:
                        rec = i[0]
                pending_msgs.append(("You are now an admin!", [rec]))
            if cmd == '3':
                if uname not in admins:
                    pending_msgs.append(("Must be an admin to use this functionality", [client]))
                    client.recv(MAX_LENGTH)
                    continue
                kicked_length = client.recv(2).decode()
                kicked = client.recv(int(kicked_length)).decode()
                for i in clients.copy():
                    if i[1] == kicked:
                        open_clients.remove(i[0])
                        i[0].close()
                        pending_msgs.append((f"{time}\t{i[1]} was kicked by {uname}", open_clients.copy()))
                        clients.remove(i)

            if cmd == '4':
                if uname not in admins:
                    pending_msgs.append(("Must be an admin to use this functionality", [client]))
                    client.recv(MAX_LENGTH)
                    continue
                muted_length = client.recv(2).decode()
                muted = client.recv(int(muted_length)).decode()
                for i in clients.copy():
                    if i[1] == muted:
                        i[2] = not i[2]
                        if i[2]:
                            pending_msgs.append(("You are now mute", [i[0]]))
                        else:
                            pending_msgs.append(("You are now unmute", [i[0]]))
            if cmd == '5':
                rec_len = client.recv(2).decode()
                rec = client.recv(int(rec_len)).decode()

                msg_len = client.recv(4).decode()
                msg = client.recv(int(msg_len)).decode()

                for i in clients:
                    if i[1] == rec:
                        pending_msgs.append((f"{time}\t!{uname}:\t{msg}", [client, i[0]]))

    for data, receivers in pending_msgs:
        for receiver in receivers:
            if receiver in wlist:
                receiver.send(f"{str(len(data)).zfill(4)}{data}".encode())
                receivers.remove(receiver)
        if not receivers:
            pending_msgs.remove((data, receivers))

