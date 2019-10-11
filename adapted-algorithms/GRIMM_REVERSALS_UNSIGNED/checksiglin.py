import sys
import commands
from subprocess import call

perms = open(sys.argv[1], 'r')
max_range = int(sys.argv[2])

for a in range(1,max_range+1):
    permutacao = perms.readline()
    comando = ""
    comando = "python2.7 lin_unsigned_to_signed.py %s >> %s" % (permutacao.rstrip(), sys.argv[3])
    call([comando], shell=True)
