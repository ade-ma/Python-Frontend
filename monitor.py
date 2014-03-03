import time, msgpack, multiprocessing, socket, config, csv, os.path

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
                d = self.parsed(msgpack.unpackb(binary_data))
                csv_path = os.path.join(config.csv_root, config.datatype_mapping[d['DataType']] + ".csv")
                with open(csv_path, 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    self.q.put(d, True)
                    writer.writerow([d['Timestamp'], d['Measurement']])