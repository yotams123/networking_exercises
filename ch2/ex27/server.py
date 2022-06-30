#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

from ch2.ex27 import protocol
import socket
import glob
import os
import shutil
import subprocess
import pyautogui

IP = '0.0.0.0'


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    valid = protocol.check_cmd(cmd)
    command = cmd.split()[0].upper()
    params = cmd.split()[1:]

    return valid, command, params


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response = 'OK'
    if command == 'DIR':
        response = glob.glob(f"{params[0]}/*.*")
        response = ", ".join(r[len(params[0]) + 1:] for r in response)
        if response == "":
            response = "Couldn't find the directory you were looking for. " \
                       "Make sure you are entering the correct absolute path"
    if command == 'DELETE':
        try:
            os.remove(f'{params[0]}')
            response = "Deleted successfully"
        except FileNotFoundError:
            response = "File not found, please make sure you are entering the correct absolute path"
    if command == 'COPY':
        try:
            shutil.copy(f'{params[0]}', fr'{params[1]}')
            response = "Copied successfully"
        except FileNotFoundError:
            response = "File not found, please make sure you are entering the correct path"

    if command == 'EXECUTE':
        try:
            subprocess.call(f'{" ".join(params)}')
            response = "Run Successfully"
        except FileNotFoundError:
            response = "File not found, please make sure you are entering the correct absolute path"
    if command == 'TAKE_SCREENSHOT':
        image = pyautogui.screenshot()
        image.save(f"screenshots/{params[0]}.jpg")
        response = "Took a screenshot successfully"
    if command == 'EXIT':
        response = "Closing connection"

    # (7)
    return response


def main():
    # open socket with client
    server_socket = socket.socket()
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen()
    print("Server is up and running")

    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)

                # add length field using "create_msg"
                protocol.create_msg(response)

                # send to client
                print(protocol.create_msg(response))
                client_socket.send(protocol.create_msg(response))
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                client_socket.send(protocol.create_msg(response))

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            client_socket.send(protocol.create_msg(response))

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
