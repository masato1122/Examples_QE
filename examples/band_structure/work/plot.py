# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mytool.mpl.initialize import (set_matplot, set_axis, set_legend)

def plot_data(data1, data2, data3, figname='fig_dos.png', 
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.9, lw=0.5, ms=0.8):
    
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
        
    ax = plt.subplot()
    ax.set_xlabel('Energy (eV)')
    ax.set_ylabel('DOS (a.u.)')
    
    labels = ['s', 'p', 'total']
    for i, data in enumerate([data1, data2, data3]):
        xdat = data[:,0]
        ydat = data[:,1]
        ax.plot(xdat, ydat, linestyle='-', lw=lw, marker='.', markersize=ms,
                mfc='none', mew=lw, label=labels[i])
     
    set_axis(ax)
    set_legend(ax, fs=6, alpha=0.5)
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def main(options):
    
    filename1 = "../s_orbital.txt"
    filename2 = "../p_orbital.txt"
    filename3 = "../Si.dos"
    data1 = np.genfromtxt(filename1)
    data2 = np.genfromtxt(filename2)
    data3 = np.genfromtxt(filename3)
    
    plot_data(data1, data2, data3)
     
    
if __name__ == '__main__':
    parser = OptionParser()
    #parser.add_option("-f", "--filename", dest="filename", type="string",
    #                  default="../s_orbital.txt",
    #                  help="input file name")
    (options, args) = parser.parse_args()
    #file_check(options.filename)
    main(options)
