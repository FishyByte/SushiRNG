# Chris Asakawa, Matt OBrien, Corey Aing, Nick McHale
# 5/28/2016

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


if __name__ == "__main__":
    # commenting for test purposes
    # Testing purposes. Using time for seed. Will change to fish
    from datetime import datetime

    now = datetime.now()
    initialize_generator(now.microsecond)

    loop = True
    while loop:
        # ask user for input for testing
        maxed_value = int(input("What is the maximum number:"))
        min_value = int(input("What is the minimum number:"))

        if min_value > maxed_value:
            print ('invalid range, please re-enter values')
            print ('')
        else:
            num_randoms = int(input("How many numbers:"))
            loop = False

    for i in range(num_randoms):
        "gen a rand "
        current_value = extract_number(maxed_value+1, min_value)
        if current_value == min_value:
            print ('hit the minimum')
        if current_value == maxed_value:
            print ('hit the maximum')
