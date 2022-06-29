#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    words = data.split()
    if not words:
        return False
    if words[0].upper() not in ['TAKE_SCREENSHOT', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']:
        return False
    if words[0].upper() == 'DIR' and len(words) != 2:
        return False
    if words[0].upper() == 'DELETE' and len(words) != 2:
        return False
    if words[0].upper() == 'COPY' and len(words) != 3:
        return False
    if words[0].upper() == 'EXECUTE' and len(words) != 2:
        return False
    if words[0].upper() == 'TAKE_SCREENSHOT' and len(words) != 2:
        return False
    return True


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    return f"{str(len(data)).zfill(4)}{data}".encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(4).decode()
    return True, my_socket.recv(int(length)).decode()


