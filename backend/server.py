from flask import Flask, request
from werkzeug.utils import secure_filename
import binascii
import os

UPLOAD_FOLDER = os.getcwd() + '/savedData'
MAX_REQUEST_SIZE = 1000 # users may request up to 1MB

app = Flask(__name__)
app.confg['UPLOAD_FOLDER'] = UPLOAD_FOLDER

byteBuffer = bytearray()

pub_key = '233taewdzvx' # todo: needs to be an env variable


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
    if(numBytes > len(byteBuffer)):
        #UH OH WE NEED MOAR BITS IN MEMORY
        if(fillByteBuffer() == False):

            abort(500) #the client has made a valid request but,
                        #no data is currently available
 
    #OKAY, now we can fufill our request
    usersBytes = byteBuffer[0:numBytes]
    byteBuffer = byteBuffer[numBytes:]
    return byteBuffer

#********************************************************
#
#
#
#********************************************************
# should only allow POST requests from the pi
@app.route("/add-bytes", methods=['POST'])
def set_bits():
    
    if request.method == 'POST':
        #NOW WOULD BE A GREAT TIME TO AUTHENTICATE
        print 'recieved post request:'
        
    else:
        abort(401)#access denied only post requests allowed

    print 'received post request'

    stream = '' # TODO: needs to be outside of this scope, was giving me issues

    if pub_key == request.form['pub_key']:
        print 'matched the key, adding bits to stream...'
        received = int(request.form['fishBits'])
        print 'received:', received
        stream += bin(received)[2:]
        # stream += bin(int(binascii.hexlify(received), 16))[2:]
        print stream

        return 'successfully'
    print 'key does not match, access denied'
    return 'fail'




def fillByteBuffer():
    #attempt to bring in a file to read into the buffer
    files = os.listdir( UPLOAD_FOLDER )
    if (len(files) > 0 ):
        #read in a file, we dont care wich one.
        with open(files[0], 'rb' ) as inFile:
            data = inFile.read()
            byteBuffer.append(data)
        return True
    else:
        return False


if __name__ == "__main__":
    fillByteBuffer()
    app.run()

