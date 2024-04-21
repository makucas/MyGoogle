import threading
import socket
import time

BUFFER_SIZE = 8192

def start_client(client_id, sleep_interval):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8000))
        
        # Aqui você pode enviar solicitações ao servidor e medir o tempo de resposta
        start_time = time.time()
        client_socket.send("testing".encode("utf-8"))
        _ = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        client_socket.send("Hoje".encode("utf-8"))
        response = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        end_time = time.time()
        
        print(f"Client {client_id} {response} with the search string 'Hoje'.")
        print(f"Client {client_id} execution time: {end_time - start_time} seconds\n")
        
        client_socket.close()
    except Exception as e:
        print(f"Error in client {client_id}: {e}")

def start_clients(num_clients, sleep_interval):
    threads = []
    
    for i in range(num_clients):
        thread = threading.Thread(target=start_client, args=(i+1, sleep_interval))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_clients = 1  # número de clientes concorrentes
    start_clients(num_clients, 0)  # 0 é o intervalo de sono entre as execuções dos clientes