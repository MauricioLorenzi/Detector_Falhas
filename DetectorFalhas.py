import socket

UDP_SEND_IP = "127.0.0.1"
UDP_SEND_PORT = 6000
SEND_MESSAGE = "1"

UDP_RECEIVE_IP = "127.0.0.1"
UDP_RECEIVE_PORT = 6001

def start:
    alive = []
    all_proc = []
    detected = []
    
    while True:
        ip = input("Digite um ip (para sair digite \'n\'): ")
        
        if ip == 'n':
            break

def ListenAll:


def ResponseAll(_p):
    vivos.__add__(_p)

def SendException(_p):
    print("processo esta com falha")

for p in all_proc:
    if not vivos.contains(p) and not detected.contains(p):
        detected.__add__(p)
        SendException(p)
    ResponseAll(p)
        