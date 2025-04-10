import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

def unpad(data):
    return data[:-ord(data[len(data)-1:])]


def ECB_encrypt(key, data):
    iv = Random.new().read(AES.block_size)
    data = pad(data)
    print(data)
    cipher = AES.new(key, AES.MODE_ECB, iv)
    encrypted_text = cipher.encrypt(data.encode())

    return encrypted_text


def ECB_decrypt(key, encrypted_text):

    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(encrypted_text)

    print(decrypted_text)

    decrypted_text = unpad(decrypted_text)

    return decrypted_text


def ECB_Mode(data, key):
    encrypted_text = ECB_encrypt(key, data)

    print(key)
    print(encrypted_text)

    decrypted_text = ECB_decrypt(key, encrypted_text)
    print(decrypted_text)


def CBC_Mode(data, key):
    pass


if __name__ == "__main__":
    
    data = "secret12"

    key = Random.get_random_bytes(16)
    key = b"1234567890123456"

    ECB_Mode(data, key)

    CBC_Mode(data, key)

    