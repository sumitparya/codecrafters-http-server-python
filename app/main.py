import socket
import threading
import os

def handle_client(conn):
    # Receive data from the client
    data = conn.recv(1024).decode()
    # Extract the path from the request
    path = data.split(" ")[1]
    
    # Handle different paths
    if path == "/":
        # Send a 200 OK response for the root path
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif "/echo" in path:
        # Extract the text from the path and send it back as a response
        text = path.split("/echo/")[1]
        conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}\r\n".encode())
    elif "/user-agent" in path:
        # Extract the user agent from the request headers and send it back as a response
        useragent = (data.split("\r\nUser-Agent: ")[1]).split("\r\n")[0]
        print(useragent)  # Print the user agent for debugging purposes
        conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(useragent)}\r\n\r\n{useragent}\r\n".encode())
    elif "/files" in path:
        try:
            # Get the file path from the request and check if it exists
            file = f"/tmp/data/codecrafters.io/http-server-tester/{path.split("/files/")[1]}"
            file_size = os.path.getsize(file)
            conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {file_size}\r\n\r\nHello, World!\r\n".encode())
        except FileNotFoundError:
            # Send a 404 Not Found response if the file does not exist
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        # Send a 404 Not Found response for any other path
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

def main():
    # Uncomment this to pass the first stage
    # Create a server socket and listen for incoming connections
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    
    while True:
        # Accept a client connection and handle it in a separate thread
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    main()
