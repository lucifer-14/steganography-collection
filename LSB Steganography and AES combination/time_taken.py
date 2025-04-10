import time
import os
import steg
message_size_list = [50, 128, 512, 1024, 4096, 8192, 16384, 32768, 65536, 98304]
messages = []
eval_vals = []
for i in message_size_list:
    try:
        with open(os.path.join('text_files', f'dummy_text_{i}.txt'), 'rb') as f:
            messages.append(f.read())
    except FileNotFoundError:
        print('error')
test_steg_e = steg.Steg(stego=os.path.join("images", "standard", "pm_stego", "test_baboon.png"))
start_time = time.time()
b = test_steg_e.extract()
time_taken = time.time() - start_time
print(time_taken)
input()