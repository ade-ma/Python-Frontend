import socket, os, os.path, time
import random, msgpack, config, sys
from time import gmtime, strftime

# construct example data
def sample_message():
    type = random.choice(["temperature", "relativeHumidity"])
    timestamp = strftime("%m/%d/%Y %H:%M:%S", gmtime())
    lower = random.random()
    uid = random.randint(0, 1024)
    measurement = random.random()
    return msgpack.packb([type, timestamp, lower, uid, measurement])

# setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = (socket.gethostname(), config.socket_port)

while True:# send binary message
    try:
        sock.sendto(sample_message(), addr)
        time.sleep(1)
    except KeyboardInterrupt:
        # close connection
        sys.exit(0)