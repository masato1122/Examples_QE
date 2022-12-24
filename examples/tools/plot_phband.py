# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mytool.mpl.initialize import (set_matplot, set_axis, set_legend)

def read_phband(filename):
    ofs = open(filename, 'r')
    lines = ofs.readlines()
    
    ### 1st line
    line = lines[0]
    line = line.replace(',', " ").replace("=", " ")
    data = line.split()
    nbnd = int(data[2])
    nks = int(data[4])
    
    ### read data (from the 2nd line)
    kpoints = np.zeros((nks,3))
    kdat = np.zeros(nks)
    frequencies = np.zeros((nks, nbnd))
    for ik in range(nks):
        line_k = lines[1+ik*2]
        line_f = lines[1+ik*2+1]

        data_k = line_k.split()
        data_f = line_f.split()

        for j in range(3):
            kpoints[ik,j] = float(data_k[j])

        ##
        if ik > 0:
            kdat[ik] = kdat[ik-1] + np.linalg.norm(kpoints[ik] - kpoints[ik-1])
        
        for j in range(nbnd):
            frequencies[ik,j] = float(data_f[j])

    return kpoints, kdat, frequencies

def plot_band(kpoints, frequencies, figname='fig_band.png', 
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.7, lw=0.5, ms=0.5):
    
    cmap = plt.get_cmap("tab10")
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
        
    ax = plt.subplot()
    ax.set_xlabel('')
    ax.set_ylabel('Frequency (${\\rm cm^{-1}}$)')
    
    nbnd = len(frequencies[0])
    for ib in range(nbnd):
        xdat = kpoints
        ydat = frequencies[:,ib]
        ax.plot(xdat, ydat, linestyle='-', c=cmap(ib), 
                lw=lw, marker='.', markersize=ms,
                mfc='none', mew=lw)
     
    set_axis(ax)
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def main(options):
    
    kpoints, kdat, frequencies = read_phband(options.file_band)
    
    plot_band(kdat, frequencies)
    
if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option("--file_band", dest="file_band", type="string",
            default="./Si.freq", help="input file name")
    
    (options, args) = parser.parse_args()
    main(options)

