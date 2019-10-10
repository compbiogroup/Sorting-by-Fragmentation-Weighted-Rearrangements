from multiprocessing import Pool
import sys
from subprocess import call
import datetime

def f(command):
    print(command)
    # call(command, shell=True)

if __name__ == '__main__':
    now = datetime.datetime.now()
    p = Pool(int(sys.argv[1]))
    inputDir = sys.argv[2]
    algs = [("r", "r"), ("r", "r_g"), ("t", "t"), ("t", "t_g"), ("rt", "rt"), ("rt", "rt_g"), ("sr", "sr"), ("sr", "sr_g"), ("srt", "srt"), ("srt", "srt_g")]
    commands = []
    for n in range(10,501,5):
        for (problem, alg) in algs:
            prefix_dir = ["20%/"+problem+"_"]
            isSigned = 0
            if('s' in problem):
                isSigned = 1
                prefix_dir.append("sig_perm_")
            else:
                prefix_dir.append("perm_")
            for prefix in prefix_dir:
                    inputPath = inputDir+prefix+str(n)+".in"
                    outputPath = "output/"+prefix.replace('/'+problem, '_'+alg).replace("perm_", "perm_" + alg + "_")+str(n)+".out"
                    outputFile = now.strftime("%Y-%m-%d")
                    command = './prog -a %s -n %s -q 1000 -s %s -i %s -o %s -v 2 >> %s.result ' % (alg,n, isSigned, inputPath, outputPath, outputFile)
                    commands.append(command)
    p.map(f, commands)
