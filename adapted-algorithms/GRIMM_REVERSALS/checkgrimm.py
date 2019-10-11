import sys
import commands
import math
from subprocess import call

nperm = 1000
perms = open(sys.argv[2], 'r')
tamanho = int(sys.argv[1])
output = sys.argv[3]
iota = str([i for i in range(1,tamanho+1)])
max_range = (2 ** tamanho) * math.factorial(tamanho)

if (tamanho > 9):
    max_range = nperm

for a in range(1,max_range+1):
    permutacao = perms.readline()
    tmp = open("grimmtmp_%s" % tamanho, "w")
    print >> tmp, ">1"
    print >> tmp, iota.replace(","," ").replace("[","").replace("]","")
    print >>tmp, ">2"
    print >>tmp, permutacao.replace(", "," ").replace(","," ").replace("[","").replace("]","")
    comando = ""
    tmp.close()
    comando = "./grimm -f grimmtmp_%s -L -d -g 1,2 -S 2 > output/%s_%s/%s.out" % (tamanho, output, tamanho, a)
    call([comando], shell=True)