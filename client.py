import socket
import threading

name = input("Digite seu nome: ")
server_ip = input("Digite o IP do servidor: ")
port = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))

# envia nome primeiro
client.send(name.encode())

def receber():
    while True:
        try:
            msg = client.recv(1024).decode()
            print(msg)
        except:
            break

def enviar():
    while True:
        msg = input()
        full_msg = f"{name}: {msg}"
        client.send(full_msg.encode())

threading.Thread(target=receber).start()
threading.Thread(target=enviar).start()