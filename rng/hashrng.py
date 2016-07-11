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
import matplotlib.pyplot as plt
import numpy as np


def create_test_list():
    bit_list = []
    for i in range(1028):
        if i % 3 == 0:
            bit_list.append(1)
        else:
            bit_list.append(0)

    return bit_list


# Calculate the distributions of 1s and 0s in total string.
def dist_calculations(bit_list):

    # For testing of the distribution. Comment out later
    bit_string = int("".join(str(x) for x in bit_list))
    bit_string = str(bit_string)
    one_count = bit_string.count('1')
    zero_count = bit_string.count('0')
    total_length = len(bit_string)

    percent_one = one_count / total_length
    percent_zero = zero_count / total_length

    return percent_one, percent_zero


# Entropy calculations
def entropy_calculations(percent_one, percent_zero):

    # calculating the bits of entropy
    entropy = (-percent_one*math.log(percent_one,2))+(-percent_zero*math.log(percent_zero,2))
    return entropy


# Find the corrected length of bits given entropy calculations
def entropy_correction(entropy):
    corrected_bits = math.ceil(128 * entropy)
    corrected_bits = 128 + (128-corrected_bits)
    return corrected_bits


# Grab the needed amounts of bits to ensure 128 bits of entropy
def alter_bit_length(bit_list, corrected_bits):
    new_bit_list = []
    for i in range(corrected_bits):
        new_bit_list.append(bit_list.pop())
    return new_bit_list


# Whitener for the 128 bit list to generate a random number
def whiten_numbers(min_value,max_value, bit_list):

    # Use SHA1 to hash the string.
    bit_string = int("".join(str(x) for x in bit_list))
    bit_string = str(bit_string)
    hash_number = hashlib.sha1(bit_string.encode('utf-8')).hexdigest()
    hash_number = int(hash_number,32)
    random_number = hash_number%max_value
    return random_number

# Main function for testing
def main():
    # Make the testing list
    bit_list = create_test_list()

    # Calculate the percents of 1s and 0s of test list
    percent_one, percent_zero = dist_calculations(bit_list)

    # Calculate Entropy
    entropy = entropy_calculations(percent_one,percent_zero)

    # Find the corrected bits we need for 128 bits of entropy.
    corrected_bits = entropy_correction(entropy)
    new_bit_list = alter_bit_length(bit_list,corrected_bits)

    # Whiten the number and set parameters for the number.
    random_number = whiten_numbers(0,100,new_bit_list)

    # Reporting all the information
    print(len(new_bit_list))
    print("Percent of 1s",percent_one)
    print("Percent of 0s", percent_zero)
    print("Bits of Entropy", entropy)
    print("Random number is: ", random_number)

main()
