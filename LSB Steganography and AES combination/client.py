import socket

class Client:
    def __init__(self, IP, PORT) -> None:
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = IP
        self.PORT = PORT
        
    
    def initiate_client(self):
        self.socket.connect((self.IP, self.PORT))
        return self.socket

    def connection_handler(self) -> bytes:
        return self.socket.recv(1024)
    
    def send(self, message: bytes) -> None:
        self.socket.send(message)