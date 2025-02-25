import socket
import logging
import pickle as pkl
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
from alive_progress import alive_bar
from Configuration import SCAN_COUNT, SCAN_START, SCAN_END, SCAN_RES, BII, SPEED_OF_LIGHT
#from constants import SPEED_OF_LIGHT

#sets up constants
messageID = 0

#sets up logger
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
s.settimeout(2)

def errorCode(code):
    ##print(messageID)
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

#F201
def decodeScan(data):
    m = OrderedDict()
    m['message_type'] = int.from_bytes(data[0:2],'big')
    m['message_id'] = int.from_bytes(data[2:4],'big')
    m['source_id'] = int.from_bytes(data[4:8],'big')
    m['timestamp'] = int.from_bytes(data[8:12],'big')
    m['scan_start'] = int.from_bytes(data[28:32],'big', signed=True)
    m['scan_stop'] = int.from_bytes(data[32:36],'big',signed=True)
    m['scan_step'] = int.from_bytes(data[36:38],'big',signed=True)
    m['scan_type'] = int.from_bytes(data[38:39],'big')
    m['antenna_id'] = int.from_bytes(data[40:41],'big')
    m['operational_mode'] = int.from_bytes(data[41:42],'big')
    m['num_samples_message'] = int.from_bytes(data[42:44],'big')
    m['num_samples_total'] = int.from_bytes(data[44:48],'big')
    m['message_index'] = int.from_bytes(data[48:50],'big')
    m['num_messages_total'] = int.from_bytes(data[50:52],'big')
    m['scan_data'] = []
    #could improve
    for i in range(m['num_samples_message']):
        m['scan_data'].append(int.from_bytes(data[52+(i*4):56+(i*4)],'big', signed=True))
    return m

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
    errorCode(m["status"])

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

#F201
def decodeScan(data):
    m = OrderedDict()
    m['message_type'] = int.from_bytes(data[0:2],'big')
    m['message_id'] = int.from_bytes(data[2:4],'big')
    m['source_id'] = int.from_bytes(data[4:8],'big')
    m['timestamp'] = int.from_bytes(data[8:12],'big')
    m['scan_start'] = int.from_bytes(data[28:32],'big', signed=True)
    m['scan_stop'] = int.from_bytes(data[32:36],'big',signed=True)
    m['scan_step'] = int.from_bytes(data[36:38],'big',signed=True)
    m['scan_type'] = int.from_bytes(data[38:39],'big')
    m['antenna_id'] = int.from_bytes(data[40:41],'big')
    m['operational_mode'] = int.from_bytes(data[41:42],'big')
    m['num_samples_message'] = int.from_bytes(data[42:44],'big')
    m['num_samples_total'] = int.from_bytes(data[44:48],'big')
    m['message_index'] = int.from_bytes(data[48:50],'big')
    m['num_messages_total'] = int.from_bytes(data[50:52],'big')
    m['scan_data'] = []
    #could improve
    for i in range(m['num_samples_message']):
        m['scan_data'].append(int.from_bytes(data[52+(i*4):56+(i*4)],'big', signed=True))
    return m


#mainDecoder
def decodeMessage(data):
    m = OrderedDict()
    m['message_type'] = int.from_bytes(data[0:2],'big')
    m['message_id'] = int.from_bytes(data[2:4],'big')
    if m['message_type'] == 65535:
        decodeCommComfirm(data, m)
    elif m['message_type'] == 4354:#1102
        decodeGetConfig(data, m)
    elif m['message_type'] == 4355:#1103
        decodeCtrlConfirm(data, m)
    elif m['message_type'] == 4359:#1107
        decodeCommComfirm(data, m)
    elif m['message_type'] == 61953: #F201
        decodeScan(data, m)
    return m

#FFFE
def encodeCommConf():
    global messageID
    message = bytes.fromhex("FFFE") + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    for i in range(3):
        message = message + int.to_bytes(i+1,2**i,'big')
    for i in range(3):
        message = message + int.to_bytes(-i-1,2**i,'big',signed=True)
    #print(b)
    return message

#1001
def encodeSetConf(scanStart, scanEnd, scan_res, baseInter):
    global messageID
    message = bytes.fromhex("1001") + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    node_id = 1
    scanEnd = int(scanEnd*2e12/SPEED_OF_LIGHT)
    message = message + int.to_bytes(node_id, 4, 'big')
    message = message + int.to_bytes(scanStart, 4, 'big', signed = True)
    message = message + int.to_bytes(scanEnd, 4, 'big', signed = True)
    message = message + int.to_bytes(scan_res, 2, 'big')
    message = message + int.to_bytes(baseInter, 2, 'big')
    for i in range(4):
        message = message + int.to_bytes(0, 2, 'big')
    for i in range(4):
        message = message + int.to_bytes(0, 1, 'big')
    ant_mode = 2 #2: B->A 3: A->B
    tx_gain_ind = 32 #0-63
    codeChannel = 7 #0-10
    persistFlag = 0 #0 - not persist 1 - will persist
    message = message + int.to_bytes(ant_mode, 1, 'big')
    message = message + int.to_bytes(tx_gain_ind, 1, 'big')
    message = message + int.to_bytes(codeChannel, 1, 'big')
    message = message + int.to_bytes(persistFlag, 1, 'big')
    return message #1001

#1002
def encodeGetConf():
    global messageID
    message = bytes.fromhex("1002") + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    return message

#1003
def encodeCtrlReq(scanCount): 
    global messageID
    message = bytes.fromhex('1003') + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    reserved = 0
    scanIntTime = 0
    message = message + int.to_bytes(scanCount, 2, 'big')
    message = message + int.to_bytes(reserved, 2, 'big')
    message = message + int.to_bytes(scanIntTime, 4, 'big')
    return message
    

def send_receive(message):
    s.sendall(message)
    try:
        data, address = s.recvfrom(4096)
        message = decodeMessage(data)
        logger.info(message)
    except:
        print("Message Dropped: #" + str(messageID))

send_receive(encodeCommConf())
send_receive(encodeSetConf(SCAN_START, SCAN_END, SCAN_RES, BII))
send_receive(encodeGetConf())
send_receive(encodeCtrlReq(SCAN_COUNT))

messageID += 1
data, address = s.recvfrom(4096)
message = decodeScan(data)
messageNum = message['num_messages_total']
datalist = np.zeros((SCAN_COUNT, message['num_samples_total']))
end = False
with alive_bar(SCAN_COUNT*messageNum) as bar:
    while not end:
        message = decodeScan(data)
        index = message['message_index']
        scan = int((message['message_id'] - 4 - index)/messageNum)
        datalist[scan][index*350:(index*350+message['num_samples_message'])] = message['scan_data']
        try:
            data, address = s.recvfrom(4096)
        except:
            print("Finished gathering data")
            end = True
        bar()