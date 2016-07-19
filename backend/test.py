import binascii
print int('100001110', 2) # = 270

print bin(270)[2:], '\n' # outputs

##################
# 64 bits here
input_data = '1100110010101000100010011101101100111100101000110110000111100111'
print input_data
convert = int(input_data, 2)
convert = binascii.unhexlify('%x' % convert)
print convert
print bin(int(binascii.hexlify(convert), 16))[2:]


# print input_data
# decode = binascii.b2a_base64(input_data)
# print decode
# encode = binascii.a2b_base64(decode)
# print encode


# decode = int(input_data, 2)
# print decode
# decode = binascii.unhexlify('%x' % decode)
# print decode
# encode = binascii.hexlify(decode)
# print encode
