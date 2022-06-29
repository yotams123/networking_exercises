"""EX 2.6 client implementation
   Author:
   Date:
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)

        if valid_cmd:
            # 1. Add length field ("RAND" -> "04RAND")
            user_input = protocol.create_msg(user_input)

            # 3. If command is EXIT, break from while loop
            if user_input.decode()[2:] == "EXIT":
                my_socket.send(protocol.create_msg(user_input))
                break

            my_socket.send(protocol.create_msg(user_input))
            # 4. Get server's response
            response = protocol.get_msg(my_socket)
            # 5. If server's response is valid, print it
            if response:
                print(f"{response[1]}\n")
            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    # Close socket
    my_socket.close()

if __name__ == "__main__":
    main()
