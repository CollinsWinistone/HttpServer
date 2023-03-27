import socket
import os
import logging # log server information
from Response.response import HTTPResponse
from Requests.requests import HTTPRequest
from http_parser.http_parser import HTTPParser
from Php_handler.php_handler import handle_request # handles php execution

logging.basicConfig(filename="server.log", level=logging.INFO)

# Default directory for server resources
WEB_ROOT = os.path.join(os.path.dirname(__file__), 'web_root')


class HTTPServer:
    """Custom HTTP Server to handle requests and return responses
    """
    def __init__(self, host, port, use_https=False):
        self.host = host # host name
        self.port = port # port number
        self.use_https = use_https # use https or not
        
        # Set up server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
    
    def serve(self):
        # Start listening for incoming connections
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}...")
        
        while True:
            # Accept incoming connection
            client_socket, address = self.server_socket.accept()
            print(f"Received connection from {address}")
            
            # Receive request
            request_data = client_socket.recv(1024).decode("utf-8")
            

            try:
                parser = HTTPParser()
                parser.parse_request(request_data)
                request = HTTPRequest(
                    request_data,
                    parser.method,
                    parser.uri,
                    parser.http_version,
                    parser.headers,
                    parser.body
                )
                
                logging.info(f"{request.method}  HTTP/1.1")
                logging.info(f"{request.headers}")
                response = HTTPResponse(500)
            except Exception as e:
                logging.error(e)
                response = HTTPResponse(500)

            # parse HTTP headers
            headers = request_data.split('\n')
            filename = headers[0].split()[1]
            
            # Serve file or return 404 error
            if request.method == "GET":
                
                # resource_name = str(request.uri)
                resource_name = request.uri.lstrip('/')
                
                filename = os.path.join(os.getcwd(),"web_root", resource_name)
                # file extension
                extension = filename.split('.')
                
                # server side script code:
                # checks if the file extension is a .php
                if extension[1] == "php":
                    response = handle_request(filename)
                    print(response.__bytes__())
                    # Send response
                    client_socket.sendall(response.__bytes__())
                    # Close connection
                    client_socket.close()
                    print(f"Server script Connection closed with {address}")
                else:
                    logging.info(f"No .php file found...")

                try:
                    # Open file
                    f = open(filename, "rb")
                    # Read file
                    response_body = f.read()
                    # Close file
                    f.close()
                    # Set response headers
                    response_headers = {
                        "Content-Type": self._get_content_type(filename),
                        "Content-Length": len(response_body),
                        "Connection": "close"
                    }

                    # Set response
                    response = HTTPResponse("200 OK", response_headers, response_body)
                    
                except:
                    # Set response
                    response = HTTPResponse("404 Not Found")
  
            else:
                response = HTTPResponse("405 Method Not Allowed")
                
            
            # Send response
            client_socket.sendall(response.__bytes__())
            
            # Close connection
            client_socket.close()
            print(f"Connection closed with {address}")
    
    def _get_file_path(self, uri):
        """Returns the file path for a given URI"""
        if uri == "/":
            return "/index.html"
        else:
            return "." + uri
    
    def _get_content_type(self, file_path):
        """Returns the content type for a given file path"""

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
        elif extension == ".php":
            return "text/html"
        else:
            return "application/octet-stream"


if __name__ == "__main__":
    server = HTTPServer("localhost", 8000)
    server.serve()

