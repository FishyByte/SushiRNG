# call constructors
from rasPi.fish_stream import FishStream
from rasPi.testing.fish_pool import FishPool

fish_stream = FishStream()
fish_pool = FishPool()

# output bitstream to file
test_input1 = open('../NIST/data/fishBits09.txt', 'r')
test_input2 = open('../NIST/data/fishBits10.txt', 'r')
test_input3 = open('../NIST/data/fishBits11.txt', 'r')
test_input4 = open('../NIST/data/fishBits12.txt', 'r')

test_output = open('fishData/fishBits.txt', 'w')
test_output.truncate()

print_count = 0
input_bits = test_input1.read() + test_input2.read() + test_input3.read() + test_input4.read()
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
    result = fish_pool.whiten_numbers(0, 2, bit_list)
    test_output.write(str(result))
    print_count += 1
    if print_count % 64 == 0:
        test_output.write('\n')


test_output.write('\n')
print print_count