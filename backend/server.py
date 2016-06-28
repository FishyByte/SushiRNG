#!/usr/bin/python
import socketserver
import Queue
import socket
import time
import sys
import os

import reader
import writer

HOST = 'localhost'
PORT = 22555
BUFFER_SIZE = 1024 * 50 #Queue up to 50MB of data before going to file  
 
randomNumberBuffer = Queue.Queue(maxsize=BUFFER_SIZE)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()

        response =
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    while True:
        #just block here for the user to quit
        user_input = input("Type 'Quit' to shutdown the server: ")
        if user_input == "Quit":
            break

    server.shutdown()
    server.server_close()

