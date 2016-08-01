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

# hashrng.py
# created: 6/28/2016
# Contributors: Matthew O'Brien
# Initial MD5 Hashfunction ideas for RNG
# -------------------------------------------------------------------------
# Initial file for use of the MD5 hash function to generate a random number
# from a given input.
# Currently reading in a nonsense string to output a hex number. Which is
# converted into a decimal number.

import numpy as np
import math
import hashlib


class RngPool:

    # Data class for pool data.
    def __init__(self):

        # Data is the fish generated 1s and 0s. Will be destroyed after each whitening
        self.data = np.zeros(1, dtype=int)

        # The Hash library
        self.whitener = hashlib.sha1()

        # The pool of random binary values as a list.
        self.random_pool = []

        # The current "datas" value for entropy bits, %s, and entropy.
        self.correct_bits = 256
        self.percent_ones = 0
        self.percent_zeros = 0
        self.entropy = 0

    # Adding new data into the pool.
    def update_data(self, bit_list):
        # Remake data equal to the size of input
        self.data = np.zeros(len(bit_list), dtype=int)

        # Override the original data with new input
        for i in range(len(bit_list)):
            self.data[i] = bit_list[i]

        self.dist_calculations()
        self.entropy_calculations()
        self.entropy_correction()

    # Calculate the distributions of 1s and 0s in total string.
    def dist_calculations(self):

        one_count = np.count_nonzero(self.data)
        total_length = len(self.data)
        zero_count = total_length - one_count

        self.percent_one = one_count / float(total_length)

        self.percent_zero = zero_count / float(total_length)

    # Entropy calculations
    def entropy_calculations(self):

        # calculating the bits of entropy
        entropy = (-self.percent_one * math.log(self.percent_one, 2)) + (-self.percent_zero * math.log(self.percent_zero, 2))
        self.entropy = entropy

    # Find the corrected length of bits given entropy calculations
    def entropy_correction(self):
        corrected_bits = math.ceil(256 * self.entropy)
        corrected_bits = int(corrected_bits)
        corrected_bits = 256 + (256 - corrected_bits)
        self.correct_bits = corrected_bits

    # Whitener for the Fish numbers to 160 bits
    def whiten_numbers(self, bit_list):

        # Starting position of the sub array to string
        start = 0

        # Iterate through list of fish numbers
        for i in range(len(bit_list)):

            # Whiten every corrected bits
            if i % self.correct_bits == 0 and i != 0:

                # Strings the bit_list from the np array
                temp_string = bit_list[start:i]
                temp_string = ''.join(str(temp_string) for x in temp_string)

                # Update the string into the hash
                self.whitener.update(temp_string)

                # Digest the hash, convert into a binary and append to the random_pool
                temp_number = self.whitener.hexdigest()
                temp_number = str(bin(int(temp_number, 16))[2:].zfill(0))

                # Append each binary digit into the pool. Probably need to rework this
                for j in range(len(temp_number)):
                    self.random_pool.append(temp_number[j])

                    # new beginning position of the sub list
                    start = i

    # Return random pool
    def return_pool_data(self):
        return self.random_pool


