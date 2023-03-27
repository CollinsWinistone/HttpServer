
class HTTPRequest:
    """A class to represent an HTTP request."""
    def __init__(self, request_string):
        self.method = None
        self.uri = None
        self.http_version = None
        self.headers = {}
        self.body = None
        
        self.parse_request(request_string)
    
    def parse_request(self, request_string):
        """Parses an HTTP request string into its components."""
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