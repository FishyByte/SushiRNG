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
from scipy import stats

class rng_pool():

    def create_test_list(self, num, size):
        bit_list = np.zeros(size, dtype=int)
        for i in range(len(bit_list)):
            if i % num == 0:
                bit_list[i] = 1

        return bit_list


    # Stir functions
    def stir_pool(self, entropy_one, entropy_two):

        # Create new numpy list XOR from two
        new_entropy_pool = np.logical_xor(entropy_one,entropy_two)

        return new_entropy_pool


    # Calculate the distributions of 1s and 0s in total string.
    def dist_calculations(self, bit_list):

        one_count = np.count_nonzero(bit_list)
        total_length = len(bit_list)
        zero_count = total_length - one_count

        percent_one = one_count / float(total_length)
        percent_zero = zero_count / float(total_length)


        return percent_one, percent_zero


    # Entropy calculations
    def entropy_calculations(self, percent_one, percent_zero):

        # calculating the bits of entropy
        entropy = (-percent_one*math.log(percent_one,2))+(-percent_zero*math.log(percent_zero,2))
        # entropy = stats.entropy(percent_one) + stats.entropy(percent_zero)

        return entropy


    # I need to fix this.
    # Find the corrected length of bits given entropy calculations
    def entropy_correction(self, entropy):
        corrected_bits = math.ceil(4096 * entropy)
        corrected_bits = int(corrected_bits)
        corrected_bits = 4096 + (4096-corrected_bits)
        return corrected_bits


    # Grab the needed amounts of bits to ensure 128 bits of entropy
    def alter_bit_length(self, bit_list, corrected_bits):
        # new_bit_list = np.zeros(corrected_bits)
        # for i in range(corrected_bits):
            # new_bit_list[i] = bit_list[i]
        new_bit_list = self.create_test_list(5, corrected_bits)
        return new_bit_list


    # Whitener for the 128 bit list to generate a random number
    def whiten_numbers(self, min_value,max_value, bit_list,whitener):

        # Stringify the list
        bit_string = np.array2string(bit_list)

        # Update the hash libraray
        whitener.update(bit_string)

        # Digest the library and convert into a int 32
        hash_number = whitener.hexdigest()
        hash_number = int(hash_number,32)

        # Kick out number of no more than max_value
        random_number = hash_number % max_value
        return random_number


    # Report function for all of the number's information
    def report_stats(self, bit_list, whitener):

        # Call Dist function
        percent_one, percent_zero = self.dist_calculations(bit_list)

        # Call Entropy
        entropy = self.entropy_calculations(percent_one, percent_zero)

        # Correct bits
        correct_bits = self.entropy_correction(entropy)

        new_bit_list = self.alter_bit_length(bit_list,correct_bits)

        random_number = self.whiten_numbers(0,20, new_bit_list,whitener)

        # print(len(new_bit_list))
        # print "Percent of 1s:", percent_one
        # print "Percent of 0s:", percent_zero
        # print "Bits of Entropy:", entropy
        print "Random number is:", random_number

        return random_number


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

        return response


# Main function for testing
def main():

    new_pool = rng_pool()
    whitener = hashlib.sha1()
    # Make the testing list
    bit_list = new_pool.create_test_list(3, 4096)
    second_bit_list = new_pool.create_test_list(10, 4096)

    # Report information
    # report_stats(bit_list,whitener)

    new_entropy_pool = new_pool.stir_pool(bit_list,second_bit_list)

    # report_stats(new_entropy_pool,whitener)

    new_entropy_pool = new_pool.stir_pool(new_entropy_pool, bit_list)


    for i in range(5):
        input = new_pool.report_stats(new_entropy_pool, whitener)
        response = new_pool.eight_ball_response(input)
        print response

main()
