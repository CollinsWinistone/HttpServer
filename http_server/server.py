import socket
import os

class HTTPServer:
    def __init__(self, host, port, use_https=False):
        self.host = host
        self.port = port
        self.use_https = use_https
        
        # Set up server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
    
    def serve_forever(self):
        # Start listening for incoming connections
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}...")
        
        while True:
            # Accept incoming connection
            client_socket, address = self.server_socket.accept()
            print(f"Received connection from {address}")
            
            # Receive request
            request_data = client_socket.recv(1024).decode("utf-8")
            request = HTTPRequest(request_data)

            # Request uri
            print("Request uri")
            print(request.uri)
            
            # Serve file or return 404 error
            if request.method == "GET":
                # file_path = self._get_file_path(request.uri)
                file_path = "./index.html"
                # print file path
                print("File path")
                print(file_path)
                if os.path.isfile(file_path):
                    print("This is a file")
                    with open(file_path, "rb") as f:
                        response_body = f.read()
                    response_headers = {
                        "Content-Type": self._get_content_type(file_path),
                        "Content-Length": len(response_body),
                        "Connection": "close"
                    }
                    response = HTTPResponse("200 OK", response_headers, response_body)
                else:
                    print("It is not a file path...")
                    response = HTTPResponse("404 Not Found")
            else:
                response = HTTPResponse("405 Method Not Allowed")
            
            # Send response
            client_socket.sendall(bytes(response))
            
            # Close connection
            client_socket.close()
            print(f"Connection closed with {address}")
    
    def _get_file_path(self, uri):
        if uri == "/":
            return "./index.html"
        else:
            return "." + uri
    
    def _get_content_type(self, file_path):
        extension = os.path.splitext(file_path)[1]
        if extension == ".html":
            return "text/html"
        elif extension == ".css":
            return "text/css"
        elif extension == ".js":
            return "application/javascript"
        elif extension == ".jpg" or extension == ".jpeg":
            return "image/jpeg"
        elif extension == ".png":
            return "image/png"
        else:
            return "application/octet-stream"


class HTTPResponse:
    def __init__(self, status, headers=None, body=None):
        self.status = status
        self.headers = headers or {}
        self.body = body or b""
    
    def __bytes__(self):
        status_line = f"HTTP/1.1 {self.status}\r\n"
        header_lines = [f"{key}: {value}\r\n" for key, value in self.headers.items()]
        header_block = "".join(header_lines)
        response = status_line + header_block + "\r\n" + self.body.decode("utf-8")
        return response.encode("utf-8")


class HTTPRequest:
    def __init__(self, request_string):
        self.method = None
        self.uri = None
        self.http_version = None
        self.headers = {}
        self.body = None
        
        self.parse_request(request_string)
    
    def parse_request(self, request_string):
        lines = request_string.split("\r\n")
        request_line = lines[0].split()
        
        self.method = request_line[0]
        self.uri = request_line[1]
        self.http_version = request_line[2]
        
        # Parse headers
        for line in lines[1:]:
            if line.strip():
                key, value = line.split(":", maxsplit=1)
                self.headers[key.strip()] = value.strip()
            
        # Parse body if applicable
        if "Content-Length" in self.headers:
            content_length = int(self.headers["Content-Length"])
            self.body = lines[-1].encode("utf-8")[:content_length]

if __name__ == "__main__":
    server = HTTPServer("localhost", 8000)
    server.serve_forever()

