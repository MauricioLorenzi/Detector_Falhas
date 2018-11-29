#Bruno de Castro RA: 140576
#Gabriel Nistardo RA: 140839
#Mauricio Luis de Lorenzi RA: 141269
#Giovanni Garcia Ribeiro de Souza RA: 140872

import os
import socket
import _thread
import time
import requests
import hashlib

MESSAGE_REQUEST = "HeartbeatRequest"
MESSAGE_RESPONSE = "HeartbeatReply"
MESSAGE_PROCESS_REQUEST = "ProcessRequest"
MESSAGE_PROCESS_RESPONSE = "Process;[{}];[{}];[{}];[{}];[{}]" #"Process;[inicio];[fim];[timestamp];[hash];[zeros]"
MESSAGE_PROCESS_RESPONSE_YES = "ProcessAnswerYes;{}" #"ProcessAnswerYes;1234"
MESSAGE_PROCESS_RESPONSE_NO = "ProcessAnswerNo" 
MESSAGE_PROCESS_STOP = "ProcessInterrupt"
POOL_NAME = "PISCINA DO MAUMAU"
WEB_SERVER_BLOCKCHAIN_RESPONSE_URL = "http://mineracao-facens.000webhostapp.com/submit.php?timestamp={}&nonce={}&poolname={}"
WEB_SERVER_BLOKCHAIN_REQUEST_URL = "http://mineracao-facens.000webhostapp.com/request.php"

UDP_IP = "172.18.3.174"
UDP_SEND_PORT = 6000
UDP_RECEIVE_PORT = 6001

SEND_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SEND_SOCKET.bind((UDP_IP, UDP_SEND_PORT))

LISTEN_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LISTEN_SOCKET.bind((UDP_IP, UDP_RECEIVE_PORT))

ALL_IPS = ["172.18.3.174", "172.18.2.221", "172.18.1.52"]
MUTEX = _thread.allocate_lock()
ALIVE = ["172.18.3.174", "172.18.2.221", "172.18.1.52"]
DETECTED = []
LEADER = ""
PROCESS_NUMBER_RANGE = []
PROCESS_TO_SEND = []
CAN_PROCESS = False
HASH_INTERVAL = 0
TIMESTAMP = int(time.time())
INITIAL_INTERVAL = 0
END_INTERVAL = 0
TIMESTAMP_FROM_LEADER = 0
LAST_HASH = ""
ZEROS = 0
SHA_ALGORITHM = hashlib.sha256()

clear = lambda: os.system('cls')

def thread_send():
    global LEADER
    while True:            
        for p in ALL_IPS:
            try:
                SEND_SOCKET.sendto(MESSAGE_REQUEST.encode(), (p, UDP_RECEIVE_PORT))
            except:
                if p not in DETECTED:
                    DETECTED.append(p)
        time.sleep(2)        
        
        for ip in ALL_IPS:
            if ip in ALIVE:
                LEADER = ip
                break
                 
        MUTEX.acquire()
        for ip in ALL_IPS:
            if ip not in ALIVE and ip not in DETECTED:
                DETECTED.append(ip)
        clear()
        print("Todos Ips => {}".format(ALL_IPS))
        print("Vivos => {}".format(ALIVE))
        print("Mortos => {}".format(DETECTED))
        print("Lider => {} \n".format(LEADER))
        ALIVE.clear()
        MUTEX.release()                                        

def thread_listen():    
    global CAN_PROCESS
    global TIMESTAMP
    global HASH_INTERVAL
    while True:
        message_received, ip_sender = LISTEN_SOCKET.recvfrom(1024)
        ip_sender = ip_sender[0]
        message_received = message_received.decode()
        
        if message_received != UDP_IP:    
            print("\nMensagem recebida => {} enviado por => {}".format(message_received, ip_sender))
        
        if message_received == MESSAGE_REQUEST:
            SEND_SOCKET.sendto(MESSAGE_RESPONSE.encode(), (ip_sender, UDP_RECEIVE_PORT))       

        elif message_received == MESSAGE_RESPONSE:                
            if ip_sender not in ALIVE and ip_sender not in DETECTED and not MUTEX.locked():
                ALIVE.append(ip_sender)

        elif LEADER is UDP_IP and message_received == MESSAGE_PROCESS_REQUEST:
            PROCESS_TO_SEND.append(ip_sender)

        elif CAN_PROCESS is True and message_received == MESSAGE_PROCESS_STOP and ip_sender == LEADER:
            CAN_PROCESS = False
        
        elif message_received.split(";")[0] == MESSAGE_PROCESS_RESPONSE_YES.split(";")[0]:
            requests.post(WEB_SERVER_BLOCKCHAIN_RESPONSE_URL.format(TIMESTAMP, message_received.split(";")[1], POOL_NAME))  
            TIMESTAMP = int(time.time())
            HASH_INTERVAL = 0

        elif message_received == MESSAGE_PROCESS_RESPONSE_NO:
            SEND_SOCKET.sendto(format_response().encode(), (ip_sender, UDP_RECEIVE_PORT))
              
        elif message_received.split(";")[0] == MESSAGE_PROCESS_RESPONSE.split(";")[0]:
            message = message_received.split(";")
            INITIAL_INTERVAL = message[1]
            END_INTERVAL = message[2]
            TIMESTAMP_FROM_LEADER = message[3]
            LAST_HASH = message[4]
            ZEROS = int(message[5])
            CAN_PROCESS = True
                 

def thread_hash():
    global INITIAL_INTERVAL
    found_hash = False
    sent_request = False
    while True:
        if LEADER != "" and LEADER != UDP_IP:
            time.sleep(2)
            
            if sent_request is False:
                SEND_SOCKET.sendto(MESSAGE_PROCESS_REQUEST.encode(), (LEADER, UDP_RECEIVE_PORT))
                sent_request = True
            
            while CAN_PROCESS is True and found_hash is False:            
                SHA_ALGORITHM.update(LAST_HASH + INITIAL_INTERVAL + TIMESTAMP_FROM_LEADER)
                hash = SHA_ALGORITHM.hexdigest()

                if hash.count("0") >= ZEROS:
                    SEND_SOCKET.sendto(MESSAGE_PROCESS_RESPONSE_YES.format(INITIAL_INTERVAL).encode(), (LEADER, UDP_RECEIVE_PORT))
                    found_hash = True
                else:
                    if INITIAL_INTERVAL <= END_INTERVAL:
                        INITIAL_INTERVAL = INITIAL_INTERVAL + 1
                    else:                        
                        SEND_SOCKET.sendto(MESSAGE_PROCESS_RESPONSE_NO, (LEADER, UDP_RECEIVE_PORT))
                        sent_request = False
                


def thread_leader():
    while True:
        if LEADER == UDP_IP:     
            time.sleep(2)                      
            for ip in PROCESS_TO_SEND:
                SEND_SOCKET.sendto(format_response().encode(), (ip, UDP_RECEIVE_PORT))
            PROCESS_TO_SEND.clear()
                
def format_response(): 
    request = requests.get(WEB_SERVER_BLOKCHAIN_REQUEST_URL)
    request_json = request.json()
    hash_range = Calculate_Interval()
    
    if hash_range is not None:
        return MESSAGE_PROCESS_RESPONSE.format(hash_range[0], hash_range[1], TIMESTAMP, request_json['hash'], request_json['zeros'])

def Calculate_Interval():
    global HASH_INTERVAL
    max_range = 2000000000
    block_lenght = 50000    
    
    first_range = HASH_INTERVAL * block_lenght

    HASH_INTERVAL = HASH_INTERVAL + 1
    value_interval = [first_range, block_lenght * HASH_INTERVAL]
    
    if value_interval <= max_range:
        TIMESTAMP = int(time.time())
        HASH_INTERVAL = 0

    return value_interval


_thread.start_new_thread(thread_send, ())
_thread.start_new_thread(thread_listen, ())
_thread.start_new_thread(thread_leader, ())
_thread.start_new_thread(thread_hash, ())

while True:
    pass