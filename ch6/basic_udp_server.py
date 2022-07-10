import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 8821))

(data, client) = server_socket.recvfrom(1024)

data = data.decode()
response = "Hello, {}".format(data)
server_socket.sendto(response.encode(), client)

server_socket.close()