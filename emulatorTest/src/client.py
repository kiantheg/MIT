import socket
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 21210
#s.connect(('localhost', port))
server_address = ("127.0.0.1", port)
s.connect(server_address)

hex_string = "1001"
b = bytes.fromhex(hex_string)
s.sendall(b)

data, address = s.recvfrom(4096)
data = data.decode('utf-8')
logger.info(data)
s.close()

