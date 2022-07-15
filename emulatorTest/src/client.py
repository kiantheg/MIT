import socket
import logging
from collections import OrderedDict

#sets up message ID counter
messageID = 0

#sets up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#sets up socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 21210
server_address = ("127.0.0.1", port)
s.connect(server_address)

#Error Code Reader
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

#connection status reader
def connectionstatus(code):
    if (code==0):
        print("Successful")
    elif (code==1):
        print("General Error")
    else:
        print("MRM already in use")

#1101
def setConfigConfirm(data, m):
    m['status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["status"])

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

#1104
def decodeServerConnect(data, m):
    m['connection status'] = int.from_bytes(data[4:8], 'big')
    connectionstatus(m["connection status"])

#1105
def MRMServerDisConfirm(data, m):
    m['status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["status"])

#1106
def setFilterConfig(data, m):
    m['status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["status"])

#1107
def decodeGetFilterConfig(data, m):
    m['filter_mask'] = int.from_bytes(data[4:6],'big')
    m['motion_filter_index'] = int.from_bytes(data[6:7],'big')
    m['reserved'] = int.from_bytes(data[7:8],'big')
    m['status'] = int.from_bytes(data[8:12],'big')
    errorCode(m["status"])

#F101
def mrm_get_statusinfo_confirm(data, m):
    m['MRM Version Major'] = int.from_bytes(data[4:5],'little')
    m['MRM Version Minor'] = int.from_bytes(data[5:6],'little')
    m['MRM Version Build'] = int.from_bytes(data[6:8],'little')
    m['UWB Kernel Major'] = int.from_bytes(data[8:9],'little')
    m['UWB Kernel Minor'] = int.from_bytes(data[9:10],'little')
    m['UWB Kernel Built'] = int.from_bytes(data[10:12],'little')
    m['FPGA Firmware Version'] = int.from_bytes(data[12:13],'little')
    m['FPGA Firmware Year'] = int.from_bytes(data[13:14],'little')
    m['FPGA Firmware Month'] = int.from_bytes(data[14:15],'little')
    m['FPGA Firmware Day'] = int.from_bytes(data[15:16],'little')
    m['Serial Number'] = int.from_bytes(data[16:22],'little')
    m['Board Version'] = int.from_bytes(data[22:23],'little')
    m['Power-On Bit Test Result'] = int.from_bytes(data[23:24],'little')
    m['Board Type'] = int.from_bytes(data[24:25],'little')
    m['Transmitter Configuration'] = int.from_bytes(data[25:26],'little')
    m['Temperature'] = int.from_bytes(data[26:30],'little')
    m['Package Version'] = int.from_bytes(data[30:62],'little')
    m['status'] = int.from_bytes(data[62:66], 'little')
    errorCode(m['status'])

#F103
def decodeOpMode(data, m):
    m['operational mode'] = int.from_bytes(data[4:8], 'big')
    m['status'] = int.from_bytes(data[8:12], 'big')
    errorCode(m["status"])

#F105
def decodeSetSleepmode(data, m):
    m['status'] = int.from_bytes(data[4:8],'big')
    errorCode(m["status"])

#F106
def decodeGetSleepmode(data, m):
    m['sleep_mode'] = int.from_bytes(data[4:8],'big')
    m['status'] = int.from_bytes(data[8:12],'big')
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
    global m
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
def encodeSetConf():
    global messageID
    message = bytes.fromhex("1001") + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    node_id = 1
    scanStart = 0 #+/-499,998 ps
    scanEnd = 200000 #+/-499,998 ps
    scan_res = 32 #1-511
    baseInter = 6 #6-15
    message = message + int.to_bytes(node_id, 4, 'big')
    message = message + int.to_bytes(scanStart, 4, 'big', signed = True)
    message = message + int.to_bytes(scanEnd, 4, 'big', signed = True)
    message = message + int.to_bytes(scan_res, 2, 'big')
    message = message + int.to_bytes(baseInter, 2, 'big')
    for i in range(4):
        message = message + int.to_bytes(0, 2, 'big')
    for i in range(4):
        message = message + int.to_bytes(0, 1, 'big')
    ant_mode = 3 #2: B->A 3: A->B
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

def encodeServerConnect():
    global messageID
    message = bytes.fromhex('1004') + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    MRMIPAddress = "127.0.0.1"
    MRMIAddress = MRMIPAddress.split(".")
    for item in MRMIAddress:
        message = message + bytes(item, 'utf-16')
    MRMIPPort = 21210
    reserved = 0
    ##message = message + bytes(MRMIPAddress, 'utf-16')
    message = message + int.to_bytes(MRMIPPort, 2, 'big')
    message = message + int.to_bytes(reserved, 2, 'big')
    return message

def encodeServerDisconnect():
    global messageID
    message = bytes.fromhex("1005") + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    return message

#1003
def encodeCtrlReq(): 
    global messageID
    message = bytes.fromhex('1003') + int.to_bytes(messageID, 2, 'big')
    messageID += 1
    scanCount = 1
    reserved = 0
    scanIntTime = 0
    message = message + int.to_bytes(scanCount, 2, 'big')
    message = message + int.to_bytes(reserved, 2, 'big')
    message = message + int.to_bytes(scanIntTime, 4, 'big')
    return message
    

def send_receive(message):
    s.sendall(message)
    data, address = s.recvfrom(4096)
    message = decodeMessage(data)
    logger.info(message)


send_receive(encodeCommConf())


send_receive(encodeSetConf())


send_receive(encodeGetConf())


send_receive(encodeCtrlReq())


data, address = s.recvfrom(4096)
message = decodeScan(data)
logger.info(message)
numtotal = message['num_messages_total']


for i in range(numtotal-1):
    data, address = s.recvfrom(4096)
    message = decodeScan(data)
    logger.info(message)


s.close()
