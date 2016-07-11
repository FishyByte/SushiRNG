# hashrng.py
# created: 6/28/2016
# Contributors: Matthew O'Brien
# Initial MD5 Hashfunction ideas for RNG
# -------------------------------------------------------------------------
# Initial file for use of the MD5 hash function to generate a random number
# from a given input.
# Currently reading in a nonsense string to output a hex number. Which is
# converted into a decimal number.


import hashlib
from bitstream import BitStream
from numpy import *
import matplotlib.pyplot as plt
# import scipy import stats



def hashrng():
    n = hashlib.sha1("w".encode('utf-8')).hexdigest()
    m = hashlib.sha1("whateve your string is".encode('utf-8')).hexdigest()
    i = int(m,16)
    j = int(n,32)
    stream = BitStream()
    stream.write("asdqwevjvwevwefovvwl", str)
    total = len(stream)
    one_count = stream.count('1')
    zero_count = stream.count('0')
    one_count /= total
    zero_count /= total
    print(one_count)
    print(zero_count)
    print(stream)
    print(i)
    print(j)

    
hashrng()
