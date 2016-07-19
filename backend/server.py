from flask import Flask, request
import binascii
app = Flask(__name__)

pub_key = '233taewdzvx' # todo: needs to be an env variable

@app.route("/")
def main_page():
    return "Hello World!"

@app.route("/asdf")
def get_bits():
    return "Hello World!asdf"

# should only allow POST requests from the pi
@app.route("/add-bits", methods=['POST'])
def set_bits():
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


if __name__ == "__main__":
    app.run()

