#!/usr/bin/python
# generates bits from fish movements
# - Chris Asakawa
from bitstream import BitStream
from numpy import *

# list to hold x position and y positions of each fish
fish_list = []
stream = BitStream()


class Fish:
    # object params for individual fish
    def __init__(self, fish_id, x, y):
        self.fish_id = fish_id
        self.x = x
        self.y = y
        self.x_compare = -1
        self.y_compare = -1

    def add_position(self):
        # new frame, calculate the position of individual fish
        # TODO: need to check for first iteration here.
        if self.fish_id == 1: # || !isEmpty(fish_list)??
            # calculate position of individual fish
            self.generate_bits()
            fish_list.append([self.x, self.y])
        # else another fish on screen add to list
        else:
            fish_list.append([self.x, self.y])

    def generate_bits(self):

        # loop through all the fish position in current frame
        for index in range(len(fish_list)):
            # nothing to compare, init compare values
            if self.x_compare == -1:
                fish_list[index][0] = self.x_compare
                fish_list[index][1] = self.y_compare
            else:
                # fish moved left on the screen
                if self.x_compare > fish_list[index][0]:
                    first_bit = 1
                else:
                    first_bit = 0
                # fish moved up the screen
                if self.y_compare > fish_list[index][1]:
                    second_bit = 1
                else:
                    second_bit = 0

                # overwrite the compare values with new values
                self.x_compare = fish_list[index][0]
                self.y_compare = fish_list[index][1]

                # save the calculated bit values in the stream
                stream.write(first_bit, bool)
                stream.write(second_bit, bool)

        # finished processing current frame, nuke the fish list
        del fish_list[:]












