import hashlib
from fish_stream import *


class FishPool:
    # constructor
    def __init__(self):
        self.entropy = 0

    # Entropy calculations
    def entropy_calculations(self, percent_one, percent_zero):
        # calculating the bits of entropy
        entropy = (-percent_one * math.log(percent_one, 2)) + \
                  (-percent_zero * math.log(percent_zero, 2))
        return entropy

    # Find the corrected length of bits given entropy calculations
    def entropy_correction(self, entropy):
        corrected_bits = math.ceil(128 * entropy)
        corrected_bits = 128 + (128 - corrected_bits)
        return int(corrected_bits)

    # Whitener for the 128 bit list to generate a random number
    def whiten_numbers(self, max_value, bit_list):
        # Use SHA1 to hash the string.
        bit_string = int("".join(str(x) for x in bit_list))
        bit_string = str(bit_string)
        hash_number = hashlib.sha1(bit_string.encode('utf-8')).hexdigest()
        hash_number = int(hash_number, 32)
        random_number = hash_number % max_value
        return random_number

    # TODO: make this work
    # i cant call fish_stream in this file because it init an empty stream.
    # this function needs to be moved to the root file of the project (color_tracking.py)
    # def get_random(self, min, max):
        # percent_one, percent_two = fish_stream.get_probabilities()
        # entropy = self.entropy_calculations(percent_one, percent_two)
        # bits_needed = self.entropy_correction(entropy)
        # bit_list = str(fish_stream.get_bits(bits_needed))
        # return self.whiten_numbers(min, max, bit_list)
