import socket
import os

PORT = 80
IP = '0.0.0.0'
ROOT_DIR = "C:/Users/yotam/projects/networking/ch4/ex44/webroot"
SOCKET_TIMEOUT = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen()


def generate_response(file):
    filetype = file.split(".")[1]
    if filetype in ['jpg', 'ico']:
        with open(fr"{ROOT_DIR}{file}", 'rb') as requestfile:
            data = requestfile.read()
    else:
        with open(fr"{ROOT_DIR}{file}", 'r') as requestfile:
            data = ""
            for line in requestfile:
                if line != "\n":
                    data += line

    content_type = None
    if filetype == 'html' or filetype == 'txt':
        content_type = "text/html; charset=utf-8"
    elif filetype == "jpg":
        content_type = "image/jpeg"
    elif filetype == "js":
        content_type = "text/javascript; charset=UTF-8"
    elif filetype == "css":
        content_type = "text/css"
    elif filetype == "ico":
        content_type = "image/x-icon"

    if filetype in ['jpg', 'ico']:
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\naccept-ranges: bytes\r\n\r\n".encode() + data
    else:
        response = f"HTTP/1.1 200 OK\r\nContent-Length: " \
                   f"{len(data)}\r\nContent-Type: {content_type}\r\n\r\n{data}".encode()

    return response


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    r = request.split()
    if r[0] == 'GET' and r[2] == 'HTTP/1.1':
        requestfile = r[1]
        if requestfile == '/':
            requestfile = '\\index.html'
        if os.path.isfile(fr"{ROOT_DIR}{requestfile}"):
            return True, generate_response(requestfile)
        else:
            return False, "HTTP/1.1 404 Not Found".encode()
    return False, "Bad request".encode()


def handle_client(sock):
    sock.settimeout(SOCKET_TIMEOUT)
    while True:
        try:
            request = sock.recv(1024).decode()
            valid, response = validate_http_request(request)

            if not valid:
                sock.close()
                return

            sock.send(response)
            sock.close()
        except (TimeoutError, OSError):
            sock.close()
            break


while True:
    (client_socket, client_address) = server_socket.accept()
    handle_client(client_socket)
