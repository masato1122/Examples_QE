# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl.initialize import (set_matplot, set_axis, set_legend)

def plot_data(xdat, ydat, figname='fig_dos.png', 
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.6, lw=0.5, ms=0.5):
    
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
        
    ax = plt.subplot()
    ax.set_xlabel('Frequency (THz)')
    ax.set_ylabel('DOS (a.u.)')
    
    ax.plot(xdat, ydat, linestyle='-', lw=lw, marker='.', markersize=ms,
            mfc='none', mew=lw)
     
    ax.axhline(0, lw=0.5, c='grey', linestyle='-')
    set_axis(ax)
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def main(options):
    
    data = np.genfromtxt("total_dos.dat")

    plot_data(data[:,0], data[:,1])

    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", type="string",
        help="input file name")
    (options, args) = parser.parse_args()
    #file_check(options.filename)
    main(options)
