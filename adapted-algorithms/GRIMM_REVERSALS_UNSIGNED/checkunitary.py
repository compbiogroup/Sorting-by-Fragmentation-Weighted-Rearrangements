import sys
import commands
from subprocess import call

perms = open(sys.argv[1], 'r')

for a in range(1,10001):
    permutacao = perms.readline()
    comando = ""
    comando = "python2.7 remove_unitary.py %s >> %s" % (permutacao.rstrip(), sys.argv[2])
    call([comando], shell=True)
