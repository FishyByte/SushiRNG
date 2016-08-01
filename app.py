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

from flask import Flask, request, flash, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
from bitstream import BitStream
from numpy import *
import binascii
import math
import os
from datetime import datetime
import time
from fish_pool import FishPool

UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = ['bin']
MAX_REQUEST_SIZE = 1000     # users may request up to 1MB
MAX_INT_RANGE = 2147483647  # max value for an integer

# init flask app
app = Flask(__name__)
CORS(app)

# init class objects
fish_stream = BitStream()   # class that holds processed bits in stream
fish_pool = FishPool()      # class that processes raw bits from fish tank

# ********************************************************
#
#
#
# ********************************************************
@app.route("/")
def main_page():
    # TODOXXX
    myStream = "BitString: " + str(fish_stream)
    return myStream
    # abort(401)#NOTHING TO SEE HERE


# ********************************************************
#
#
#
# ********************************************************
@app.route("/getBytes")
def get_bits():
    numBytes = int(request.headers.get('number-bytes-requested'))
    if ((numBytes == None) or (numBytes < 1) or (numBytes > MAX_REQUEST_SIZE)):
        abort(400)  # invalid request, we dont waste time around here, come back when you are prepared.
    if (numBytes > (len(fish_stream) / 8)):
        # UH OH WE NEED MOAR BITS IN MEMORY
        # if(fillByteBuffer() == False):

        abort(400)  # the client has made a valid request but,
        # no data is currently available

    # OKAY, now we can fulfill our request

    try:
        print 'bitstream: len=' + str(len(fish_stream))
        userBytes = fish_stream.read(int8, numBytes)
        userBytes = binascii.hexlify(userBytes)
        return userBytes
    except Exception, e:
        print e
        return abort(500)

# ********************************************************
#
#
#
# ********************************************************
@app.route("/get-binary")
def get_binary():
    quantity = int(request.headers.get('quantity'))

    # empty request
    if quantity is None:
        return abort(400)

    # param value too small or too large
    if quantity < 1 or quantity > MAX_REQUEST_SIZE:
        return abort(400)

    # ship it
    try:
        return str(fish_stream.read(quantity))
    except Exception, e:
        print e
        return abort(500)


# ********************************************************
#
#
#
# ********************************************************
@app.route("/get-ints")
def get_ints():
    quantity = int(request.headers.get('quantity'))
    max_value = int(request.headers.get('max-value'))
    bits_requested = get_number_bits(max_value)

    # empty request
    if quantity is None or max_value is None:
        return abort(400)

    # param value to small
    if quantity < 1 or max_value < 1:
        return abort(400)

    # limit request size to 1000 bytes/8000 bits
    if bits_requested > (MAX_REQUEST_SIZE * 8):
        return abort(400)

    # too large of a range
    if max_value > MAX_INT_RANGE:
        return abort(400)

    try:
        return get_ints_with_range(max_value, quantity)

    except Exception, e:
        print e
        return abort(500)


# calculate the required number of bits
def get_number_bits(upper_bound):
    exponent = 1
    number_bits = 1
    while True:

        if upper_bound >= pow(2, exponent):
            number_bits += 1
        else:
            return number_bits

        exponent += 1

# ********************************************************
#
#
#
# ********************************************************
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
    if which_lottery == 'powerball':
        white_range = 69
        red_range = 26
    elif which_lottery == 'megamillions':
        white_range = 75
        red_range = 15
    else:
        return abort(400)

    try:
        get_lottery_lines(quantity, white_range, red_range)
    except Exception, e:
        print e
        return abort(500)
# ********************************************************
# this route will allow the upload of data to the server
# include a string of random bits with the header "raw-data"
#
# ********************************************************
# should only allow POST requests from the pi
@app.route("/add-bytes", methods=['POST'])
def set_bits():
    if request.method == 'POST':

        if os.environ['SECRET_KEY'] != request.form['secret-key']:
            return abort(401)

        print 'received post request:'

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


if __name__ == "__main__":
    #    fillByteBuffer()
    app.run()


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
        if current <= max_value:
            respond += str(current) + ' '  # white space delimiter
            quantity -= 1
        # lets not be wasteful, write unused value back to stream
        else:
            fish_stream.write(str(current))


def get_lottery_lines(quantity, white, red):
    response = ''
    print 'hit lottery function'
    # loop through the quantity specified
    for i in range(0, quantity):
        print 'gathering line', i
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
                print numbers
                # sort the list
                numbers.sort()
                print numbers

                # append the red ball
                numbers.append(int(get_ints_with_range(red, 1)) + 1)
                print numbers

                response += ' '.join(str(numbers))
                response += ' '

                print response
                break

    # were done, return the response string
    return response
