# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys

def plot(name, plots, legend, x_init, x_end, x_step, lim_inf, lim_sup):
    import matplotlib
    import matplotlib.pyplot as plt

    n_unsigned = np.asarray(range(x_init, x_end+1, x_step))
    print(n_unsigned)
    pgf_with_custom_preamble = {
    "font.family": "serif", # use serif/main font for text elements
    "text.usetex": True,   # don't setup fonts from rc parameters
    "text.latex.preview": True,
    "figure.figsize": (9,4),
    "pgf.preamble": [
         "\\usepackage{units}",
          "\\usepackage{amsmath, amsthm, mathtools}",          # load additional packages
          "\def\-{\raisebox{.5pt}{-}}",
         "\\usepackage{metalogo}",
         "\\usepackage{unicode-math}",  # unicode math setup
         r"\setmathfont{xits-math.otf}",
         r"\setmainfont{HelveticaLTStd-Bold}", # serif font via preamble
         ]
    }
    plt.rcParams.update(pgf_with_custom_preamble)

    ax = plt.subplot(1, 1, 1)
    for y in plots:
        if(y['label'] == "sqrt"):
            y['label'] = "\sqrt{n}"
        labeldata = y['label'].split("-")
        labeltext = r'$\mathrm{}$'.format(labeldata[0])+'-'+r'$\mathrm{}$'.format(labeldata[1])
        ax.plot(n_unsigned, y['data'], '-', color=y['color'], markersize=5, marker=y['marker'], label=labeltext)

    matplotlib.rcParams.update({'font.size': 12})
    ax.set_ylim([lim_inf,lim_sup]) #TODO get precise ranges
    ax.legend(loc=legend.replace("_"," "), ncol=4)
    plt.xlabel('Permutation Size', fontsize=12)
    plt.ylabel('Average Approximation Factor', fontsize=12)
    plt.savefig(name + '.eps', bbox_inches='tight', pad_inches = 0)

name= sys.argv[1]
x_init = int(sys.argv[2])
x_end = int(sys.argv[3])
x_step = int(sys.argv[4])
lim_inf = float(sys.argv[5])
lim_sup = float(sys.argv[6])
legend = (sys.argv[7])
arg = 8
plots = []
while len(sys.argv) > arg:
    y = {}
    y['data'] = pd.read_csv(sys.argv[arg + 0], header=None, sep=';')
    column = int(sys.argv[arg + 1])
    y['data'] = np.asarray(y['data'])[:,column]
    y['color'] = sys.argv[arg + 2]
    y['label'] = sys.argv[arg + 3].replace("_", " ")
    y['marker'] = sys.argv[arg + 4]
    arg += 5
    plots.append(y)

plot(name, plots, legend, x_init, x_end, x_step, lim_inf, lim_sup)
