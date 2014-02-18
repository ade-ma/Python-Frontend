import os
csv_root = 'static/csvs/'
dirname = os.path.dirname(__file__)
static_path = os.path.join(dirname, 'static')
db_file = "readings.db"
chunk_size = 4096
poll_interval = 1
queue_size = 64
schema = ["DataType", "Timestamp", "Lower", "UID", "Measurement"]
server_port = 8888
socket_port = 9999