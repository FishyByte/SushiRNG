import hashlib
import math

# there will be 2^13 or 8192 fed into this class (input_bits)
class FishPool:

    # constructor
    def __init__(self):
        # The Hash library
        self.whitener = hashlib.sha1()      # init hash lib
        self.raw_data = ''                  # raw binary from the fish tank
        self.percent_ones = 0               # percent of ones and zeros
        self.percent_zeros = 0
        self.entropy = 0                    # calculated entropy
        self.correct_bits = 0               # corrected bit count
        self.total_count = 0                # total bit count
        self.return_string = ''             # string to be returned
        self.finish_processing = False      # boolean for knowing when done
        pass

    # uses all the methods in this class to generate a randomized string of 1's and 0's
    # input_bits parameter here, is a string
    def process_bits(self, input_bits):

        # there may be some left over bits here, lets append to that
        self.raw_data += input_bits

        # reset all class variables (except hashlib and raw_data)
        self.reset_class_variables()

        # loop until all the bits have been processed
        while True:
            self.dist_calculations()        # sets percentages of zeros and ones
            self.entropy_calculations()     # sets the calculated entropy
            self.entropy_correction()       # sets the corrected bits length
            self.whiten_numbers()           # grabs the corrected bit list and whitens it

            # the whiten_number function will set this flag when done
            if self.finish_processing:
                return self.return_string

    # Calculate the distributions of 1s and 0s in total string.
    def dist_calculations(self):

        # get counts of ones zeros and total
        zero_count = self.raw_data.count('0')
        one_count = self.raw_data.count('1')
        self.total_count = zero_count + one_count

        # lets avoid that dividing by zero
        if self.total_count == 0:
            self.finish_processing = True
            return

        # now lets get the probabilities of each
        self.percent_zeros = zero_count / float(self.total_count)
        self.percent_ones = one_count / float(self.total_count)

    # Entropy calculations
    def entropy_calculations(self):
        # we done?
        if self.finish_processing:
            return
        # calculate entropy
        self.entropy = (-self.percent_ones * math.log(self.percent_ones, 2)) + \
                       (-self.percent_zeros * math.log(self.percent_zeros, 2))

    # Find the corrected length of bits given entropy calculations
    def entropy_correction(self):
        # we done?
        if self.finish_processing:
            return

        corrected_bits = math.ceil(256 * self.entropy)
        corrected_bits = int(corrected_bits)
        corrected_bits = 256 + (256 - corrected_bits)
        self.correct_bits = corrected_bits

    # Whitener for the Fish numbers to 160 bits
    def whiten_numbers(self):
        # we done?
        if self.finish_processing:
            return

        # lets ensure we have enough bits left before continugsing
        if self.total_count < self.correct_bits:
            self.finish_processing = True
            return

        # simulate a pop operation, grab and delete
        process_chunk = self.raw_data[:self.correct_bits]
        self.raw_data = self.raw_data[self.correct_bits:]

        # Update the string into the hash
        self.whitener.update(process_chunk)

        # Digest the hash, convert into a binary and append to the random_pool
        hash_number = self.whitener.hexdigest()
        hash_number = str(bin(int(hash_number, 16))[2:].zfill(0))
        self.return_string += str(hash_number)

    # this function is used to re-init class variables
    def reset_class_variables(self):
        self.percent_ones = 0               # percent of ones and zeros
        self.percent_zeros = 0
        self.entropy = 0                    # calculated entropy
        self.correct_bits = 0               # corrected bit count
        self.total_count = 0                # total bit count
        self.return_string = ''             # string to be returned
        self.finish_processing = False      # boolean for knowing when done

    def stream_analysis(self, stream):
        # get counts of ones zeros and total
        zero_count = stream.count('0')
        one_count = stream.count('1')
        total_count = zero_count + one_count

        # lets avoid that divide by zero
        if total_count == 0:
            return 'empty stream :('

        # now lets get the probabilities of each
        percent_zeros = zero_count / float(total_count)
        percent_ones = one_count / float(total_count)

        entropy = (-percent_ones * math.log(percent_ones, 2)) + \
                  (-percent_zeros * math.log(percent_zeros, 2))

        # now return a string with the calculated analysis
        return '_________BitStream Analysis_________', '\n', \
               'total bits in stream:', total_count, '\n', \
               'percentage of zeros:', percent_zeros, '\n', \
               'percentage of ones:', percent_ones, '\n', \
               'entropy calculation:', entropy
