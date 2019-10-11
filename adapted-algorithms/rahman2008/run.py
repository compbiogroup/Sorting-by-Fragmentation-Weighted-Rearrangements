import sys
from subprocess import call

for n in range(10,501,5):
        print("size",n)
        with open('../inputs/perm_'+str(n)+".in") as infile:
                for line in infile:
                        permutation = line.split("\n")[0]
                        command = "python rahman2008sig.py %s output/%s.dist output/%s.sort" % (permutation, n, n)
#                       print(command)
                        call(command, shell=True)
        with open('../inputs/20%/srt_'+str(n)+".in") as infile:
                for line in infile:
                        permutation = line.split("\n")[0]
                        command = "python rahman2008sig.py %s output/20%%_%s.dist output/20%%_%s.sort" % (permutation, n, n)
#                       print(command)
                        call(command, shell=True)
