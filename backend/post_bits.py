import requests
import os
import time

test_input = ''
for x in range(0, 4):
    path = 'data/fishBits' + str(x) + '.txt'
    test_input = open(path, 'r').read().rstrip('\n')

    payload = {
        'secret-key': os.environ['SECRET_KEY'],
        'raw-data': test_input
    }

    r = requests.post('https://fish-bit-hub.herokuapp.com/add-bytes', data=payload)
    print 'status code:', r.status_code

    # lets wait to let teh back end process that last request
    print 'waiting 10 seconds...'
    time.sleep(10)
