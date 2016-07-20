# Corey Aing
# 07/12/2016
# Python script to run NIST tests against a bitstream found in a textfile

import subprocess
from subprocess import Popen, PIPE

#Results and statistics .txt files are found in ./experiments/AlgorithmTesting/Runs
#The number following the ./assess argument states the size of the bitstream
try:
	p = Popen(["./assess", "200"], stdin=PIPE, stdout=PIPE)

	p.stdin.write("0\n")#indicates that we want to select a file
	p.stdin.write("data/fishBits.txt\n")#indicates the file path
	p.stdin.write("1\n")#apply all tests
	p.stdin.write("0\n")#indicates using default parameters
	p.stdin.write("1\n")#indicates how many repeated tests against the bitstream size
	#as long as the .txt file has enough bits
	p.stdin.write("0\n")#indicates its an ASCII binary file consisting of 0's and 1's
	print "Success"
except:
	print "Script failed to execute"
