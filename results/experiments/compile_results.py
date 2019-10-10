import sys
import datetime
import math
def prepareResults(outputPath):
    count = 0
    nperms = 1000
    result = ""
    with open(outputPath) as infile:
        approx_sum = 0
        approx_max = 0
        approx_min = 100000000 # good value for min approx
        for line in infile:
            if(count == nperms):
                break
            count += 1
            data = line.split(';')
            if(len(data) == 2):
                lower_bound = float(data[0])
                weight = float(data[1])
                approx = 1
                if(lower_bound > 0):
                    approx = weight/math.ceil(lower_bound)
                approx_sum += approx
                if (approx > approx_max):
                    approx_max = approx
                if (approx < approx_min):
                    approx_min = approx
            else:
                print("ERROR", outputPath)
        if count < nperms:
            print("ERROR", outputPath);
        result += "%s;%s;%s;%s;%s" % (alg, n, approx_sum/(1.0*count), approx_max, approx_min)
    return result

if __name__ == '__main__':
    now = datetime.datetime.now()
    algs = ["r", "t", "rt", "sr", "srt", "r_g", "t_g", "rt_g", "sr_g", "srt_g"]
    for alg in algs:
        prefix_dir = ["20%_"+alg+"_"]
        isSigned = 0
        if(alg[0] == 's'):
            prefix_dir.append("sig_perm_" + alg + "_")
            isSigned = 1
        else:
           prefix_dir.append("perm_" + alg + "_")
        for prefix in prefix_dir:
            outputFile = open("results/"+prefix+".result", "w")
            for n in range(10,501,5):
                outputPath = "../../output/"+prefix+str(n)+".out"
                # print(outputPath)
                result = prepareResults(outputPath)+"\n"
                outputFile.write(result)
            outputFile.close()
