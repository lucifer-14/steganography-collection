import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AES_Cipher:
    
    def __init__(self, key: str, mode : str ="ECB" ) -> None:
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()
        # if mode == "ECB":
        self.mode = AES.MODE_ECB
        # elif mode == "CBC":
        #     self.mode = AES.MODE_CBC
        #     self.iv = Random.new().read(self.block_size)
        

    def encrypt(self, data: str) -> bytes:

        # print(len(data))
        data = self._pad(data)
        # print(data)
        # print(len(data))

        cipher = AES.new(self.key, self.mode)
        ciphertext = cipher.encrypt(data.encode())

        return ciphertext
    
    def decrypt(self, ciphertext: bytes) -> str:

        cipher = AES.new(self.key, self.mode)
        decrypted_text = cipher.decrypt(ciphertext)

        decrypted_text = self._unpad(decrypted_text)
        
        return decrypted_text.decode()
        

    def _pad(self, d: str) -> str:
        
        return d + (self.block_size - len(d) % self.block_size) * chr(self.block_size - len(d) % self.block_size)


    @staticmethod
    def _unpad(d: bytes) -> bytes:
        return d[:-d[-1]]