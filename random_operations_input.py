from subprocess import call
import sys
import math
problems = ["r", "sr", "t", "rt", "srt"]
outdir = sys.argv[1]
nperms = 1000
for alg in problems:
    uns = 1
    if alg[0] == "s":
        uns = 0
    for size in range(10,501,5):
        nop_types = [("20%", size//5)]
        for (nop_type, nop) in nop_types:
            call('mkdir -p %s/%s' % (outdir, nop_type), shell=True)
            command = './generate-input-op --size %s --nperms %s --nop %s --uns %s --alg %s > %s/%s/%s_%s.in' % (size,nperms,nop,uns,alg,outdir,nop_type,alg,size)
            print(command)
            call(command, shell=True)
