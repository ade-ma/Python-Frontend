import socket, os, os.path, time
import random, msgpack, config, sys

# construct example data
def sample_message(msg_length):
    return msgpack.packb([random.random() for i in range(msg_length)])

# setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = (socket.gethostname(), config.socket_port)

size = len(config.schema)
while True:# send binary message
    try:
        sock.sendto(sample_message(size), addr)
        time.sleep(1)
    except KeyboardInterrupt:
        # close connection
        sys.exit(0)