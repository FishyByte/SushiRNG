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
# bitstream page: https://github.com/boisgera/bitstream
from flask import Flask, request
from werkzeug.utils import secure_filename
from bitstream import BitStream
from numpy import *
import binascii
import os


UPLOAD_FOLDER = '/home/rngData'
ALLOWED_EXTENSIONS=['bin']
MAX_REQUEST_SIZE = 1000 # users may request up to 1MB

app = Flask(__name__)
app.confg['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
myBitStream = BitStream()

#pub_key = '' # todo: needs to be an env variable


#********************************************************
#
#
#
#********************************************************
@app.route("/")
def main_page():
    #TODOXXX
    
    return "Hello World!"
    abort(401)#NOTHING TO SEE HERE

#********************************************************
#
#
#
#********************************************************
@app.route("/getBytes")
def get_bits():
    numBytes = request.headers.get('number-bytes-requested')
    if ((numBytes == None) or (numBytes < 1) or (numBytes > MAX_REQUEST_SIZE)):
        abort(400) #invalid request, we dont waste time around here, come back when you are prepared.
    if(numBytes > len(myBitStream)):
        #UH OH WE NEED MOAR BITS IN MEMORY
        if(fillByteBuffer() == False):

            abort(500) #the client has made a valid request but,
                        #no data is currently available
 
    #OKAY, now we can fufill our request
    usersBytes = myBitStream.read( int8, numBytes )
    return userBytes

#********************************************************
#
#
#
#********************************************************
#should only allow POST requests from the pi
@app.route("/add-bytes", methods=['POST'])
def set_bits():
    
    if request.method == 'POST':
        #TODO: NOW WOULD BE A GREAT TIME TO AUTHENTICATE
        print 'recieved post request:'
        
        # check if the post request has the file part
        if 'document' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['document']
        # if user does not select file, browser also
        # submit a empty part without filename
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'success'
    else:
        abort(401) #access denied only post requests allowed


def fillByteBuffer():
    #attempt to bring in a file to read into the buffer
    
    files = os.listdir( UPLOAD_FOLDER )
    if (len(files) > 0 ):
        #read in a file, we dont care wich one.
        with open(files[0], 'rb' ) as inFile:
            data = inFile.read()
            myBitStream.write(data, bool)
        return True
    else:
        return False


if __name__ == "__main__":
    fillByteBuffer()
    app.run()

