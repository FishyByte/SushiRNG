# Copyright (c) 2016 Christopher Asakawa, Nicholas McHale, Matthew O'Brien, Corey Aing
# This code is available under the "MIT License".
# Please see the file COPYING in this distribution
# for license terms.

# Python script to run NIST tests against a bitstream found in a textfile

import sys
from subprocess import Popen, PIPE


def main():
    runNist(sys.argv[1], sys.argv[2])
    showResults()


def runNist(bitStreamLength, path):
    # Results and statistics .txt files are found in
    # ./experiments/AlgorithmTesting/__respective test directory__/stats.txt
    # Final Analysis Report will be shown automatically after running this script
    # The number following the ./assess argument states the size of the bitstream
    try:
        p = Popen(["./assess", bitStreamLength], stdin=PIPE, stdout=PIPE)

        p.stdin.write("0\n")  # indicates that we want to select a file
        p.stdin.write(path + "\n")  # indicates the file path
        p.stdin.write("1\n")  # apply all tests
        p.stdin.write("0\n")  # indicates using default parameters
        p.stdin.write("1\n")  # indicates how many repeated tests against the bitstream size
        # as long as the .txt file has enough bits
        p.stdin.write("0\n")  # indicates its an ASCII binary file consisting of 0's and 1's
        print "Tests ran successfully"
    except:
        print "Script failed to execute"


def showResults():
    try:
        f = open("./experiments/AlgorithmTesting/finalAnalysisReport.txt", 'r')
        print f.read()
    except:
        print "Results failed to show"


main()
