#!/usr/bin/env python
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
# Chris Asakawa, Matt OBrien, Corey Aing, Nick McHale
# 6/28/2016

# Create a length 624 list to store the state of the generator
MT = [0 for i in range(624)]
index = 0

# To get last 32 bits
bitmask_1 = (2 ** 32) - 1

# To get 32. bit
bitmask_2 = 2 ** 31

# To get last 31 bits
bitmask_3 = (2 ** 31) - 1


# Starts the generator seed. This will use fish numbers
def initialize_generator(seed):
    global MT
    global bitmask_1
    MT[0] = seed
    for i in range(1, 624):
        MT[i] = ((1812433253 * MT[i - 1]) ^ ((MT[i - 1] >> 30) + i)) & bitmask_1


# Pulls the numbers out of the array of 624 numbers.
def extract_number(maxed_value, min_value):
    global index
    global MT
    if index == 0:
        generate_numbers()
    y = MT[index]
    y ^= y >> 11
    y ^= (y << 7) & 2636928640
    y ^= (y << 15) & 4022730752
    y ^= y >> 18

    index = (index + 1) % 624
    returnvalue = y % maxed_value
    if returnvalue < min_value:
        return extract_number(maxed_value, min_value)
    else:
        return returnvalue


# Generates 624 numbers
def generate_numbers():
    global MT
    for i in range(624):
        y = (MT[i] & bitmask_2) + (MT[(i + 1) % 624] & bitmask_3)
        MT[i] = MT[(i + 397) % 624] ^ (y >> 1)
        if y % 2 != 0:
            MT[i] ^= 2567483615

def plot_distribution(num_count):
    num_selected = []
    for a in range(len(num_count)):
        num_selected.append(a)
    plt.plot(num_selected, num_count)
    plt.ylabel("Amount of Number")
    plt.xlabel("Number Randomized")
    plt.show()


if __name__ == "__main__":
    # commenting for test purposes
    # Testing purposes. Using time for seed. Will change to fish
    from datetime import datetime
    import matplotlib.pyplot as plt

    now = datetime.now()
    initialize_generator(now.microsecond)

    loop = True
    while loop:
        # ask user for input for testing
        maxed_value = int(input("What is the maximum number:"))
        min_value = int(input("What is the minimum number:"))

        if min_value > maxed_value:
            print('invalid range, please re-enter values')
            print('')
        else:
            num_randoms = int(input("How many numbers:"))
            loop = False

    count_list = []
    # init the count list to have all values equal zero.
    # attemtping a fix
    for a in range(maxed_value + 1):
        count_list.append(0)

    for i in range(num_randoms):
        "gen a rand "
        current_value = extract_number(maxed_value+1, min_value)
        count_list[current_value] += 1

    print('_____  Distribution _____')
    print('value : num of occurrences')
    print('_________________________')
    print('')
    for j in range(len(count_list)):
        print(j, ':', count_list[j], '    variance:', count_list[j]-num_randoms / len(count_list))

    print('_________________________')
    plot_distribution(count_list)
