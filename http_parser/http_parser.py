class HTTPParser():
    """Parses an HTTP request string into its components."""
    def __init__(self):
        self.method = None
        self.uri = None
        self.http_version = None
        self.headers = {}
        self.body = None
        # self.parse_request(request_string)
    
    def parse_request(self, request_string):
        """parses an HTTP request string into its components"""
        lines = request_string.split("\r\n")
        request_line = lines[0].split()
        
        self.method = request_line[0]
        self.uri = request_line[1]
        self.http_version = request_line[2]
        
        # Parse headers
        for line in lines[1:]:
            if line == "":
                break
            header_parts = line.split(": ")
            header_name = header_parts[0]
            header_value = header_parts[1]
            self.headers[header_name] = header_value
        
        # Parse body
        if "\r\n\r\n" in request_string:
            self.body = request_string.split("\r\n\r\n")[1]
