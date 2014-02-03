import socket
import os, os.path, time
import random
import capnp
from config import socket_file, schema_file

schemas = capnp.load(schema_file)

# construct example data
def sample_message():
    sample_data = schemas.Reading.new_message()
    stream_length = random.randint(0, 1024)
    raw_values = sample_data.init('lower', stream_length)
    for i in range(stream_length):
        raw_values[i] = random.choice([True, False])
    sample_data.sensorType = random.choice(["temperature", "relativeHumidity"])
    sample_data.sensorConstant = random.randint(0, 1024)
    sample_data.sensorReading = random.random()
    sample_data.readingTimestamp = random.random()
    return sample_data

# setup socket
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if os.path.exists(socket_file): 
    os.remove(socket_file)
s.bind(socket_file)
s.listen(1)

# establish connection with client 
conn, addr = s.accept()

# send binary message
conn.send(sample_message().to_bytes())

# close connection
conn.close()
