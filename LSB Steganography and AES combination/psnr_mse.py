
from math import log10, sqrt
import cv2
import numpy as np


def MSE(original, compressed):
    return np.mean(np.square(np.subtract(original, compressed)))

def PSNR(original, compressed):
    mse = MSE(original, compressed)
    # mse = np.mean(np.square(np.subtract(original, compressed)))
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
                  # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    # print("MSE:", mse)
    psnr = 20 * log10(max_pixel / sqrt(mse))
    # psnr = 10 * log10((max_pixel*max_pixel)/mse)
    return psnr
  
def main():
    original = "images/cover_small1.png"
    compressed = "images/output_cover_small1.png"
    #  compressed = original
    original = cv2.imread(original)
    compressed = cv2.imread(compressed, 1)
    value = PSNR(original, compressed)
    print(f"PSNR value is {value} dB")
       
if __name__ == "__main__":
    main()