# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys

# python compile.py ../output/20%%_t_ output/t_20%%_ > elias_20%.result
# python compile.py ../output/perm_t_ output/t_ > elias_perm.result

lb_output_folder = sys.argv[1]
weight_output_folder = sys.argv[2]
files = [(weight_output_folder + '%s.out', lb_output_folder+'%s.lb')]
for (output, lb_output) in files:
    for i in range(10,501,5):
        lines = 0
        data = pd.read_csv(output%i, sep=';', header=None)
        data = np.asarray(data)
        datalb = pd.read_csv(lb_output%i, sep=';', header=None)
        datalb = np.asarray(datalb)
        total_approx = 0.0
        max_approx = 0
        min_approx = sys.maxsize
        for index in range(len(data)):
            weight = data[index][0]
            lower_bound = datalb[index][0]
            approx = 1
            if(lower_bound != 0):
                approx = weight/(lower_bound*1.0)
            total_approx += approx
            max_approx = max(max_approx, approx)
            min_approx = min(min_approx, approx)
        mean_approx = total_approx/len(data)
        print("%s;%s;%s;%s" % (i, mean_approx, max_approx, min_approx))
        if len(data) != 1000:
            print("ERROR")
            exit()