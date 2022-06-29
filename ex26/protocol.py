"""EX 2.6 protocol implementation
   Author:
   Date:
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data.upper() in ['RAND', 'WHORU', 'TIME', 'EXIT']:
        return True
    else:
        return False


def create_msg(data):
    """Create a valid protocol message, with length field"""
    return f"{len(data):02}{data.upper()}".encode()


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    data = my_socket.recv(1024).decode()
    field = data[:2]
    try:
        field = int(field)
    except ValueError:
        return False, "Error"
    return True, data[2:]
