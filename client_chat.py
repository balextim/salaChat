# Cliente para una sala de chat

import socket
from threading import Thread
from datetime import datetime



class Listener(Thread):
    '''Hilo que implementa un canal de comunicación entre el servidor
    que proporciona el servicio de una sala de chat y el cliente actual'''
    DATA_SIZE = 1024    # 1 kilobyte para recibir datos

    def __init__(self, sock):
        super(Listener, self).__init__()
        self.sock = sock
        self.dateTime="["+datetime.now().strftime('%Y-%m-%d || %H:%M')+"]"

    def run(self):
        try:
            while True:
                data=self.sock.recv(self.DATA_SIZE)
                print(self.dateTime+": "+data.decode())
        except:
            self.sock.close()
            exit()


class ChatClient:
    '''Cliente para el servidor de una sala de chat'''

    def __init__(self, address, port, nickname):
        self.address = address
        self.port = port
        self.nickname = "<"+nickname+"> "
        self.sock = socket.socket()

    def setup_sock(self):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       #para relaizar la conexión con el servidor
        try:
            self.sock.connect((self.address, int(self.port)))
        except:
            self.sock.close()

    def run(self):
        self.setup_sock()
        print("Puede empezar a escribir")
        try:
            while True:
                listener=Listener(self.sock)
                listener.start()
                my_data=self.nickname+input()
                self.sock.send(my_data.encode())
        except:
            self.sock.close()

if __name__ == '__main__':
    address = input("ingrese la dirección ip del servidor")
    port = input("Ingrese el puerto de conexión")
    nickname = input("Introduzca su nombre de usuario>")
    client = ChatClient(address, port, nickname)
    client.run()

