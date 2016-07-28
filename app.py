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
import os
from datetime import datetime
import time

UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = ['bin']
MAX_REQUEST_SIZE = 1000  # users may request up to 1MB
MAX_INT_RANGE = 2147483647

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
myBitStream = BitStream()


# pub_key = '' # todo: needs to be an env variable




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
    myStream = "BitString: " + str(myBitStream)
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
    if (numBytes > (len(myBitStream) / 8)):
        # UH OH WE NEED MOAR BITS IN MEMORY
        # if(fillByteBuffer() == False):

        abort(400)  # the client has made a valid request but,
        # no data is currently available

    # OKAY, now we can fufill our request

    try:
        print 'bitstream: len=' + str(len(myBitStream))
        userBytes = myBitStream.read(int8, numBytes)
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
@app.route("/get-ints")
def get_ints():
    quantity = int(request.headers.get('quantity'))
    max_value = int(request.headers.get('max-value'))
    byte_mult = get_byte_multiplier(max_value)
    bounds_check = quantity * byte_mult
    respond = ''

    # error checking for days
    if quantity is None:
        return abort(400)
    if max_value is None:
        return abort(400)
    if quantity < 1:
        return abort(400)
    if bounds_check > MAX_REQUEST_SIZE:
        return abort(400)
    if (len(myBitStream) / 8) < bounds_check:
        return abort(400)
    if max > MAX_INT_RANGE:
        return abort(400)
    try:

        # loop till we fill the order
        while True:
            # ship it
            if quantity == 0:
                return respond

            # grab some byte(s) for one value
            current = int(str(myBitStream.read(8 * byte_mult)), 2)

            # within range? add to return string
            if current < max:
                respond += str(current) + ' '  # white space delimiter
                quantity -= 1

    except Exception, e:
        print e
        return abort(500)


def get_byte_multiplier(int_value):
    counter = 1
    while True:
        if int_value < 256:  # one bye is 0-255
            return counter
        int_value -= 256
        counter += 1


# ********************************************************
# this route will allow the upload of data to the server
# include a string of random bits with the header "raw-data"
#
# ********************************************************
# should only allow POST requests from the pi
@app.route("/add-bytes", methods=['POST'])
def set_bits():
    if request.method == 'POST':
        # TODO: NOW WOULD BE A GREAT TIME TO AUTHENTICATE
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

        bitString = request.form['raw-data']
        i = 0
        while i < len(bitString):
            myBitStream.write(int(bitString[i]), bool)
            i = i + 1

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
        while(len(myBitStream) < MAX_REQUEST_SIZE and i < numFiles):
            curFile = 'data/' + str(files[i])
            i = i + 1
            with open(curFile, 'rb' ) as inFile:
                data = inFile.read(1)
                while data != '':
                    toAdd = int(binascii.hexlify(data), 16)
                    myBitStream.write(toAdd, int8)
                    data = inFile.read(1)
            os.remove(curFile)
        return True
    else:
        return False
"""

if __name__ == "__main__":
    #    fillByteBuffer()
    app.run()
