#*********************************************************************
#The MIT License (MIT)
#
#Copyright (c) 2016 Christopher Asakawa, Mathew O'Brien, Nicholas McHale, Corey Aing
#
#Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# permit persons to whom the Software is furnished to do so, subject 
# to the following conditions:
#
#The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
# OTHER DEALINGS IN THE SOFTWARE.
#*******************************************************************
import requests
import binascii
import os
# 64 bits here
input_data = '1100110010101000100010011101101100111100101000110110000111100111'
encoded = int(input_data, 2)
# encoded = binascii.unhexlify('%x' % encoded)
# print encoded
# print bin(int(binascii.hexlify(encoded), 16))[2:]


payload = {
    'pub_key': '233taewdzvx',
    'fishBits': encoded
}
print os.getcwd()
r = requests.post('http://127.0.0.1:5000/add-bytes', data=payload, files={'file': open('/home/nick/SushiRNG/backend/bits.bin','rb')})
print r.status_code
