#!/usr/bin/python
# generates bits from fish movements
# - Chris Asakawa

# Copyright (c) 2016 Christopher Asakawa, Nicholas McHale, Matthew O'Brien, Corey Aing
# This code is available under the "MIT License".
# Please see the file COPYING in this distribution
# for license terms.

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
        # if velocity and acceleration is greater than these values
        # then flip the bit value.
        velocity_threshold = 5
        acceleration_threshold = 5

        # if the current index it empty this will throw
        # an indexException, and in which case, init the
        # current fish position at that index.
        try:
            # grab the past position of the current fish    # - PREVIOUS -
            x_previous = self.fish_positions[fish_id][0]    # position of x
            y_previous = self.fish_positions[fish_id][1]    # position of y
            vx_previous = self.fish_positions[fish_id][2]   # velocity of x
            vy_previous = self.fish_positions[fish_id][3]   # velocity of y
            ax = ay = 0

            # determine the current velocity
            if x_previous > x:
                vx = (x_previous - x)
            else:
                vx = (x - x_previous)

            if y_previous > y:
                vy = (y_previous - y)
            else:
                vy = (y - y_previous)

            # determine the current acceleration
            if vx_previous > vx:
                ax = vx_previous - vx
            else:
                ax = vx - vx_previous
            if vy_previous > vy:
                ay = vy_previous - vy
            else:
                ay = vy - vy_previous



            # current fish moved to the right
            if x_previous > x:
                if vx < velocity_threshold:
                    if ax < acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()
                else:
                    if ax < acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()

            # current fish moved to the left
            elif x_previous < x:
                if vx < velocity_threshold:
                    if ax > acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()
                else:
                    if ax > acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()

            # current fish moved up the screen
            if y_previous < y:
                if vy < velocity_threshold:
                    if ay < acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()
                else:
                    if ay < acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()

            # current fish moved down the screen
            elif y_previous > y:
                if vy < velocity_threshold:
                    if ay > acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()
                else:
                    if ay > acceleration_threshold:
                        self.add_one()
                    else:
                        self.add_zero()

            # overwrite previous positions with current
            self.fish_positions[fish_id] = [x, y, vx, vy]

        except IndexError:
            # new fish found, append is to the list
            self.fish_positions.append([x, y, 0, 0])

    def print_stream(self):
        print self.stream

    # returns two values, probability of zero and one
    def get_probabilities(self):
        # calculate total (we use it twice)
        total = self.zero_count + self.one_count
        if total == 0:
            return 0, 0
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
