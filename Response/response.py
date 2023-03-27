class HTTPResponse:
    """
        A class to represent Http response.
    """
    def __init__(self, status, headers=None, body=None):
        self.status = status
        self.headers = headers or {}
        self.body = body or b""
    
    def __bytes__(self):
        """Returns the bytes representation of the HTTP response"""
        status_line = f"HTTP/1.1 {self.status}\r\n"
        header_lines = [f"{key}: {value}\r\n" for key, value in self.headers.items()]
        header_block = "".join(header_lines)
        response = status_line + header_block + "\r\n" + self.body.decode("utf-8")
        return response.encode("utf-8")