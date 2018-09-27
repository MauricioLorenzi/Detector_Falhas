import os
import socket
import _thread
import time

MESSAGE_REQUEST = "HeartbeatRequest"
MESSAGE_RESPONSE = "HeartbeatReply"
MESSAGE_REQUEST_PROCESS = "ProcessRequest"
MESSAGE_PROCESS_RESPONSE_YES = "ProcessAnswerYes;" 
MESSAGE_PROCESS_RESPONSE_NO = "ProcessAnswerNo" 
MESSAGE_PROCESS_STOP = "ProcessStop"

UDP_IP = "10.110.5.244"
UDP_SEND_PORT = 6000
UDP_RECEIVE_PORT = 6001

SEND_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SEND_SOCKET.bind((UDP_IP, UDP_SEND_PORT))

LISTEN_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LISTEN_SOCKET.bind((UDP_IP, UDP_RECEIVE_PORT))

ALL_IPS = ["10.110.5.244", "10.110.4.245"]
MUTEX = _thread.allocate_lock()
ALIVE = ["10.110.5.244", "10.110.4.245"]
DETECTED = []
LEADER = ""
PROCESS_NUMBER_RANGE = []
PROCESS_TO_SEND = []
CAN_PROCESS = False

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

        elif LEADER is UDP_IP and message_received == MESSAGE_REQUEST_PROCESS:
            PROCESS_TO_SEND.append(ip_sender)

        elif CAN_PROCESS is True and message_received == MESSAGE_PROCESS_STOP and ip_sender == LEADER:
            CAN_PROCESS = False


def thread_hash():
    found_hash = False
    while True:
        if LEADER != "" and LEADER != UDP_IP:
            time.sleep(2)
            SEND_SOCKET.sendto(MESSAGE_REQUEST_PROCESS.encode(), (LEADER, UDP_RECEIVE_PORT))
            while CAN_PROCESS is True and found_hash is False:            
                print("\nProcessing Hash {}".format(PROCESS_NUMBER_RANGE))
                found_hash = True


def thread_leader():
    while True:
        for ip in PROCESS_TO_SEND:
            if ip != UDP_IP:
                time.sleep(2)
                SEND_SOCKET.sendto("numbers range to calculate hash".encode(), (ip, UDP_RECEIVE_PORT))  
            #execute proccess

_thread.start_new_thread(thread_send, ())
_thread.start_new_thread(thread_listen, ())
_thread.start_new_thread(thread_leader, ())
_thread.start_new_thread(thread_hash, ())

while True:
    pass