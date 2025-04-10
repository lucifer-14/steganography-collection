import socket
import threading

class Server:
    def __init__(self, IP, PORT) -> None:
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = IP
        self.PORT = PORT
        
    
    def initiate_server(self):
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()
        self.conn, self.addr = self.socket.accept()
        return self.conn

    def client_handler(self) -> bytes:
        return self.conn.recv(1024)
    
    def send(self, message: bytes) -> None:
        self.conn.send(message)

        # thread = threading.Thread(target=self.client_handler)
        # thread.start()