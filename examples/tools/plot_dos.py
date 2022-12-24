# -*- coding: utf-8 -*-
import os.path
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

def plot_dos(dos, efermi, carrier='electron', figname='fig_dos.png', 
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.6, lw=0.5, ms=0.5):
    
    cmap = plt.get_cmap("tab10")
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
    
    ax = plt.subplot()
    
    if carrier == 'electron':
        ax.set_xlabel('Energy (eV)')
        ax2 = ax.twinx()
        ax2.set_ylabel('Int. DOS (state)')
    else:
        ax.set_xlabel('Frequency (${\\rm cm^{-1}}$)')
    ax.set_ylabel('DOS (a.u.)')
    
    xdat = dos[:,0] - efermi
    
    ### DOS
    ydat = dos[:,1]
    ax.plot(xdat, ydat, linestyle='-', c='black', lw=lw, marker='.', 
            markersize=ms,
            mec='black', mfc='none', mew=lw, label='total DOS')
    ax.axvline(0., lw=0.3, c='grey')
    
    ### partial DOS
    labels = ['s-orbital', 'p-orbital']
    for i, fn in enumerate(['s_orbital.txt', 'p_orbital.txt']):
        if os.path.exists(fn):
            data = np.genfromtxt(fn)
            ax.plot(
                    data[:,0] - efermi,
                    data[:,1],
                    linestyle='-', lw=lw, 
                    marker='.', markersize=ms, mew=lw, mec=cmap(i+1), mfc='None',
                    label=labels[i]
                )
    
    ### integrated DOS
    if carrier == 'electron':
        ydat = dos[:,2]
        ax2.plot(xdat, ydat, linestyle='-', c='black', lw=lw, 
                 marker='.', markersize=ms,
                 mec='black', mfc='none', mew=lw, label="integrated")
    else:
        ndat = len(dos[0]) - 1
        for i in range(ndat-1):
            label = "PDOS(%d)" % (i+1)
            ydat = dos[:,2+i]
            ax.plot(xdat, ydat, linestyle='-', c=cmap(i), lw=lw, 
                     marker='.', markersize=ms,
                     mec=cmap(i), mfc='none', mew=lw * 0.7, label=label)
    
    set_axis(ax)
    ax.tick_params(labelright=False, right=False, which='both')
    
    if carrier == 'electron':
        set_axis(ax2)
        ax2.tick_params(labelleft=False, left=False, which='both')
        set_legend2(ax, ax2)
    else:
        set_legend(ax, fs=6)

    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def read_dos_file(filename):
    
    ### Read the first line: Fermi energy
    line = open(filename, 'r').readline()
    if "EFermi" in line:
        data = line.split()
        efermi = float(data[-2])
        carrier = 'electron'
    else:
        efermi = 0.
        carrier = 'phonon'
    
    ### energy and DOS
    dos = np.genfromtxt(filename)
    return dos, efermi, carrier

def main(options):
    
    dos, efermi, carrier = read_dos_file(options.filename)

    plot_dos(dos, efermi, carrier=carrier)
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", type="string",
                      default="./Si.dos", 
                      help=".dos file name [Si.dos]")
    (options, args) = parser.parse_args()
    main(options)

