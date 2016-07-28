import hashlib
import math
import numpy as np

class FishPool:
    def __init__(self, input_bits):
        # The Hash library
        self.whitener = hashlib.sha1()
        # Data is the fish generated 1s and 0s. Will be destroyed after each whitening
        self.data = np.zeros(1, dtype=int)
        # init data values for entropy bits, %s, and entropy.
        self.percent_ones = 0
        self.percent_zeros = 0
        self.entropy = 0
        self.correct_bits = 0
        self.return_string = ''
        pass

    # uses all the methods in this class to generate a randomized stream of 1's and 0's
    def create_random_list(self):
        self.dist_calculations()        # sets percentages of zeros and ones
        self.entropy_calculations()     # sets calculates the entropy
        self.entropy_correction()       # sets the corrected bits length
        self.whiten_numbers()

    # Calculate the distributions of 1s and 0s in total string.
    def dist_calculations(self):

        one_count = np.count_nonzero(self.data)
        total_length = len(self.data)
        zero_count = total_length - one_count

        self.percent_ones = one_count / float(total_length)
        self.percent_zeros = zero_count / float(total_length)

    # Entropy calculations
    def entropy_calculations(self):
        self.entropy = (-self.percent_ones * math.log(self.percent_ones, 2)) + \
                       (-self.percent_zeros * math.log(self.percent_zeros, 2))

    # Find the corrected length of bits given entropy calculations
    def entropy_correction(self):
        corrected_bits = math.ceil(256 * self.entropy)
        corrected_bits = int(corrected_bits)
        corrected_bits = 256 + (256 - corrected_bits)
        self.correct_bits = corrected_bits

    # Whitener for the Fish numbers to 160 bits
    def whiten_numbers(self):

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
                temp_number = str(bin(int(temp_number,16))[2:].zfill(0))

                # Append each binary digit into the pool. Probably need to rework this
                for j in range(len(temp_number)):
                    self.return_string += str(temp_number[j])

                # new beginning position of the sub list
                start = i