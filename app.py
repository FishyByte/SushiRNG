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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# init class objects
fish_stream = BitStream()   # class that holds processed bits in stream
fish_pool = FishPool()      # class that processes raw bits from fish tank

# SECRET_KEY = '' # todo: needs to be an env variable




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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

    # OKAY, now we can fufill our request

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

    respond = ''

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

        print 'recieved post request:'

        """
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print "DBG: No file part"
            abort(400)
            return "no file part"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        
        if file.filename == '':
            flash('No selected file')
            print 'DBG: no seleced file'
            return "no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            current_milli_time = int(round(time.time() * 1000))
            filename = str(current_milli_time) + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'success'
        """
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


"""
def fillByteBuffer():
    #attempt to bring in a file to read into the buffer
    
    files = os.listdir( UPLOAD_FOLDER )
    numFiles = len(files)
    if (numFiles > 0 ):
        #read in a file, we dont care wich one.
        i = 0
        while(len(fish_stream) < MAX_REQUEST_SIZE and i < numFiles):
            curFile = 'data/' + str(files[i])
            i = i + 1
            with open(curFile, 'rb' ) as inFile:
                data = inFile.read(1)
                while data != '':
                    toAdd = int(binascii.hexlify(data), 16)
                    fish_stream.write(toAdd, int8)
                    data = inFile.read(1)
            os.remove(curFile)
        return True
    else:
        return False
"""

if __name__ == "__main__":
    #    fillByteBuffer()
    app.run()
