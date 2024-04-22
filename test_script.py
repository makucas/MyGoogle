import multiprocessing
import socket
import time

BUFFER_SIZE = 8192

def start_client(file_name):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8000))
        
        client_socket.send("testing".encode("utf-8"))
        _ = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        client_socket.send("Hoje".encode("utf-8"))
        _ = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_clients(num_clients, file_name):
    processes = []
    
    for i in range(num_clients):
        process = multiprocessing.Process(target=start_client, args=(i+1,file_name))
        processes.append(process)
        process.start()
        
    for process in processes:
        process.join()

    with open(file_name, "a") as file:
        file.write("\n")

def run_test(duration, requests_per_second, file_name):
    interval = 1 / requests_per_second
    start_time = time.time()

    while time.time() - start_time < duration:
        process_start_time = time.time()
        multiprocessing.Process(target=start_client, args=(file_name,)).start()
        process_end_time = time.time()

        execution_time = process_end_time - process_start_time
        with open(file_name, "a") as file:
            file.write(f"{execution_time}\n")

        time.sleep(interval)

if __name__ == "__main__":
    DURATION = 60
    REQUEST_PER_SECOND = 400
    run_test(duration=DURATION, requests_per_second=REQUEST_PER_SECOND, file_name=f"executions_time_{REQUEST_PER_SECOND}.txt")

