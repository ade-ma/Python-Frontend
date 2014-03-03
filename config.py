import os
csv_root = 'static/csvs/'
dirname = os.path.dirname(__file__)
static_path = os.path.join(dirname, 'static')
db_file = "readings.db"
chunk_size = 1024
poll_interval = 1
queue_size = 64
schema = ["DataType", "Timestamp", "Lower", "UID", "Measurement"]
datatype_mapping = {0: "Temperature", 1: "RelativeHumidity"}
server_port = 8888
socket_addr = "127.0.0.1"
socket_port = 9999
