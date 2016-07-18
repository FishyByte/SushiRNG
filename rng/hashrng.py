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


def create_test_list(num, size):
    bit_list = np.zeros(size, dtype=int)
    for i in range(len(bit_list)):
        if i % num == 0:
            bit_list[i] = 1

    return bit_list


# Stir functions
def stir_pool(entropy_one, entropy_two):

    # Create new numpy list XOR from two
    new_entropy_pool = np.logical_xor(entropy_one,entropy_two)

    return new_entropy_pool


# Calculate the distributions of 1s and 0s in total string.
def dist_calculations(bit_list):

    one_count = np.count_nonzero(bit_list)
    total_length = len(bit_list)
    zero_count = total_length - one_count

    percent_one = one_count / float(total_length)
    percent_zero = zero_count / float(total_length)


    return percent_one, percent_zero


# Entropy calculations
def entropy_calculations(percent_one, percent_zero):

    # calculating the bits of entropy
    entropy = (-percent_one*math.log(percent_one,2))+(-percent_zero*math.log(percent_zero,2))
    # entropy = stats.entropy(percent_one) + stats.entropy(percent_zero)

    return entropy


# I need to fix this.
# Find the corrected length of bits given entropy calculations
def entropy_correction(entropy):
    corrected_bits = math.ceil(4096 * entropy)
    corrected_bits = int(corrected_bits)
    corrected_bits = 4096 + (4096-corrected_bits)
    return corrected_bits


# Grab the needed amounts of bits to ensure 128 bits of entropy
def alter_bit_length(bit_list, corrected_bits):
    # new_bit_list = np.zeros(corrected_bits)
    # for i in range(corrected_bits):
        # new_bit_list[i] = bit_list[i]
    new_bit_list = create_test_list(5, corrected_bits)
    return new_bit_list


# Whitener for the 128 bit list to generate a random number
def whiten_numbers(min_value,max_value, bit_list,whitener):

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
def report_stats(bit_list, whitener):

    # Call Dist function
    percent_one, percent_zero = dist_calculations(bit_list)

    # Call Entropy
    entropy = entropy_calculations(percent_one, percent_zero)

    # Correct bits
    correct_bits = entropy_correction(entropy)

    new_bit_list = alter_bit_length(bit_list,correct_bits)

    random_number = whiten_numbers(0,100, new_bit_list,whitener)

    print(len(new_bit_list))
    print "Percent of 1s:", percent_one
    print "Percent of 0s:", percent_zero
    print "Bits of Entropy:", entropy
    print "Random number is:", random_number


# Main function for testing
def main():

    whitener = hashlib.sha1()
    # Make the testing list
    bit_list = create_test_list(3, 4096)
    second_bit_list = create_test_list(10, 4096)

    # Report information
    report_stats(bit_list,whitener)

    new_entropy_pool = stir_pool(bit_list,second_bit_list)

    report_stats(new_entropy_pool,whitener)

    new_entropy_pool = stir_pool(new_entropy_pool, bit_list)

    report_stats(new_entropy_pool,whitener)
    report_stats(new_entropy_pool,whitener)

main()
