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
