import socket
import capnp
import flask
from config import socket_file, schema_file

schemas = capnp.load(schema_file)

# create socket object
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(socket_file)

while True:
    try:
        # receive binary data
        binary_data = s.recv(4096)
        if binary_data:
            # parse as Reading object 
            print schemas.Reading.from_bytes(binary_data)

    except KeyboardInterrupt:
        # close connection
        s.close()