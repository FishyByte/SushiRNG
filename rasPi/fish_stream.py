#!/usr/bin/python
# generates bits from fish movements
# - Chris Asakawa
from bitstream import BitStream
from numpy import *


class FishStream:
    # init a BitStream to hold the bit values
    def __init__(self):
        self.stream = BitStream()
        self.fish_positions = []
        self.zero_count = 0
        self.one_count = 0

    def add_position(self, fish_id, x, y):
        # if the current index it empty this will throw
        # an indexException, and in which case, init the
        # current fish position at that index.
        try:
            # current fish moved to the right
            if self.fish_positions[fish_id][0] > x:
                self.stream.write(True)
                self.one_count += 1
            # current fish moved to the left
            else:
                self.stream.write(False)
                self.zero_count += 1

            # current fish moved up the screen
            if self.fish_positions[fish_id][1] > y:
                self.stream.write(True)
                self.one_count += 1
            # current fish moved down the screen
            else:
                self.stream.write(False)
                self.zero_count += 1

            # if y_old > x_current
            if self.fish_positions[fish_id][1] > x:
                self.stream.write(True)
                self.one_count += 1
            else:
                self.stream.write(False)
                self.zero_count += 1

            # if x_old > y_current
            if self.fish_positions[fish_id][0] > y:
                self.stream.write(True)
                self.one_count += 1
            else:
                self.stream.write(False)
                self.zero_count += 1

            # overwrite previous positions with current
            self.fish_positions[fish_id] = [x, y]
        except IndexError:
            # new fish found, append is to the list
            self.fish_positions.append([x, y])

    def print_stream(self):
        print self.stream

    def get_probability(self):
        # calculate total (we use it twice)
        total = self.zero_count + self.one_count
        # returns the probability of a zero and a one
        return float(self.zero_count) / total, \
            float(self.one_count) / total

    def get_bits(self, length):
        return_bits = self.stream.read(length)
        self.zero_count -= str(return_bits).count('0')
        self.one_count -= str(return_bits).count('1')
        return return_bits

    def get_length(self):
        return len(str(self.stream))
