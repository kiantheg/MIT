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
port = 10000
#s.connect(('localhost', port))
server_address = ('localhost', port)
s.connect(server_address)
z = hex(17)
s.sendall(z.encode())

data, address = s.recvfrom(4096)
data = data.decode('utf-8')
logger.info(data)
s.close()
