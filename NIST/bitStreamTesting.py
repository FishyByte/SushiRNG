#Corey Aing
#07/12/2016
#Python script to run NIST tests against a bitstream found in a textfile

import subprocess
from subprocess import Popen, PIPE

#For now this will just perform a Runs test on 120 binary bits from data/data.pi
#Results and statistics .txt files are found in ./experiments/AlgorithmTesting/Runs
p = Popen(["./assess", "120"], stdin=PIPE, stdout=PIPE)

p.stdin.write("0\n")
p.stdin.write("data/data.pi\n")
p.stdin.write("0\n")
p.stdin.write("000100000000000\n")
p.stdin.write("1\n")
p.stdin.write("0\n")
