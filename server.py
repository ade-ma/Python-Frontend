#!/usr/bin/env python -B

import socket, os, os.path, time
import random, msgpack, config, sys
import time

# construct example data
def sample_message():
    type = random.randint(0, 1)
    timestamp = time.time()*1000
    lower = random.random()
    uid = random.randint(0, 1024)
    measurement = random.random()
    return msgpack.packb([lower, type, uid, measurement, timestamp])

# setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = (config.socket_addr, config.socket_port)

while True:# send binary message
    try:
        sock.sendto(sample_message(), addr)
        time.sleep(1)
    except KeyboardInterrupt:
        # close connection
        sys.exit(0)