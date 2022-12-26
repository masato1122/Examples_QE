# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mytool.mpl.initialize import (set_matplot, set_axis, set_legend)

def plot_data(xdat, ydat, xc, figname='fig_alat-E.png', 
        dpi=300, fontsize=7, fig_width=2.3, aspect=0.9, lw=0.5, ms=2.0):
    
    ### fitting
    out = np.polyfit(xdat, ydat, 2)
    xc = -out[1] / 2./out[0]
    print(" xcenter [Bohr]: ", xc)
    
    ###
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
        
    ax = plt.subplot()
    ax.set_xlabel('${\\rm a_{lat} (\\Bohr)}$')
    ax.set_ylabel('Energy (Ry)')
    
    ax.plot(xdat, ydat, linestyle='None', lw=lw, marker='o', markersize=ms,
            mfc='none', mew=lw)
    
    ### fitting curve
    nfit = 101
    xfit = np.linspace(np.min(xdat), np.max(xdat), nfit)
    yfit = np.polyval(out, xfit)
    ax.plot(xfit, yfit, linestyle='-', c='black', lw=lw)

    ax.axvline(xc, lw=0.5, linestyle='-', c='grey')
     
    set_axis(ax)
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig


def main(options):

    data = np.genfromtxt(options.filename)
    xdat = data[:,1]
    ydat = data[:,2]
    
    plot_data(xdat, ydat)
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", type="string",
            default="energy.txt", help="input file name")
    (options, args) = parser.parse_args()
    #file_check(options.filename)
    main(options)
