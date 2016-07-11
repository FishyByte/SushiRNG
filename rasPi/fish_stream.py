#!/usr/bin/python
# generates bits from fish movements
# - Chris Asakawa
from bitstream import BitStream
from numpy import *
import time


class FishStream:
    # init a BitStream to hold the bit values
    def __init__(self):
        self.stream = BitStream()
        self.fish_positions = []
        self.zero_count = 0
        self.one_count = 0

    # helper function, add one to the stream and one count
    def add_zero(self):
        self.stream.write(False)
        self.zero_count += 1

    # helper function, add zero to the stream and the zero count
    def add_one(self):
        self.stream.write(True)
        self.one_count += 1

    def add_position(self, fish_id, x, y):

        # if the current index it empty this will throw
        # an indexException, and in which case, init the
        # current fish position at that index.
        try:
            # grab the past position of the current fish
            x_previous = self.fish_positions[fish_id][0]
            y_previous = self.fish_positions[fish_id][1]

            # current fish moved to the right
            if x_previous > x:
                self.add_one()
            # current fish moved to the left
            else:
                self.add_zero()
            # current fish moved up the screen
            if y_previous > y:
                self.add_one()
            # current fish moved down the screen
            else:
                self.add_zero()

            # MOAR bits
            if y_previous > x:
                self.add_one()
            else:
                self.add_zero()
            if x_previous > y:
                self.add_one()
            else:
                self.add_zero()

            # overwrite previous positions with current
            self.fish_positions[fish_id] = [x, y]
        except IndexError:
            # new fish found, append is to the list
            self.fish_positions.append([x, y])

    def print_stream(self):
        print self.stream

    # returns two values, probability of zero and one
    def get_probabilities(self):
        # calculate total (we use it twice)
        total = self.zero_count + self.one_count
        # returns the probability of a zero and a one
        return float(self.zero_count) / total, \
            float(self.one_count) / total

    def get_bits(self, length):
        while self.stream.__len__() < length:
            time.sleep(0.1)
        return_bits = self.stream.read(length)
        self.zero_count -= str(return_bits).count('0')
        self.one_count -= str(return_bits).count('1')
        return return_bits

    def get_length(self):
        return len(str(self.stream))
