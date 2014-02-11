import socket, time
import capnp
from flask import Flask
from config import socket_file, schema_file, poll_interval

app = Flask(__name__)

def listen(s):
    while True:
        try:
            # receive binary data
            binary_data = s.recv(4096)
            if binary_data:
                # parse as Reading object 
                print schemas.Reading.from_bytes(binary_data)
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            # close connection
            s.close()

if __name__ == "__main__":
    schemas = capnp.load(schema_file)

    # create socket object
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(socket_file)

    # begin listening for data emitted
    listen(s)