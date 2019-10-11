# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys

#TODO change to include approx mean

for i in range(15,505,5):
    data = pd.read_csv('output/rt_%s.dist' % i, sep=';', header=None)
    data = np.asarray(data)
    total_weight = 0.0
    max_weight = 0
    min_weight = sys.maxsize
    for row in data:
        weight = row[0]
        total_weight += weight
        max_weight = max(max_weight, weight)
        min_weight = min(min_weight, weight)
    total_weight = total_weight/len(data)
    print("%s;%s;%s;%s" % (i, total_weight, max_weight, min_weight))

for i in range(2,11):
    data = pd.read_csv('output/rt_%s.dist' % i, sep=';', header=None)
    data = np.asarray(data)
    total_weight = 0.0
    max_weight = 0
    min_weight = sys.maxsize
    for row in data:
        weight = row[0]
        total_weight += weight
        max_weight = max(max_weight, weight)
        min_weight = min(min_weight, weight)
    total_weight = total_weight/len(data)
    print("%s;%s;%s;%s" % (i, total_weight, max_weight, min_weight))
