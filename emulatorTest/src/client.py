import socket
import logging
from collections import OrderedDict

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

hex_string = "FFFE10111010101010101001"
b = bytes.fromhex(hex_string)
s.sendall(b)
def decodeCommComfirm(data):
    m = OrderedDict()
    m['message_type'] = int.from_bytes(data[0:4],'little')
    m['message_id'] = int.from_bytes(data[4:8],'little')
    m['uint8_val'] = int.from_bytes(data[8:10],'little')
    m['uint16_val'] = int.from_bytes(data[10:14],'little')
    m['uint32_val'] = int.from_bytes(data[14:22],'little')
    m['int8_val'] = int.from_bytes(data[22:24],'little',signed=True)
    m['int16_val'] = int.from_bytes(data[24:28],'little',signed=True)
    m['int32_val'] = int.from_bytes(data[28:36],'little',signed=True)
    return m
data, address = s.recvfrom(4096)
message = decodeCommComfirm(data)
logger.info(message)
s.close()
