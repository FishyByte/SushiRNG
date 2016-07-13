# Corey Aing
# 07/12/2016
# Python script to run NIST tests against a bitstream found in a textfile

from subprocess import Popen, PIPE

# Results and statistics .txt files are found in ./experiments/AlgorithmTesting/Runs
p = Popen(["./assess", "100093"], stdin=PIPE, stdout=PIPE)

p.stdin.write("0\n")
p.stdin.write("data/fishBits.txt\n")
p.stdin.write("0\n")
p.stdin.write("111111111111111\n")
p.stdin.write("1\n")
p.stdin.write("0\n")
