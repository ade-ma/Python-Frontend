#!/usr/bin/env python -B

import time, msgpack, multiprocessing, socket, config, csv, os, os.path, db, sys
import pprint

class Monitor(multiprocessing.Process):

    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.q = q
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((config.socket_addr, config.socket_port))

    def close(self):
        self.sock.close()

    def parsed(self, binary_data):
        return dict(zip(config.schema, binary_data))

    def run(self):
        while True:
            binary_data, addr = self.sock.recvfrom(config.chunk_size)
            if binary_data:
                d = self.parsed(msgpack.unpackb(binary_data))
                db.add(d).callback(True)
                self.q.put(d, True)