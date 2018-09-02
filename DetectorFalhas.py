import socket
import _thread
import time

MESSAGE = b"1"
MESSAGE_2 = b"2"
UDP_IP = "127.0.0.1"
UDP_SEND_PORT = 6002
UDP_RECEIVE_PORT = 6001

#all_proc = ["172.18.2.188", "172.18.1.52", "172.18.3.181", "172.18.1.69", "172.18.1.69", "172.18.1.64"]
all_proc = ["127.0.0.2"]
mutex = _thread.allocate_lock()
alive = ["127.0.0.2"]
detected = []

def listen():
    sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_listen.bind(("", UDP_RECEIVE_PORT))

    message_received, ip_sender = sock_listen.recvfrom(1024)
    print("\nSender: {} => Mensagem recebida: {}".format(ip_sender, message_received))
    
    if message_received is MESSAGE:                        
        oldtime = time.time()

        while time.time() - oldtime < 3:
            sock_listen.bind(("", UDP_RECEIVE_PORT))
            message_received_2, ip_sender_2 = sock_listen.recvfrom(1024)

        if message_received_2 is MESSAGE_2:
            mutex = _thread.allocate_lock()
            with mutex:                    
                mutex.acquire()
                alive.append(ip_sender_2)
                mutex.release()

def response(ip):    
    sock_response = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_response.settimeout(5)
    sock_response.sendto(MESSAGE, (UDP_IP, UDP_SEND_PORT))

def sendException(p):
    print("\nprocesso {} esta com falha".format(p))

def thread_send():
    while True:            
        for p in all_proc:
            if p not in alive and p not in detected:
                detected.append(p)
                sendException(p)
            time.sleep(10)
            response(p)
        alive.clear()

def thread_listen():    
    while True:
        listen()

def thread_print():
    while True:
        time.sleep(10)        
        print("\nVivos => {}".format(alive))
        print("\nDetectados => {}".format(detected))

time.sleep(5)
_thread.start_new_thread(thread_listen, ())
_thread.start_new_thread(thread_send, ())
_thread.start_new_thread(thread_print, ())       

while True:
    pass