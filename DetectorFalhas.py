import os
import socket
import _thread
import time

MESSAGE = b"1"
MESSAGE_2 = b"2"
UDP_IP = "172.18.3.100"
UDP_SEND_PORT = 6000
UDP_RECEIVE_PORT = 6001

SEND_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SEND_SOCKET.bind((UDP_IP, UDP_SEND_PORT))

LISTEN_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LISTEN_SOCKET.bind((UDP_IP, UDP_RECEIVE_PORT))

all_proc = ["127.0.0.1", "127.0.0.2"]
mutex = _thread.allocate_lock()
alive = ["127.0.0.1", "127.0.0.2"]
detected = []
leader = None

clear = lambda: os.system('cls')

def listen():
    message_received, ip_sender = LISTEN_SOCKET.recvfrom(1024)
    ip_sender = ip_sender[0]

    message_received = ord(message_received)
    
    if message_received != UDP_IP:    
        print("\nMensagem recebida => {} enviado por => {}".format(str(message_received), ip_sender))
    
    if message_received is 1:
        response(ip_sender)        

    if message_received is 2:
        mutex = _thread.allocate_lock()
        with mutex:                    
            mutex.acquire()
            if ip_sender not in alive:
                alive.append(ip_sender)
            mutex.release()

def response(ip):   
    try:
        SEND_SOCKET.sendto(MESSAGE, (ip, UDP_SEND_PORT))
    except:
        if ip not in alive and ip not in detected:
            detected.append(ip)
            sendException(ip)

def sendException(ip):
    print("\nprocesso {} esta com falha".format(ip))

def thread_send():
    while True:            
        for p in all_proc:
            response(p)
        time.sleep(3)

        mutex = _thread.allocate_lock()

        with mutex:                    
            mutex.acquire()
            alive.clear()
            mutex.release()

def thread_listen():    
    while True:
        listen()

def thread_print():
    while True:
        time.sleep(5)
        clear()
        #with mutex:                    
         #   mutex.acquire()
        print("Todos => {}".format(all_proc))       
        print("Vivos => {}".format(alive))
        print("Mortos => {}".format(detected))
        print("Lider => {} \n".format(leader))
          #  mutex.release()

time.sleep(5)
_thread.start_new_thread(thread_listen, ())
_thread.start_new_thread(thread_send, ())
_thread.start_new_thread(thread_print, ())       

while True:
    pass