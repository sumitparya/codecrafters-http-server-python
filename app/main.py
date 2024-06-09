# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept()
    print("Received connection from", addr[0], "port", addr[1])
    data = conn.recv(1024).decode()
    path = data.split(" ")[1]
    if path == "/":
        pass
    elif "/echo/" in path:
        text = path.split("/")[2]
        print(text)
        conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}\r\n".encode())
    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
