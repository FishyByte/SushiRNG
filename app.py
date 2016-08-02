# *********************************************************************
# The MIT License (MIT)
#
# Copyright (c) 2016 Christopher Asakawa, Mathew O'Brien, Nicholas McHale, Corey Aing
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# permit persons to whom the Software is furnished to do so, subject 
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
# OTHER DEALINGS IN THE SOFTWARE.
# *******************************************************************
# bitstream page: https://github.com/boisgera/bitstream

from flask import Flask, request, abort
from flask_cors import CORS
from bitstream import BitStream
from numpy import *
import binascii
import os
import math
from fish_pool import FishPool

MAX_REQUEST_SIZE = 1000  # users may request up to 1MB
MAX_INT_RANGE = 2147483647  # max value for an integer

app = Flask(__name__)  # init the flask application
CORS(app)  # enable cross-origin resource sharing on all routes

# init class objects
fish_stream = BitStream()  # class that holds processed bits in a stream
fish_pool = FishPool()  # class that processes raw bits from fish tank


# ********************************************************
#   The following is all of the flask routes, that can be
#   accessed via http requests (https://fish-bit-hub.herokuapp.com/).
#   Here is a list of the following GET request routes:
#
#       ("/")               home route for stream analysis
#       ("/get-bytes")      returns a series of byte values
#       ("/get-binary")     returns a binary string
#       ("/get-ints")       returns a string of integers
#       ("/get-hex")        returns a string of hex values
#       ("/get-lottery")    returns a string of integers
#
#   The only POST route for this application is secured with
#   a secret key, there is only one client that is allowed to
#   make POST requests (raspberry pi). This route for this is
#
#       ("/set-bits")       sets the bits that are passing in
#                           through the header field.
#
# ********************************************************

# home route, runs analysis on stream
@app.route("/")
def main_page():
    return stream_analysis()


# returns a series of byte values
@app.route("/get-bytes")
def get_bytes():
    quantity = int(request.headers.get('quantity'))
    if (quantity is None) or (quantity < 1) or (quantity > MAX_REQUEST_SIZE):
        abort(400)  # invalid request

    # OKAY, now we can fulfill our request
    try:
        return str(fish_stream.read(int8, quantity))
    except Exception, e:
        print e
        return abort(500)


# returns a binary string
@app.route("/get-binary")
def get_binary():
    quantity = int(request.headers.get('quantity'))

    # empty request OR param value too small OR too large
    if quantity is None or quantity < 1 or quantity > MAX_REQUEST_SIZE:
        return abort(400)

    # ship it
    try:
        return str(fish_stream.read(quantity))
    except Exception, e:
        print e
        return abort(500)


# returns a series of integers with a white space delimiter
@app.route("/get-ints")
def get_ints():
    quantity = int(request.headers.get('quantity'))
    max_value = int(request.headers.get('max-value'))
    bits_requested = get_number_bits(max_value)

    # Error checking: empty request, or out of bounds, or too large
    if quantity is None or max_value is None or quantity < 1 or max_value < 1 \
            or bits_requested > (MAX_REQUEST_SIZE * 8) or max_value > MAX_INT_RANGE:
        return abort(400)

    try:
        return get_ints_with_range(max_value, quantity)
    except Exception, e:
        print e
        return abort(500)


@app.route("/get-hex")
def get_hex():
    quantity = int(request.headers.get('quantity'))

    # empty request OR param value to small OR to big
    if quantity is None or quantity < 1 or quantity > MAX_REQUEST_SIZE:
        return abort(400)

    try:
        return get_hex_values(quantity / 2)
    except Exception, e:
        print e
        return abort(500)


# returns a string of integers
@app.route("/get-lottery")
def get_lottery():
    quantity = int(request.headers.get('quantity'))
    which_lottery = str(request.headers.get('which-lottery'))

    # empty request
    if quantity is None or which_lottery is None:
        return abort(400)

    # only allow one to five rows
    if quantity < 1 or quantity > 5:
        return abort(400)

    # grab lottery numbers ranges, fix offset by one
    if which_lottery == 'Powerball':
        white_range = 69  # 1-69
        red_range = 26  # 1-26
    elif which_lottery == 'MegaMillions':
        white_range = 75  # 1-75
        red_range = 15  # 1-15
    else:
        return abort(400)

    try:
        return get_lottery_lines(quantity, white_range, red_range)
    except Exception, e:
        print e
        return abort(500)


# POST route, only one client, which is the raspberry pi
@app.route("/set-bits", methods=['POST'])
def set_bits():
    if request.method == 'POST':

        # first lets authenticate the post
        if os.environ['SECRET_KEY'] != request.form['secret-key']:
            return abort(401)

        print '...received post request...'
        # grab the raw bits from the header
        raw_bits = str(request.form['raw-data'])
        # process those raw bits
        processed_bits = fish_pool.process_bits(raw_bits)
        # lets loop through the processed string and add it to the fish_stream
        for i in range(len(processed_bits)):
            fish_stream.write(int(processed_bits[i]), bool)
        return 'success'
    else:
        abort(401)  # access denied only post requests allowed


# init the flask server
if __name__ == "__main__":
    app.run()


# run analysis on the bit stream and return the results formatted
# into a string formatted with html
def stream_analysis():
    analyze_stream = str(fish_stream)
    # get counts of ones zeros and total
    zero_count = analyze_stream.count('0')
    one_count = analyze_stream.count('1')
    total_count = zero_count + one_count

    # lets avoid that divide by zero
    if total_count == 0:
        return '<h3>empty stream :(</h3>'

    # now lets get the probabilities of each
    percent_zeros = zero_count / float(total_count)
    percent_ones = one_count / float(total_count)

    entropy = (-percent_ones * math.log(percent_ones, 2)) + \
              (-percent_zeros * math.log(percent_zeros, 2))

    # now return a string with the calculated analysis
    response = '<h3>Fish Bit Hub Analysis</h3> total bits in stream: ' + str(total_count) + \
               '<br> percentage of zeros: ' + str(percent_zeros) + \
               '<br> percentage of ones: ' + str(percent_ones) + \
               '<br> entropy calculation: ' + str(entropy)
    return response


# get a random integer with a specified range, the minimum bound
# is static as zero, and the upper bound is non-inclusive
def get_ints_with_range(max_value, quantity):
    bits_requested = get_number_bits(max_value)
    respond = ''

    # loop till we fill the order
    while True:
        # ship it
        if quantity == 0:
            return respond

        # grab some byte(s) for one value
        current = int(str(fish_stream.read(bits_requested)), 2)

        # within range? add to return string
        if current < max_value:
            respond += str(current) + ' '  # white space delimiter
            quantity -= 1

            # todo: figure out a way to not waste bits here.


# calls get_int_with_range() until the order is filled, then returns
# the results parsed into a string
def get_lottery_lines(quantity, white, red):
    response = ''
    print 'hit lottery function'
    # loop through the quantity specified
    for i in range(0, quantity):
        # number list, used to avoid duplicates
        numbers = []

        # loop through until we get enough values for one line
        while True:
            # grab the white ball value
            white_ball = int(get_ints_with_range(white, 1)) + 1  # correct zero offset
            # not in the list? then add it
            if white_ball not in numbers:
                numbers.append(white_ball)

            # sweet we got enough values
            if len(numbers) == 5:
                # sort the list
                numbers.sort()
                # append the red ball
                numbers.append(int(get_ints_with_range(red, 1)) + 1)

                response += ' '.join(str(x) for x in numbers)
                response += ' '
                break

    # were done, return the response string
    return response


# calculate the required number of bits for the upper_bound
# this is used for getting an integer with a range
def get_number_bits(upper_bound):
    return int(math.ceil(math.log((upper_bound + 1), 2)))


# get hex values, returns hex values parsed into a string
def get_hex_values(quantity):
    response = fish_stream.read(int8, quantity)
    response = binascii.hexlify(response)
    # capitalize all the letters in the response
    response = str.upper(response)
    # were done, now ship it
    return str(response)
