import socket
import logging
from collections import OrderedDict

global counter
counter =  0 

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


hex_string = "FFFE" + int.to_bytes(counter, 2, 'big')
counter += 1

b = bytes.fromhex(hex_string)
for i in range(3):
    b = b + int.to_bytes(i+1,2**i,'big')
for i in range(3):
    b = b + int.to_bytes(-i-1,2**i,'big',signed=True)
print(b)
s.sendall(b)



#Error Code Reader
def errorCode(code):
    if(code == 0):
        print("Success")
    elif(code == 1):
        print("Generic Failure")
    elif(code == 2):
        print("Wrong Op Mode")
    elif(code == 3):
        print("Unsupported Value")
    elif(code == 4):
        print("Invalid During Sleep")
    elif(code == 5):
        print("Wrong Message Size")
    elif(code == 6):
        print("Not Enabled")
    elif(code == 7):
        print("Wrong Buffer Size")
    else:
        print("Unrecognized Message Type")

#connection status reader
def connectionStatus(code):
    if (code==0):
        print("Successful")
    elif (code==1):
        print("General Error")
    else:
        print("MRM already in use")
#1101
def setConfigConfirm(data, m):
    m['Status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["Status"])

#1102
def decodeGetConfig(data, m):
    m['node_id'] = int.from_bytes(data[4:8],'big')
    m['scan_start'] = int.from_bytes(data[8:12],'big',signed=True)
    m['scan_end'] = int.from_bytes(data[12:16],'big',signed=True)
    m['scan_res'] = int.from_bytes(data[16:18],'big')
    m['base_integration_index'] = int.from_bytes(data[18:20],'big')
    m['antenna_mode'] = int.from_bytes(data[20:21],'big')
    m['transmit_gain'] = int.from_bytes(data[21:22],'big')
    m['code_channel'] = int.from_bytes(data[22:23],'big')
    m['persist_flag'] = int.from_bytes(data[23:24],'big')
    m['timestamp'] = int.from_bytes(data[24:28],'big')
    m['status'] = int.from_bytes(data[28:32],'big')
    
#1103
def decodeCtrlConfirm(data, m):
    m['status'] = int.from_bytes(data[4:8], 'big')
    errorCode(m["Status"])  

#1104
def decodeServerConnect(data, m):
    m['connection status'] = int.from_bytes(data[4:8], 'big')
    connectionStatus(m["connection status"])

#1105
def MRMServerDisConfirm(data, m):
    m['Status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["Status"])   

#1106
def setFilterConfig(data, m):
    m['Status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["Status"]) 

#1107
def decodeGetFilterConfig(data, m):
    m['filter_mask'] = int.from_bytes(data[4:6],'big')
    m['motion_filter_index'] = int.from_bytes(data[6:7],'big')
    m['reserved'] = int.from_bytes(data[7:8],'big')
    m['status'] = int.from_bytes(data[8:12],'big')
    errorCode(m["Status"]) 

#F103
def decodeOpMode(data, m):
    m['operational mode'] = int.from_bytes(data[4:8], 'big')
    m['status'] = int.from_bytes(data[8:12], 'big')
    errorCode(m["Status"])

#F105
def decodeSetSleepmode(data, m):
    m['status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["Status"])

#F106
def decodeGetSleepmode(data, m):
    m['sleep_mode'] = int.from_bytes(data[4:8],'big')
    m['status'] = int.from_bytes(data[8:12],'big')
    errorCode(m["Status"])

#FFFF
def decodeCommComfirm(data, m):
    m['uint8_val'] = int.from_bytes(data[4:5],'big')
    m['uint16_val'] = int.from_bytes(data[5:7],'big')
    m['uint32_val'] = int.from_bytes(data[7:11],'big')
    m['int8_val'] = int.from_bytes(data[11:12],'big',signed=True)
    m['int16_val'] = int.from_bytes(data[12:14],'big',signed=True)
    m['int32_val'] = int.from_bytes(data[14:18],'big',signed=True)
    m['char[15]'] = data[18:33]
    m['status'] = int.from_bytes(data[33:37],'big')
    errorCode(m['status'])

def decodeMessage(data):
    m = OrderedDict()
    m['message_type'] = int.from_bytes(data[0:2],'big')
    m['message_id'] = int.from_bytes(data[2:4],'big')
    if m['message_type'] == 65535:
        decodeCommComfirm(data, m)
    elif m['message_type'] == 4353:#1101
        setConfigConfirm(data, m)
    elif m['message_type'] == 4354:#1102
        decodeGetConfig(data, m)
    elif m['message_type'] == 4355:#1103
        decodeCtrlConfirm(data, m)
    elif m['message_type'] == 4356:#1104
        decodeServerConnect(data, m)
    elif m['message_type'] == 4357:#1105
        MRMServerDisConfirm(data, m)
    elif m['message_type'] == 4358:#1106
        setFilterConfig(data, m)
    elif m['message_type'] == 4359:#1107
        decodeCommComfirm(data, m)
    elif m['message_type'] == 61699:#F103
        decodeOpMode(data, m)
    elif m['message_type'] == 61701:#F105
        decodeSetSleepmode(data, m)
    elif m['message_type'] == 61702:#F106
        decodeGetSleepmode(data, m)
    return m


data, address = s.recvfrom(4096)
message = decodeMessage(data)
logger.info(message)
s.close()
