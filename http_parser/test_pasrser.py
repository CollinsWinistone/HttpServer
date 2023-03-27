from http_parser import HTTPRequest

request_string = "GET /hello.txt HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
request = HTTPRequest(request_string)

print(request.method) # "GET"
print(request.uri) # "/hello.txt"
print(request.http_version) # "HTTP/1.1"
print(request.headers) # {"Host": "example.com", "Connection": "close"}
print(request.body) # None
