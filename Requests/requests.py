
class HTTPRequest:
    """A class to represent an HTTP request."""
    def __init__(self, request_string,method,uri,http_version,headers,body):
        self.method = method
        self.uri = uri
        self.http_version = http_version
        self.headers = headers
        self.body = body
        # self.parser = HTTPParser(request_string)
        # self.parser.parse_request(request_string)
        # parser_obj.parse_request(request_string)
        # print(parser_obj.body)
        # # self.parse_request(request_string)
    
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