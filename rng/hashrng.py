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


import hashlib
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

fake_size = 20000
fake_mod = 3


# Creates a fake RNG set for testing and returns as a list of ints
def create_test_list(fake_mod, fake_size):

    # Make an numpy array of zeros to replace
    bit_np = np.zeros(fake_size, dtype=int)

    # Replace the array with "fake" values of 1s and 0s
    for i in range(len(bit_np)):
        if i % fake_mod == 0:
            bit_np[i] = 1

    # Make it into a list. Assumed LIST type was needed for implementation
    bit_list = bit_np.tolist()

    return bit_list


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
        self.correct_bits = 4096
        self.percent_ones = 0
        self.percent_zeros = 0
        self.entropy = 0

    # Report information on pool
    def report_pool_info(self):
        print "Corrected bits: ", self.correct_bits
        print "Entropy: ", self.entropy
        print "Percent of zeros: ", self.percent_zero
        print "Percent of ones: ", self.percent_one

    # Adding new data into the pool.
    def update_data(self,bit_list):

        # Remake data equal to the size of input
        self.data = np.zeros(len(bit_list), dtype=int)

        # Override the original data with new input
        for i in range(len(bit_list)):
            self.data[i] = bit_list[i]


        self.dist_calculations()
        self.entropy_calculations()
        self.entropy_correction()

    # Stir the pool
    def stir_split_pool(self):

        # Split the pool in half and XOR
        new_pool = np.split(self.random_pool, 2)
        new_pool = np.logical_xor(new_pool[0],new_pool[1])
        new_pool = new_pool.tolist()

        # Set the pool equal to the XOR functioned pool.
        self.random_pool = new_pool

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
        entropy = (-self.percent_one*math.log(self.percent_one,2))+(-self.percent_zero*math.log(self.percent_zero,2))
        self.entropy = entropy

    # Find the corrected length of bits given entropy calculations
    def entropy_correction(self):
        corrected_bits = math.ceil(4096 * self.entropy)
        corrected_bits = int(corrected_bits)
        corrected_bits = 4096 + (4096-corrected_bits)
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
                temp_number = str(bin(int(temp_number,32))[2:].zfill(0))

                # Append each binary digit into the pool. Probably need to rework this
                for j in range(len(temp_number)):
                    self.random_pool.append(temp_number[j])

                # new beginning position of the sub list
                start = i

    # Report function for all of the number's information. Stale function
    # def report_stats(self, bit_list, whitener):

        # Call Dist function
        # percent_one, percent_zero = self.dist_calculations(bit_list)

        # Call Entropy
        # self.entropy_calculations(percent_one, percent_zero)

        # Correct bits
        # self.entropy_correction(entropy)

        # self.alter_bit_length(bit_list,correct_bits)

        # random_number = self.whiten_numbers(new_bit_list)

        # print(len(new_bit_list))
        # print "Percent of 1s:", percent_one
        # print "Percent of 0s:", percent_zero
        # print "Bits of Entropy:", entropy
        # print "Random number is:", random_number

        # return random_number

    # 8-Ball Responses
    def eight_ball_response(self, number):

        if number == 0:
            response = "It is Certain"
        elif number == 1:
            response = "It is decidedly so"
        elif number == 2:
            response = "Without a doubt"
        elif number == 3:
            response = "Yes, definitely"
        elif number == 4:
            response = "You may rely on it"
        elif number == 5:
            response = "As I see it, yes"
        elif number == 6:
            response = "Most likely"
        elif number == 7:
            response = "Outlook good"
        elif number == 8:
            response = "Yes"
        elif number == 9:
            response = "Signs point to yes"
        elif number == 10:
            response = "Reply hazy, try again"
        elif number == 11:
            response = "Ask again later"
        elif number == 12:
            response = "Better not tell you now"
        elif number == 13:
            response = "Cannot predict now"
        elif number == 14:
            response = "Concentrate and ask again"
        elif number == 15:
            response = "Don't count on it"
        elif number == 16:
            response = "My reply is no"
        elif number == 17:
            response = "My sources say no"
        elif number == 18:
            response = "Outlook not so good"
        elif number == 19:
            response = "Very doubtful"
        else:
            response = "Lol no"

        # Need to add more possible responses

        return response

    # Turn a file into a numpy array
    def read_from_file(self,text):

        with open(text, 'r') as myfile:
            data = myfile.read().replace('\n', '')
        test_array = np.array(list(data), dtype=int)
        return test_array

    # Turn a numpy array into a file
    def write_to_file(self, f_name):
        with open(f_name, 'w') as f:
            for value in self.random_pool:
                f.write(value)

    # Returns a random dice roll of X size Y times.
    def dice_roll_return(self, dice_size, num_dice):

        # Find out the binary size of the dice size
        bin_length = len(bin(dice_size)[2:].zfill(0))
        response = []

        # Make the response list, and remove from pool.
        for i in range(num_dice):
            temp_string = []
            for j in range(bin_length):
                temp_string.append(self.random_pool.pop())
            temp_number = int(''.join(str(x) for x in temp_string), 2)
            response.append(temp_number)

        # Printing responses for testing purposes
        print response

        return response

    # Returns a response string one time
    def eight_ball_return(self):

        # Temp String
        temp_string = []

        # Make the string
        for i in range(5):
            temp_string.append(self.random_pool.pop())

        # Convert into an Int
        temp_number = int(''.join(str(x) for x in temp_string), 2)

        # Get the response from the 8-ball
        response = self.eight_ball_response(temp_number)
        print response

        return response

    # Returns heads or tails
    def coin_flip_return(self):

        next_data = int(self.random_pool.pop())

        if next_data == 0:
            response = "heads"
        else:
            response = "tails"

        print response

        return response


# Main function for testing
def main():

    # Make a pool.
    new_pool = RngPool()

    # Make a "fake" list of values
    bit_list = create_test_list(fake_mod, fake_size)

    # Update the pool with the new data
    new_pool.update_data(bit_list)

    # Report the current stats of the pool.
    new_pool.report_pool_info()

    # Whiten the current data set
    new_pool.whiten_numbers(bit_list)

    # Print the length of the pool.
    print "Current length of the pool", len(new_pool.random_pool)
    new_pool.dice_roll_return(5, 15)
    new_pool.eight_ball_return()
    new_pool.coin_flip_return()

    for i in range(10):
        new_pool.coin_flip_return()

    # Ending length to be sure we are using and removing random binary numbers.
    print "Current length of the pool: ", len(new_pool.random_pool)

    # Write the pool to a file for NIST testing.
    new_pool.write_to_file("test_numbers")

    # Make the testing list
    # bit_list = new_pool.create_test_list(5, 4096)
    # second_bit_list = new_pool.create_test_list(10, 4096)

    # new_pool.write_to_file(new_pool.data,'test_numbers')

    # file_input = new_pool.read_from_file("test_numbers")
    # print "Testing area:"
    # print file_input
    # new_pool.report_stats(file_input, new_pool.whitener)

    # Needs work.

    # Report information
    # report_stats(bit_list,whitener)

    # new_entropy_pool = new_pool.stir_pool(bit_list,second_bit_list)

    # report_stats(new_entropy_pool,whitener)

    # new_entropy_pool = new_pool.stir_pool(new_entropy_pool, bit_list)

    # stirred_pool = new_pool.stir_split_pool(new_entropy_pool)

    # number_input = new_pool.report_stats(stirred_pool, whitener)
    # reps = new_pool.eight_ball_response(number_input)
    # print reps

    # for i in range(3):
        # input = new_pool.report_stats(new_entropy_pool, whitener)
        # response = new_pool.eight_ball_response(input)
        # print response

main()
