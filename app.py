# IGNORE THIS FILE
# UNUSED, ALL RELEVANT FILES ARE IN THE 
# BIN AND DATABASE DIRECTORIES

import os
from flask import Flask
import socket
from socket import AF_INET, SOCK_DGRAM

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)