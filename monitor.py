import time, msgpack, multiprocessing, socket, config

class Monitor(multiprocessing.Process):

    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.q = q
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((socket.gethostname(), config.socket_port))

    def close(self):
        self.sock.close()

    def parsed(self, binary_data):
        return dict(zip(config.schema, binary_data))

    def run(self):
        while True:
            binary_data, addr = self.sock.recvfrom(config.chunk_size)
            if binary_data:
                d = msgpack.unpackb(binary_data)
                self.q.put(self.parsed(d), True)