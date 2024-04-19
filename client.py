import socket
import functions

BUFFER_SIZE = 8192

def show_options():
    print(f"1-Search\n2-Insert\n3-Remove\n4-Show All")

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  # replace with the server's IP address
    server_port = 8000  # replace with the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))

    show_options()

    try:
        while True:
            msg = input("Input: ")
            client.send(msg.encode("utf-8")[:BUFFER_SIZE])

            response = client.recv(BUFFER_SIZE)
            response = response.decode("utf-8")

            if response.lower() == "closed":
                break

            print(f"{response}")
            if "task completed!" in response.lower():
                input("Press enter to continue\n")
                show_options()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

run_client()
