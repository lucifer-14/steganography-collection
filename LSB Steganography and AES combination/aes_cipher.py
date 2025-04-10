import base64
import hashlib
from Crypto.Cipher import AES

class AES_Cipher:
    
    def __init__(self, key: str, mode : str ="ECB" ) -> None:
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()
        if mode == "ECB":
            self.mode = AES.MODE_ECB
        # elif mode == "CBC":
        #     self.mode = AES.MODE_CBC
        #     self.iv = Random.new().read(self.block_size)
        

    def encrypt(self, data: bytes) -> bytes:

        # print(len(data))
        data = self._pad(data)
        # print(data)
        # print(len(data))

        cipher = AES.new(self.key, self.mode)
        ciphertext = cipher.encrypt(data)

        return ciphertext
    
    def decrypt(self, ciphertext: bytes) -> bytes:

        cipher = AES.new(self.key, self.mode)
        decrypted_text = cipher.decrypt(ciphertext)

        decrypted_text = self._unpad(decrypted_text)
        
        return decrypted_text
        

    def _pad(self, d: bytes) -> bytes:
        # print(chr(self.block_size - len(d) % self.block_size))
        # print('len of d', len(d))
        # print('len of sth ', (self.block_size - len(d) % self.block_size))
        # print('res', (self.block_size - len(d) % self.block_size) * chr(self.block_size - len(d) % self.block_size))
        # print('type', type((self.block_size - len(d) % self.block_size) * chr(self.block_size - len(d) % self.block_size)))
        # print('res', bytes(self.block_size - len(d) % self.block_size) * chr(self.block_size - len(d) % self.block_size))
        return d + bytes((self.block_size - len(d) % self.block_size) * chr(self.block_size - len(d) % self.block_size), 'UTF-8')


    @staticmethod
    def _unpad(d: bytes) -> bytes:
        return d[:-d[-1]]