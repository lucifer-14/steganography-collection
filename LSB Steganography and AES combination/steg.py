import cv2
import numpy as np
import sys
import time
import aes_cipher

class Steg:

    def __init__(self, image = "", stego = "", delimiter = b"***EOD***", LSB = 1) -> None:
        if not isinstance(image, np.ndarray):
            self.image = cv2.imread(image)
        else:
            self.image = image
        self.stego_path = stego
        self.stego = cv2.imread(stego)
        self.delimiter = delimiter
        self.LSB = LSB

    @staticmethod
    def to_binary(data):

        if isinstance(data, bytes):
            return "".join([format(i, "08b") for i in data])
        elif isinstance(data, np.ndarray):
            return [format(i, "08b") for i in data]

    def get_max_capacity(self) -> int:
        delimiter_bits = len(self.delimiter) * 8
        capacity = self.image.shape[0] * self.image.shape[1] *  3 * self.LSB
        capacity = capacity - (capacity % 8)            # removing excess bits caused by the shape of image
        capacity = capacity - delimiter_bits - ((capacity - delimiter_bits) % 128) - 8
        return capacity

    def embed(self, message: bytes) -> np.ndarray:
        
        message = message + self.delimiter
        max_bits = self.get_max_capacity()
        max_bytes = max_bits // 8

        # print('Max capacity bits:', max_bits)
        # print('Max capacity bytes:', max_bytes)

        if len(message) > max_bytes:
            print("Not Enough Capacity")
            sys.exit()

        binary_message = self.to_binary(message)
        
        binary_index = 0
        binary_message_len = len(binary_message)

        for row in self.image:
            for pixel in row:
                b, g, r = self.to_binary(pixel)
                if binary_index < binary_message_len:
                    # pixel[0] = int()
                    pixel[0] = int(b[:-self.LSB] + binary_message[binary_index: (binary_index+self.LSB)], 2)
                    binary_index += self.LSB
                
                if binary_index < binary_message_len:
                    # pixel[1] = int()
                    pixel[1] = int(g[:-self.LSB] + binary_message[binary_index: (binary_index+self.LSB)], 2)
                    binary_index += self.LSB

                if binary_index < binary_message_len:
                    # pixel[2] = int()
                    pixel[2] = int(r[:-self.LSB] + binary_message[binary_index: (binary_index+self.LSB)], 2)
                    binary_index += self.LSB
        
                if binary_index >= binary_message_len:
                    break
        cv2.imwrite(self.stego_path, self.image)
        return self.image

    def extract(self) -> bytes:
        byte_message = []
        binary_message = ""
        binary_delimiter = self.to_binary(self.delimiter)
        # binary_check_limit = -len(binary_delimiter) * self.LSB
        # print(self.stego)
        for row in self.stego:
            for pixel in row:
                b, g, r = self.to_binary(pixel)
                binary_message += b[-self.LSB:]
                binary_message += g[-self.LSB:]
                binary_message += r[-self.LSB:]

                # print(len(binary_message))
                # print(binary_message[binary_check_limit:], end="\n\n")
                if binary_delimiter in binary_message:
                    return b"".join([int(binary_message[i: i+8], 2).to_bytes(1, 'little') for i in range(0, len(binary_message), 8)]).split(self.delimiter)[0]
        # return [chr(int(binary_message[i: i+8], 2)) for i in range(0, len(binary_message), 8)][:10]
        return b""


    def extract_v2(self):
        byte_message = []
        binary_message = ""

        for row in self.image:
            for pixel in row:
                b, g, r = self.to_binary(pixel)
                binary_message += b[-self.LSB]
                binary_message += g[-self.LSB]
                binary_message += r[-self.LSB]
                if len(binary_message) > 8:
                    temp = [binary_message[i: i+8] for i in range(0, len(binary_message), 8)]
                    if len(temp[-1]) != 8:
                        binary_message = temp.pop(-1)
                    else:
                        binary_message = ""
                    byte_message.extend(temp)
            
            if self.delimiter in binary_message[-len(self.delimiter)*self.LSB:]:
                return binary_message
            

def file_steg_test():
    stego = Steg(image="data/images/cover/file_steg_test_cover.png", stego="data/images/stego/file_steg_test_ok_4.1.png", lsb=4)
    # start

    print(stego.get_max_capacity() // 8)
    with open("data/files/test.pptx", "rb") as f:
        data_to_embed = f.read()
    stego.embed(data_to_embed)

    # end   
    extracted_d = stego.extract()
    print("done")
    print(extracted_d)
    with open("data/files/reconstructedpptx.pptx", "wb") as f:
        f.write(extracted_d)

if __name__ == "__main__":
    """
    stego = Steg(image="images/gfg.png", stego="images/stego_res.png")
    # stego.embed(b'This is secret message')

    print(stego.extract())
    """
    file_steg_test()



