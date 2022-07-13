import socket
import logging
from collections import OrderedDict

global counter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 21210
server_address = ("127.0.0.1", port)
s.connect(server_address)

hex_string = "FFFE0001"
b = bytes.fromhex(hex_string)
for i in range(3):
    b = b + int.to_bytes(i+1,2**i,'little')
for i in range(3):
    b = b + int.to_bytes(-i-1,2**i,'little',signed=True)
print(b)
s.sendall(b)

def decodeCommComfirm(data):
    m = OrderedDict()
    m['message_type'] = int.from_bytes(data[0:2],'little')
    m['message_id'] = int.from_bytes(data[2:4],'little')
    m['uint8_val'] = int.from_bytes(data[4:5],'little')
    m['uint16_val'] = int.from_bytes(data[5:7],'little')
    m['uint32_val'] = int.from_bytes(data[7:11],'little')
    m['int8_val'] = int.from_bytes(data[11:12],'little',signed=True)
    m['int16_val'] = int.from_bytes(data[12:14],'little',signed=True)
    m['int32_val'] = int.from_bytes(data[14:18],'little',signed=True)
    return m
data, address = s.recvfrom(4096)
message = decodeCommComfirm(data)
logger.info(message)
s.close()
