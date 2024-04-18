import socket
import threading
import my_google

def handle_request(client_socket, request):
    data_list = my_google.load_data()
    index_size = len(data_list)

    if request.lower() == "search":
        client_socket.send("Enter the search string!".encode("utf-8"))

        while True:
            search_string = client_socket.recv(1024).decode("utf-8")
            # Return an index list that has the position of each founded item.
            index_list = my_google.search(search_string, data_list)

            if index_list:
                composed_string = ""
                # Iterate through each index and construct the string that contains the answer.
                for index in index_list:
                    title = my_google.show(index, data_list)
                    composed_string += title + "\n"
                composed_string += "\nTask completed!"
                client_socket.send(composed_string.encode("utf-8"))
                break
            else:
                client_socket.send("not founded, try again".encode("utf-8"))

    if request.lower() == "insert":
        client_socket.send("Enter the path to the archive".encode("utf-8"))

        while True:
            archive_path = client_socket.recv(1024).decode("utf-8")
            if my_google.insert(archive_path, data_list, index_size):
                index_size+=1
                client_socket.send("file inserted".encode("utf-8"))
            else:
                client_socket.send("ERROR: file not inserted, try again".encode("utf-8"))


    if request.lower() == "remove":
        pass

    else:
        response = "Didn't find any option!"
        client_socket.send(response.encode("utf-8"))

def handle_client(client_socket, addr):
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            handle_request(client_socket, request)

    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def run_server():
    server_ip = "127.0.0.1"  # server hostname or IP address
    port = 8000  # server port number
    # create apy socket object
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

run_server()
