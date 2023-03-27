import socket
import os
import logging # log server information
from Response.response import HTTPResponse
from Requests.requests import HTTPRequest
from Php_handler.php_handler import handle_request


logging.basicConfig(filename="server.log", level=logging.INFO)

WEB_ROOT = os.path.join(os.path.dirname(__file__), 'web_root')
print("WEb root is below")
print(WEB_ROOT)

class HTTPServer:
    """Custom HTTP Server to handle requests and return responses
    """
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
            

            try:
                request = HTTPRequest(request_data)
                logging.info(f"{request.method}  HTTP/1.1")
                response = HTTPResponse(500)
            except Exception as e:
                logging.error(e)
                response = HTTPResponse(500)

            # parse HTTP headers
            headers = request_data.split('\n')
            filename = headers[0].split()[1]

            

            # Request uri
            print("Request uri")
            print(request.uri)
            
            # Serve file or return 404 error
            if request.method == "GET":
                # resource_name = str(request.uri)
                resource_name = request.uri.lstrip('/')
                # asset_folder="C:\\Users\colwam\\Desktop\\Http_Server\\web_root\\"
                
                filename = os.path.join(os.getcwd(),"web_root", resource_name)
                extension = filename.split('.')
                print("The extension is: "+extension[1])
                print("File name after changing the server directory:::")
                print(filename)
                
                # server side script code:
                if extension[1] == "php":

                    print("=================")
                    print("Inside extension loop..")
                    print(filename)
                    print("===================")
                    response = handle_request(filename)
                    # Send response
                    client_socket.sendall(response.__bytes__())
                    
                    # Close connection
                    client_socket.close()
                    print(f"Server script Connection closed with {address}")
                else:
                    print("==========================")
                    print("Not .php file")
                    print(extension[1])
                    print("=================================")

                try:
                    # Open file
                    print("In the try block...")
                    f = open(filename, "rb")
                    print("File opened")
                    # Read file
                    response_body = f.read()
                    print("REsponse body====")
                    print(response_body)
                    # Close file
                    f.close()
                    # Set response headers
                    response_headers = {
                        "Content-Type": self._get_content_type(filename),
                        "Content-Length": len(response_body),
                        "Connection": "close"
                    }
                    print("Check if filename is .php")
                    print(response_headers["Content-Type"])

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
    server.serve_forever()

