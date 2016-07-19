import requests
import binascii

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
r = requests.post('http://127.0.0.1:5000/add-bits', data=payload)
print r.status_code