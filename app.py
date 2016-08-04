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
# FROM, OUT OF OR I CONNECTION WITH THE SOFTWARE OR THE USE OR 
# OTHER DEALINGS IN THE SOFTWARE.
# *******************************************************************
# bitstream page: https://github.com/boisgera/bitstream
# synch psudo code from: https://en.wikipedia.org/wiki/Readers%E2%80%93writers_problem
#

from flask import Flask, request, abort
from flask_cors import CORS
from bitstream import BitStream
from numpy import *
import binascii
import os
import math
from fish_pool import FishPool
from threading import Semaphore
import urlparse
import psycopg2

MAX_REQUEST_BITS = 4096     # max bits that can be requested
MAX_STREAM_SIZE = 1048576   # 2^20 bits
MIN_STREAM_SIZE = 32768     # 2^15 bits

app = Flask(__name__)  # init the flask application
CORS(app)  # enable cross-origin resource sharing on all routes

# init class objects
fish_stream = BitStream()  # class that holds processed bits in a stream
fish_pool = FishPool()  # class that processes raw bits from fish tank

# synch objects
streamResource = Semaphore()

# database url
url = urlparse.urlparse(os.environ["DATABASE_URL"])


# ************************************************************************
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
# ************************************************************************

# home route, runs analysis on stream
@app.route("/")
def main_page():
    acquireReadLock()
    result = stream_analysis()
    releaseReadLock()
    return result


# returns a series of byte values
@app.route("/get-bytes")
def get_bytes():
    bit_check_lower()   # check health of bit stream
    quantity = int(request.headers.get('quantity'))

    # empty or two small of a request
    if (quantity is None) or (quantity < 1):
        abort(400)

    # one byte = 8 bits
    elif (quantity * 8) > MAX_REQUEST_BITS:
        abort(400)

    # OKAY, now we can fulfill our request
    try:
        acquireReadLock()
        result = str(fish_stream.read(int8, quantity))
        releaseReadLock()
        return result
    except Exception, e:
        print e
        releaseReadLock()
        return abort(500)


# returns a binary string
@app.route("/get-binary")
def get_binary():
    bit_check_lower()
    quantity = int(request.headers.get('quantity'))

    # empty request OR param value too small OR too large
    if quantity is None or quantity < 1 or quantity > MAX_REQUEST_BITS:
        return abort(400)

    # ship it
    try:
        acquireReadLock()
        result = str(fish_stream.read(quantity))
        releaseReadLock()
        return result
    except Exception, e:
        print e
        releaseReadLock()
        return abort(500)


# returns a series of integers with a white space delimiter
@app.route("/get-ints")
def get_ints():
    bit_check_lower()
    quantity = int(request.headers.get('quantity'))
    max_value = int(request.headers.get('max-value'))
    bits_requested = get_number_bits(max_value)

    # empty request
    if quantity is None or max_value is None:
        return abort(400)
    # request wants to many bits
    if (quantity * bits_requested) > MAX_REQUEST_BITS:
        return abort(400)

    try:
        acquireReadLock()
        result = get_ints_with_range(max_value, quantity)
        releaseReadLock()
        return result
    except Exception, e:
        print e
        releaseReadLock()
        return abort(500)


@app.route("/get-hex")
def get_hex():
    bit_check_lower()
    quantity = int(request.headers.get('quantity'))

    # empty request OR param value to small
    if quantity is None or quantity < 1:
        return abort(400)

    # one hex = 4 bits
    if (quantity * 4) > MAX_REQUEST_BITS:
        return abort(400)

    try:
        acquireReadLock()
        result = get_hex_values(quantity)
        releaseReadLock()
        return result
    except Exception, e:
        print e
        releaseReadLock()
        return abort(500)


# returns a string of integers
@app.route("/get-lottery")
def get_lottery():
    bit_check_lower()

    quantity = int(request.headers.get('quantity'))
    which_lottery = str(request.headers.get('which-lottery'))

    # empty request
    if quantity is None or which_lottery is None:
        return abort(400)

    # only allow one to five rows
    if quantity < 1 or quantity > 5:
        return abort(400)

    # grab lottery numbers ranges
    if which_lottery == 'Powerball':
        white_range = 69  # 1-69
        red_range = 26  # 1-26
    elif which_lottery == 'MegaMillions':
        white_range = 75  # 1-75
        red_range = 15  # 1-15
    else:
        return abort(400)

    try:
        acquireReadLock()
        result = get_lottery_lines(quantity, white_range, red_range)
        releaseReadLock()

        return result
    except Exception, e:
        print e
        releaseReadLock()
        return abort(500)


# POST route, only one client, which is the raspberry pi
@app.route("/set-bits", methods=['POST'])
def set_bits():
    if request.method == 'POST':

        # first lets authenticate the post
        if os.environ['SECRET_KEY'] != request.form['secret-key']:
            return abort(401)
        acquireWriteLock()
        print '...received post request...'
        # grab the raw bits from the header
        raw_bits = str(request.form['raw-data'])
        # process those raw bits
        processed_bits = fish_pool.process_bits(raw_bits)
        for i in range(len(processed_bits)):
            fish_stream.write(int(processed_bits[i]), bool)

        releaseWriteLock()
        bit_check_upper()  # TODO make this smarter
        return 'done'
    else:
        abort(401)  # access denied only post requests allowed


#############################################################################


# init the flask server
if __name__ == "__main__":
    app.run()


##################
# Reader Synch
##################

def acquireReadLock():
    streamResource.acquire()


def releaseReadLock():
    streamResource.release()


##################
# Writer Synch
##################

def acquireWriteLock():
    streamResource.acquire()


def releaseWriteLock():
    streamResource.release()


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

        # grab some bits for one value
        current = int(str(fish_stream.read(bits_requested)), 2)

        # within range? add to return string
        if current < max_value:
            respond += str(current) + ' '  # white space delimiter
            quantity -= 1

            # todo: implement a way to not be so wasteful


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
    response = str(fish_stream.read((quantity * 4)))
    print response
    # binary string to hex conversion
    response = hex(int(response, 2))[2:]
    print response
    # capitalize all the letters in the response
    response = str.upper(response)
    print response
    # were done, now ship it
    return str(response)


# upper bound check of the bit stream
def bit_check_upper():
    # plenty of bits here, save some for later
    if len(fish_stream) > MAX_STREAM_SIZE:  # 2^20 bits
        insert_db()


# lower bound check of the bit stream
def bit_check_lower():
    # MOAR bits NAOW
    if len(fish_stream) < MIN_STREAM_SIZE:  # 2^14 bits
        pop_db()


# insert into the database
def insert_db():
    # TODO: if DB full then start throwing away bits

    # each row will hold 2^15 bits, max size is 2^20 bits per row
    bit_string = fish_stream.read(MIN_STREAM_SIZE)

    # lets craft up that insert query
    query = "INSERT INTO FishBucket (bits) VALUES('" + str(bit_string) + "');"
    print query  # testing
    try:
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        current = connection.cursor()
        current.execute(str(query))
        connection.commit()
        connection.close()

    except:
        print "unable to connect to the database"


# simulate a pop operation with the database, catch the first row
# and then delete from database, then write that row to the fish_stream
def pop_db():
    # lets craft up that insert queries
    select_query = 'SELECT bits FROM FishBucket ORDER BY timestamp ASC LIMIT 1;'
    delete_query = 'DELETE FROM FishBucket WHERE bits IN (SELECT bits FROM FishBucket ORDER BY timestamp ASC LIMIT 1);'

    try:
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        current = connection.cursor()
        current.execute(str(select_query))
        row = current.fetchone()

        # lets make sure there is data in the DB
        if row is not None:
            bit_string = row[0]
            current.execute(str(delete_query))
        else:
            bit_string = ''
            print 'the FishBucket database is empty...'

        connection.commit()
        connection.close()
        popped_stream = fish_stream.write(str(bit_string))
        for i in range(len(popped_stream)):
            fish_stream.write(int(popped_stream[i]), bool)

    except:
        print "unable to connect to the database"
