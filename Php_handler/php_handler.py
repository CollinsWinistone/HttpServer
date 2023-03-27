import os
import subprocess

def handle_request(file_path):
    #current file
    php_output = subprocess.check_output(['php', file_path])

    print("==========================")
    print("We are inside subprocess module.....")
    print("==========================")
    # Send the PHP output back to the client as the response
    response = 'HTTP/1.1 200 OK\n\n' + php_output.decode('utf-8')
  
    return response


