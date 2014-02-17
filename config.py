import os
dirname = os.path.dirname(__file__)
static_path = os.path.join(dirname, 'static')
db_file = "readings.db"
chunk_size = 4096
poll_interval = 1
queue_size = 64
schema = ["Lower", "DataType", "UID", "Measurement", "Timestamp"]
server_port = 8888
socket_port = 9999