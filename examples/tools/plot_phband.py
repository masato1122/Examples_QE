# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mytool.mpl.initialize import (set_matplot, set_axis, set_legend)
    
def _extract_symmetric_kpoints(kpoints):
    
    nk = len(kpoints) - 1
    dks = np.zeros((nk, 3))
    for j in range(3):
        dks[:,j] = np.diff(kpoints[:,j])
    
    ##
    ik0 = 0
    idx_sym = []
    for ik in range(nk-1):
        dk2 = dks[ik+1] - dks[ik]
        if abs(np.linalg.norm(dk2)) > 1e-5:
            idx_sym.append(ik0)
            ik0 = ik + 1
    idx_sym.append(ik0)
    idx_sym.append(nk)
    return idx_sym

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
            #kdat[ik] = ik
        
        for j in range(nbnd):
            frequencies[ik,j] = float(data_f[j])
    
    ### symmetric points
    idx_sym = _extract_symmetric_kpoints(kpoints)
    
    ### adjust overlapping points
    for i in range(1, len(idx_sym)):
        ik_sym0 = idx_sym[i-1]
        ik_sym1 = idx_sym[i]
        if abs(ik_sym1 - ik_sym0) < 2:
            kdiff = kdat[ik_sym1] - kdat[ik_sym0]
            kdat[ik_sym1:] -= kdiff
    
    return kpoints, kdat, frequencies, idx_sym
    
def _plot_symmetric_kpoints(ax, kdat, idx, sym_names):
    """
    kdat : numpy array, shape=(ndat)

    idx : array of index, shape=(nsym)

    sym_names : array of string, shape=(nsym)
    
    """
    names = sym_names.split(":")
    
    ksym = []
    xticks = []
    xticklabels = []
    for isym, ik_sym in enumerate(idx):
        k = kdat[ik_sym]
        ksym.append(k)
        ax.axvline(k, linestyle='-', c='grey', lw=0.3)
        
        ###
        name = names[isym]
        if isym == 0:
            xticks.append(k)
            xticklabels.append(name)
        else:
            if abs(k - kdat[idx[isym-1]]) < 1e-3:
                xticks[-1] = k
                name0 = xticklabels[-1]
                xticklabels[-1] = "${\\rm ^{%s}/_{%s}}$" % (name0, name)
            else:
                xticks.append(k)
                xticklabels.append(name)
    
    set_axis(ax)
    ax.xaxis.set_ticklabels([])
    
    #names = sym_names.split(":")
    #if len(names) == len(ksym):
    #    ax.set_xticks(ksym)
    #    ax.set_xticklabels(names)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)

def plot_band(kpoints, frequencies, idx_sym, figname='fig_band.png', 
        symmetric_names=None,
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.6, lw=0.5, ms=0.5):
    
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
    
    ## symmetric kpoints
    _plot_symmetric_kpoints(ax, kpoints, idx_sym, symmetric_names)

    ax.axhline(0, lw=0.3, c='grey', linestyle='-')
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def main(options):
    
    kpoints, kdat, frequencies, idx_sym = read_phband(options.file_band)

    plot_band(
            kdat, frequencies, idx_sym, 
            symmetric_names=options.symmetric_names,
            figname=options.figname,
            )
    
if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option("--file_band", dest="file_band", type="string",
            default="./Si.freq", help="input file name")
    
    parser.add_option("--figname", dest="figname", type="string",
            default="fig_band.png", help="figure name")
    
    parser.add_option("--symmetric_names", dest="symmetric_names",
                      type="string",
                      default="G:X:U:K:G:L:W:X",
                      help="symmetric names [G:X:U:K:G:L:W:X]")

    (options, args) = parser.parse_args()
    main(options)

