import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(msg, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(msg)
            except:
                clients.remove(client)

def handle_client(conn):
    while True:
        try:
            msg = conn.recv(1024)
            broadcast(msg, conn)
        except:
            clients.remove(conn)
            conn.close()
            break

print("Servidor rodando...")

while True:
    conn, addr = server.accept()

    # primeiro dado enviado = nome do usuário
    name = conn.recv(1024).decode()
    print(f"{name} entrou de {addr}")

    clients.append(conn)

    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()