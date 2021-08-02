*** IMPORTANT NOTICE: Only works for PNG format ***

HOW TO USE
==========
<h2>Basic Usage</h2>
Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret"
<br>
Extracting secret message from photo: imagesteg.py -d raw_encoded.png
<br>
<br>
<h2>Advanced Usage</h2>
<h4>Passphrase and Outfile</h4>
Using passphrase and output file are optional.
<br>
<br>
Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret" -p "this is pass" -o outfile
<br>
Extracting secret message from photo: imageteg.py -d outfile.png -p "this is pass"
<br>
<br>
<h4> Bit index </h4>
In default, data is hidden in least significant bit. This can be edited by using -b (bit index) flag. The flag values can be from 0 to 7. (0 = most significant bit, 7 = least significant bit, default = 7) If the value out of range is used or -b flag isn't used, default value will be automatically assigned. 
<br>
<br>
For example hiding in most significant bit: 
<br>
<br>
Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret" -p "this is pass" -o msbout -b 0
<br>
<br>
Extracting secret message from photo: imagesteg.py -d msbout.png -b 0
