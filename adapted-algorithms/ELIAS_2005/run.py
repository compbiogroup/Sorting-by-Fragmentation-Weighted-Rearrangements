import sys
from subprocess import call

for n in range(10,501,5):
        print("size",n)
        with open('../inputs/perm_'+str(n)+".in") as infile:
                for line in infile:
                        permutation = line.split("\n")[0]
                        command = "(python3 elias2005.py " + permutation + ") >> output/t_"+str(n)+".out"
#                       print(command)
                        call(command, shell=True)
        with open('../inputs/20%/t_'+str(n)+".in") as infile:
                for line in infile:
                        permutation = line.split("\n")[0]
                        command = "(python3 elias2005.py " + permutation + ") >> output/t_20%_"+str(n)+".out"
                        print(command)
                        call(command, shell=True)