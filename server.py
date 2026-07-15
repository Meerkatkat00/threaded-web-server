import socket
import os
import mimetypes
import threading
HOST = "127.0.0.1"
PORT = 8080

def print_note(message):
    print(f"[Log Note] {message}")


def create_http(status_code, status_text, body, content_type="text/html; charset=utf-8"):
    if isinstance(body, str):
        body = body.encode("utf-8")
    response_line = f"HTTP/1.0 {status_code} {status_text}\r\n"
    headers = (
        f"Content-Length: {len(body)}\r\n"
        f"Content-Type: {content_type}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return response_line.encode("utf-8") + headers.encode("utf-8") + body

def read_http_request(client_socket):
    data = b""

    while b"\r\n\r\n" not in data:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        data += chunk
        if len(data) > 8192:
            break

    return data.decode("utf-8", errors="ignore")

def handle_client(client_socket, client_address):

    print_note(f"Client connected: {client_address}")
    request_text = read_http_request(client_socket)
    first_line = request_text.split("\r\n")[0]

    print_note("Request received:")
    print(first_line)
    parts = first_line.split()

    if len(parts) != 3:
        body = "<h1>400 Bad Request</h1><p>The request format is invalid.</p>"
        response = create_http(400, "Bad request", body)
        client_socket.sendall(response)
        client_socket.close()
        print_note("Returned 400 Bad Request.")
        return

    method, path, version = parts
    print_note(f"Requested path: {path}")

    if method != "GET":
        body = "<h1>400 Bad Request</h1><p>Only GET requests are supported.</p>"
        response = create_http(400, "Bad request", body)
        client_socket.sendall(response)
        client_socket.close()
        print_note("Returned 400 because the method isn't GET.")
        return

    if ".." in path:
        body = "<h1>400 Bad Request</h1><p>Directory traversal is blocked.</p>"
        response = create_http(400, "Bad request", body)
        client_socket.sendall(response)
        client_socket.close()
        print_note("Blocked directory traversal attempt.")
        return
    if path == "/":
        path = "/index.html"
    file_path = os.path.join("static", path.lstrip("/"))

    if os.path.isdir(file_path):
        body = "<h1>400 Bad Request</h1><p>Directory listing isn't allowed.</p>"
        response = create_http(400, "Bad request", body)
        client_socket.sendall(response)
        client_socket.close()
        print_note("Returned 400 because a directory was requested.")
        return
    if not os.path.exists(file_path):
        body = "<h1>404 Not Found</h1><p>The requested file does not exist.</p>"
        response = create_http(404, "Not found", body)
        client_socket.sendall(response)
        client_socket.close()
        print_note("Returned 404 Not found.")
        return
    
    with open(file_path, "rb") as file:
        body = file.read()
    content_type, _ = mimetypes.guess_type(file_path)

    if content_type is None:
        content_type = "application/octet-stream"
    response = create_http(200, "OK", body, content_type)

    client_socket.sendall(response)
    client_socket.close()
    print_note(f"Returned 200 OK with Content-Type: {content_type}")
    print_note("Connection closed.")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(7)

    print_note(f"Server is running at http://localhost:{PORT}")
    print_note("Waiting for you to get on the browser/client...")

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()