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


def hashrng():
    n = hashlib.md5("w".encode('utf-8')).hexdigest()
    m = hashlib.md5("whateve your string is".encode('utf-8')).hexdigest()
    i = int(m,16)
    j = int(n,32)
    print(i)
    print(j)

    
hashrng()