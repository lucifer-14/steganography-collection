*** IMPORTANT NOTICE: Only works for PNG format ***

HOW TO USE
==========
<br>
Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret"
<br>
Extracting secret message from photo: imagesteg.py -d raw_encoded.png
<br>
<br>
Using passphrase and output file are optional.
<br>
<br>
Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret" -p "this is pass" -o outfile
<br>
Extracting secret message from photo: imageteg.py -d outfile.png -p "this is pass"
<br>
<br>
In default, data is hidden in least significant bit. This can be edited by using -b (bit index) flag. The flag values can be from 0 to 7. (0 = most significant bit, 7 = least significant bit, default = 7) If the value out of range is used or -b flag isn't used, default value will be automatically assigned. 
<br>
<br>
For example hiding in most significant bit: 
<br>
Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret" -p "this is pass" -o msbout -b 0
<br>
Extracting secret message from photo: imagesteg.py -d msbout.png -b 0
