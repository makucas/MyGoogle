import socket
import threading
import functions

BUFFER_SIZE = 8192

def handle_request(client_socket, request):
    my_google = functions.DataManager(data_path='dataset/sample_dataset.json')
    my_google.load_data()

    if request.lower() == "testing":
        client_socket.send("accepted".encode("utf-8"))
        while True:
            search_string = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            index_list = my_google.search(search_string)
            if index_list:
                n, _ = my_google.show(index_list)
                client_socket.send(f"founded a total of {n} items.".encode("utf-8"))
                break
            else:
                client_socket.send("Not founded, try again".encode("utf-8"))

    elif request.lower() == "search" or request == "1":
        client_socket.send("Enter the search string!".encode("utf-8"))
        while True:
            search_string = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            # retorna uma lista contendo os indices dos arquivos encontrados
            index_list = my_google.search(search_string)
            if index_list:
                # retorna o número de itens encontrados e a string contendo os títulos de todos
                n, composed_string = my_google.show(index_list)
                client_socket.send(f"Found a total of {n} items:\n{composed_string}\nEnter the index of the desired file!".encode("utf-8"))

                # exibe o resultado do arquivo escolhido
                index = client_socket.recv(BUFFER_SIZE).decode("utf-8")
                search_results = my_google.show_instance(int(index))
                client_socket.send(f"{search_results}\nTask completed!".encode("utf-8"))
                break
            else:
                client_socket.send("Not founded, try again".encode("utf-8"))

    elif request.lower() == "insert" or request == "2":
        client_socket.send("Enter the path to the archive".encode("utf-8"))
        while True:
            archive_path = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if my_google.insert(archive_path):
                client_socket.send("File inserted, task completed!".encode("utf-8"))
                break
            else:
                client_socket.send("ERROR: file not inserted, try again".encode("utf-8"))

    elif request.lower() == "remove" or request == "3":
        client_socket.send("Enter the index of the archive".encode("utf-8"))
        while True:
            index = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if my_google.remove(int(index)):
                client_socket.send(f"File removed, task completed!".encode("utf-8"))
                break
            else:
                client_socket.send(f"ERROR: File not removed, try again".encode("utf-8"))

    elif request.lower() == "show all" or request == "4":
        size, composed_string = my_google.show_all()
        client_socket.send(f"Found a total of {size} items:\n{composed_string}\nTask completed!".encode("utf-8"))
        
    else:
        client_socket.send(f"Please, chose a available option.".encode("utf-8"))

def handle_client(client_socket, addr):
    try:
        while True:
            request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if request.lower() == "close" or request == "5":
                client_socket.send("closed".encode("utf-8"))
                break
            handle_request(client_socket, request)

    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def run_server():
    server_ip = "127.0.0.1"  
    port = 8000  
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

run_server()
