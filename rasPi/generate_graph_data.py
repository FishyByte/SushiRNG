# call constructors
from fish_stream import FishStream
from fish_pool import FishPool

fish_stream = FishStream()
fish_pool = FishPool()

# output bitstream to file
test_input = open('../NIST/data/fishBits11.txt', 'r')
test_output = open('fishData/fishBits.txt', 'w')
test_output.truncate()

print_count = 0


input_bits = test_input.read()
input_bits.replace(' ', '')
input_bits.rstrip('\n')
for current in input_bits:
    if current == '0':
        fish_stream.add_zero()
    elif current == '1':
        fish_stream.add_one()
    else:
        continue

while True:

    if fish_stream.get_length() < 1024:
        break

    prob1, prob2 = fish_stream.get_probabilities()
    entropy = fish_pool.entropy_calculations(prob1, prob2)
    correct_bits = int(fish_pool.entropy_correction(entropy))
    bit_list = str(fish_stream.get_bits(correct_bits))
    result = fish_pool.whiten_numbers(129, bit_list)
    test_output.write(str(result))
    test_output.write(', ')
    print_count += 1



print print_count