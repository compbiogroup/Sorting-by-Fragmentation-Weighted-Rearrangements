# O arquivo rahman2008lin.py é executado com o python2.7 devido a compatibilidade do código
# O arquivo lin_decomposition.py é executado com o python3 devido a compartivilidade do código
# Dentro de rahman2008lin.py é feito uma chamada a lin_decomposition.py

import sys
from subprocess import call

for n in range(10,501,5):
        print("size",n)
        with open('../inputs/perm_'+str(n)+".in") as infile:
                for line in infile:
                        permutation = line.split("\n")[0]
                        command = "(python2.7 rahman2008lin.py " + permutation + ") >> output/"+str(n)+".out"
#                       print(command)
                        call(command, shell=True)
        with open('../inputs/20%/rt_'+str(n)+".in") as infile:
                for line in infile:
                        permutation = line.split("\n")[0]
                        command = "(python2.7 rahman2008lin.py " + permutation + ") >> output/20%_"+str(n)+".out"
#                       print(command)
                        call(command, shell=True)
