# Servidor para una sala de chat

import socket
from threading import Thread
from datetime import datetime



class Listener(Thread):
    '''Hilo que implementa un canal de comunicación con uno de los clientes
    conectados al servidor de la sala de chat'''

    DATA_SIZE = 1024    # 1 kilobyte para recibir datos
    def __init__(self, sock, chat_server, client_addres):
        super(Listener, self).__init__()
        self.sock = sock
        self.chat_server = chat_server
        self.client_addres=client_addres
        self.dateTime ="["+datetime.now().strftime('%Y-%m-%d || %H:%M')+"]"

    def run(self):
        try:
            while True:
                client_data=self.sock.recv(self.DATA_SIZE)
                self.chat_server.broadcast(client_data, self.sock)
        except:
            print(str(self.client_addres)+": Desconectado")
            self.sock.close()

class ChatServer:
    '''Servidor de una sala de chat'''

    def __init__(self, address, port, max_users):
        self.address = address
        self.port = port
        self.max_users = max_users  # Cuantos clientes admite
        self.sock = socket.socket()
        self.client_socks = set()  # Saca de clientes conectados (conjunto)

    def setup_sock(self):
        '''Inicializa el socket creado en el constructor'''
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, int(self.port)))
        self.sock.listen(self.max_users)

    def broadcast(self, msg, chatServer):
        '''Difunde el mensaje recibido a todos los usuarios conectados'''
        for i in self.client_socks:
            if i != chatServer:
                i.send(msg)

    def run(self):
        '''Arranca el servicio y acepta conexiones de clientes indefinidamente'''
        self.setup_sock()
        print("Servidor en funcionamiento y esperando conexiones")
        try:
            while True:
                if len(self.client_socks) >= self.max_users:
                    dato="sala llena"
                    client_connected.send(dato.encode())
                    client_connected.close()
                else:
                    client_connected, client_address = self.sock.accept()
                    self.client_socks.add(client_connected)
                    print("["+datetime.now().strftime('%Y-%m-%d || %H:%M')+"]: "+str(client_address)+":Conectado")
                    room =Listener(client_connected, self, client_address)
                    room.start()
        except:
            client_connected.close()
            self.sock.close()

if __name__ == '__main__':
    address = input("ingrese la dirección ip del servidor")
    port = input("Ingrese el puerto de conexión")
    max_users = 10
    server = ChatServer(address, port, max_users)
    server.run()
