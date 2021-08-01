*** IMPORTANT NOTICE: Only works for PNG format ***

HOW TO USE
==========

Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret"

Extracting secret message from photo: imagesteg.py -d raw_encoded.png


Using passphrase and output file are optional.

Hiding secret message in photo: imagesteg.py -e raw.png -t "this is secret" -p "this is pass" -o outfile

Extracting secret message from photo: imageteg.py -d outfile.png -p "this is pass"
