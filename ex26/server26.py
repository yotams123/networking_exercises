"""EX 2.6 server implementation
   Author:
   Date:
"""

import socket
import protocol
import datetime
import random

def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == "TIME":
        return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    elif cmd == 'WHORU':
        return "My Server"
    elif cmd == "RAND":
        return str(random.randint(1, 10))


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            cmd = cmd[4:-1]
            print(cmd)

            # 2. Check if the command is valid
            valid = protocol.check_cmd(cmd)
            response = "-"

            # 3. If valid command - create response
            if valid:
                if cmd == 'EXIT':
                    client_socket.close()
                    break
                else:
                    response = create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

        client_socket.send(protocol.create_msg(response))
        # Send response to the client

    print("Closing\n")
    # Close sockets

if __name__ == "__main__":
    main()
