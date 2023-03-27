import socket
import ssl
import os
import logging

logging.basicConfig(filename="server.log", level=logging.INFO)

class HTTPRequest:
    def __init__(self, method, path, headers=None, body=None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body or b""

class HTTPResponse:
    def __init__(self, status_code, headers=None, body=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body or b""

    def to_bytes(self):
        status_line = f"HTTP/1.1 {self.status_code}\r\n"
        header_lines = ""
        for key, value in self.headers.items():
            header_lines += f"{key}: {value}\r\n"
        body = self.body
        headers = status_line + header_lines + "\r\n"
        return headers.encode("utf-8") + body

class HTTPServer:
    def __init__(self, host, port, cert_file=None, key_file=None):
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Listening on {self.host}:{self.port}...")

            while True:
                client_socket, client_address = server_socket.accept()
                client_socket = self.wrap_socket(client_socket)
                print(f"Accepted connection from {client_address}")
                try:
                    request = self.parse_request(client_socket)
                    logging.info(f"{request.method} {request.path} HTTP/1.1")
                    response = self.handle_request(request)
                except Exception as e:
                    logging.error(e)
                    response = HTTPResponse(500)
                client_socket.sendall(response.to_bytes())
                client_socket.close()

    def wrap_socket(self, socket):
        if self.cert_file and self.key_file:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(self.cert_file, keyfile=self.key_file)
            return ssl_context.wrap_socket(socket, server_side=True)
        else:
            return socket

    def parse_request(self, client_socket):
        request_data = client_socket.recv(4096).decode("utf-8")
        if not request_data:
            raise ValueError("Request data is empty")

        headers = {}
        method, path, version = request_data.strip().split("\r\n")[0].split(" ")
        lines = request_data.strip().split("\r\n")
        for line in lines[1:]:
            if line.strip():
                key, value = line.split(":", maxsplit=1)
                headers[key.strip()] = value.strip()

        if "Content-Length" in headers:
            content_length = int(headers["Content-Length"])
            body = request_data.split("\r\n\r\n", maxsplit=1)[1][:content_length].encode("utf-8")
        else:
            body = None

        return HTTPRequest(method, path, headers, body)

    def handle_request(self, request):
        if request.method not in ["GET", "POST", "PUT", "DELETE"]:
            return HTTPResponse(501)

        file_path = os.path.join(".", request.path[1:])
        if not os.path.exists(file_path):
            return HTTPResponse(404)

        if request.method == "GET":
            try:
                with open(file_path, "rb") as f:
                    body = f.read()
            except Exception as e:
                return HTTPResponse(500)
if __name__ == "__main__":
    server = HTTPServer("localhost", 8000)
    server.serve_forever()   
