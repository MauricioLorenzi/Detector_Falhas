import os
import socket
import _thread
import time

MESSAGE = bytearray()
MESSAGE_2 = bytearray()

MESSAGE.append(1)
MESSAGE_2.append(2)

UDP_IP = "172.18.3.100"
UDP_SEND_PORT = 6000
UDP_RECEIVE_PORT = 6001

SEND_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SEND_SOCKET.bind((UDP_IP, UDP_SEND_PORT))

LISTEN_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LISTEN_SOCKET.bind((UDP_IP, UDP_RECEIVE_PORT))

ALL_IPS = ["172.18.1.41", "172.18.2.209", "172.18.3.100", "172.17.98.96", "172.18.1.52"]
MUTEX = _thread.allocate_lock()
ALIVE = ["172.18.1.41", "172.18.2.209", "172.18.3.100", "172.17.98.96", "172.18.1.52"]
DETECTED = []
LEADER = ""

clear = lambda: os.system('cls')

def thread_send():
    global LEADER
    while True:            
        for p in ALL_IPS:
            try:
                SEND_SOCKET.sendto(MESSAGE, (p, UDP_RECEIVE_PORT))
            except:
                if p not in DETECTED:
                    DETECTED.append(p)
        time.sleep(2)        

        if LEADER not in ALIVE:
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
    while True:
        message_received, ip_sender = LISTEN_SOCKET.recvfrom(1024)
        ip_sender = ip_sender[0]
        message_received = message_received[0]
        
        if message_received != UDP_IP:    
            print("\nMensagem recebida => {} enviado por => {}".format(str(message_received), ip_sender))
        
        if message_received == 1:
            SEND_SOCKET.sendto(MESSAGE_2, (ip_sender, UDP_RECEIVE_PORT))       

        elif message_received == 2:                
            if ip_sender not in ALIVE and not MUTEX.locked():
                ALIVE.append(ip_sender)

_thread.start_new_thread(thread_send, ())
_thread.start_new_thread(thread_listen, ())

while True:
    pass