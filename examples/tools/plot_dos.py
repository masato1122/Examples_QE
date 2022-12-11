# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl.initialize import (set_matplot, set_axis, set_legend)

def set_legend2(ax1, ax2):
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    leg = ax1.legend(h1+h2, l1+l2,
                     fontsize=6, labelspacing=0.3, handlelength=1.0,
                     fancybox=False, edgecolor='grey',
                     loc='best')
    leg.get_frame().set_linewidth(0.5)

def plot_dos(dos, efermi, figname='fig_dos.png', 
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.6, lw=0.5, ms=0.5):
    
    cmap = plt.get_cmap("tab10")
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
    
    ax = plt.subplot()
    ax2 = ax.twinx()
    ax.set_xlabel('Energy (eV)')
    ax.set_ylabel('DOS (a.u.)')
    ax2.set_ylabel('Int. DOS (state)')
    
    xdat = dos[:,0] - efermi
    
    ### DOS
    ydat = dos[:,1]
    ax.plot(xdat, ydat, linestyle='None', lw=lw, marker='o', markersize=ms,
            mec=cmap(0), mfc='none', mew=lw, label='DOS')
    ax.axvline(0., lw=0.3, c='grey')
    
    ### integrated DOS
    ydat = dos[:,2]
    ax2.plot(xdat, ydat, linestyle='None', lw=lw, marker='o', markersize=ms,
            mec=cmap(1), mfc='none', mew=lw, label="integrated")
    
    set_axis(ax)
    set_axis(ax2)
    
    ax.tick_params(labelright=False, right=False, which='both')
    ax2.tick_params(labelleft=False, left=False, which='both')

    set_legend2(ax, ax2)
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def read_dos_file(filename):
    
    ### Fermi energy
    line = open(filename, 'r').readline()
    data = line.split()
    efermi = float(data[-2])
    
    ### energy and DOS
    dos = np.genfromtxt(filename)
    return dos, efermi

def main(options):
    
    dos, efermi = read_dos_file(options.filename)

    plot_dos(dos, efermi)
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", type="string",
                      default="./Si.dos", 
                      help=".dos file name [Si.dos]")
    (options, args) = parser.parse_args()
    main(options)

