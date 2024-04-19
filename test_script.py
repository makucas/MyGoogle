import socket

BUFFER_SIZE = 8192

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1" 
    server_port = 8000  
    client.connect((server_ip, server_port))

    try:
        client.send("search".encode("utf-8")[:BUFFER_SIZE])
        response = client.recv(BUFFER_SIZE).decode("utf-8")
        client.send("a".encode("utf-8")[:BUFFER_SIZE])



        print(f"{response}")
        if "task completed!" in response.lower():
            input("Press enter to continue\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")
run_client()
