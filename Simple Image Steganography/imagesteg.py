import cv2
import numpy as np
import os
import argparse
import sys

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def to_binv2(data, passphrase):
    if isinstance(data, str):
        # change data to ascii
        to_ascii = [int(ord(c)) for c in data]
        # check if passphrase is used
        if passphrase:
            # change each letter of passphrase to ascii
            passphrase = [int(ord(c)) for c in passphrase]
            passphrase.reverse()
            counter = 0
            passphrase_len = len(passphrase)
            # encode each letter of data using passphrase
            for i in range(len(to_ascii)):
                to_ascii[i] += passphrase[counter]
                counter += 1
                if counter == passphrase_len:
                    counter = 0
                    passphrase.reverse()

        return ''.join(format(i, "08b") for i in to_ascii)


def encode(image_name, secret_data, passphrase, bit_index):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "==***=="
    data_index = 0
    # convert data to binary version 2 (check passphrase)
    binary_secret_data = to_binv2(secret_data, passphrase)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify pixel RGB bits only if there is still data to store
            if data_index < data_len:
                # editing red pixel bit
                pixel[0] = int(r[:bit_index] + binary_secret_data[data_index] + r[bit_index+1:], 2)
                data_index += 1
            if data_index < data_len:
                # editing green pixel bit
                pixel[1] = int(g[:bit_index] + binary_secret_data[data_index] + g[bit_index+1:], 2)
                data_index += 1
            if data_index < data_len:
                # editing blue pixel bit
                pixel[2] = int(b[:bit_index] + binary_secret_data[data_index] + b[bit_index+1:], 2)
                data_index += 1
            # if data is encoded, break out of the loop
            if data_index >= data_len:
                break
    return image


def decode(image_name, passphrase, bit_index):
    print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[bit_index]
            binary_data += g[bit_index]
            binary_data += b[bit_index]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    counter = 0
    # change each letter of passphrase to ascii
    passphrase = [int(ord(c)) for c in passphrase]
    passphrase.reverse()
    decoded_data = ""
    # convert from bits to characters
    for byte in all_bytes:
        # check if passphrase is used
        if passphrase :        
            passphrase_len = len(passphrase)
            # decode each letter of data using passphrase
            try :
                decoded_data += chr(int(byte, 2)-passphrase[counter])
            except :
                print('[-] Failed to decode the image.')
                sys.exit()
            counter += 1
            if counter == passphrase_len:
                counter = 0
                passphrase.reverse()
        else :
            decoded_data += chr(int(byte, 2))
        if decoded_data[-7:] == "==***==":
            break
    return decoded_data[:-7]


if __name__ == "__main__":

    bit_index = 7           # 0 - 7, 0 = most significant bit, 7 = least significant bit, default = 7 
    passphrase="default"    # default value of passphrase = default (It's so safe right, LOL)

    parser = argparse.ArgumentParser(description="Steganography Image encoder/decoder, this Python scripts encode data within images. Encoding using passphrase is optional.")
    parser.add_argument("-t", "--text", help="The text data to encode into the image (ONLY for encoding)")
    parser.add_argument("-p", "--passphrase",  help="The passphrase for additional security (optional)")
    parser.add_argument("-e", "--encode", help="The image file to be encoded")
    parser.add_argument("-o", "--outfile", help="The output file name (ONLY for encoding, optional)")
    parser.add_argument("-d", "--decode", help="The image file to be decoded")
    parser.add_argument("-b", "--bit_index", help="The bit index of pixel to encode or decode (0-7: 0 = most significant bit, 7 = least significant bit, default = 7")
    
    
    args = parser.parse_args()
    secret_data = args.text
    
    if args.passphrase:
        passphrase=args.passphrase
    if args.bit_index:
        bit_index=args.bit_index

    bit_index=int(bit_index)
    # change to default bit index if it is invalid bit index
    if not (0<=bit_index<=7) :
        bit_index = 7       

    if args.encode:
        # if the encode argument is specified
        input_image = args.encode
        print("[+] Input image:", input_image)
        # split the absolute path and the file
        path, file = os.path.split(input_image)
        # split the filename and the image extension
        filename, ext = file.split(".")
        # default outfile name
        outfile=f"{filename}_encoded.{ext}"
        # custom outfile name
        if args.outfile:
            outfile=f"{args.outfile}.{ext}"
        output_image = os.path.join(path, outfile)
        # encode the data into the image
        encoded_image = encode(image_name=input_image, secret_data=secret_data, passphrase=passphrase, bit_index=bit_index)
        # save the output image (encoded image)
        cv2.imwrite(output_image, encoded_image)
        print("[+] Saved encoded image.")
        print("[+] Output image:", output_image)
    if args.decode:
        input_image = args.decode
        # decode the secret data from the image
        decoded_data = decode(image_name=input_image, passphrase=passphrase, bit_index=bit_index)
        print("[+] Decoded data:", decoded_data)
