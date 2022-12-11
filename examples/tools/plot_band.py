# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl.initialize import (set_matplot, set_axis, set_legend)

def plot_band(bands, nelectrons=None, figname='fig_band.png', 
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.6, lw=0.5, ms=0.5):
    
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
        
    ax = plt.subplot()
    ax.set_xlabel('')
    ax.set_ylabel('Energy (eV)')
    
    for band in bands:
        xdat = band[:,0]
        ydat = band[:,1]
        
        ## with markers
        #ax.plot(xdat, ydat, linestyle='None', lw=lw, marker='o', markersize=ms,
        #        mfc='none', mew=lw)
        
        ## with line
        ax.plot(xdat, ydat, linestyle='-', lw=lw, c='black',
                marker='.', markersize=ms,
                mfc='none', mew=lw)
    
    if nelectrons is not None:
        nb = len(bands)
        nk = len(bands[0])
        ene_sort = np.sort(bands.reshape(nb*nk,2)[:,1])
        idx_vbm = int(nelectrons * nk / 2) - 1
        ene_vbm = ene_sort[idx_vbm]
        ene_cbm = ene_sort[idx_vbm + 1]
        
        ## Note that this energy is not exact Fermi energy.
        ene_mid = (ene_vbm + ene_cbm) * 0.5
        ax.axhline(ene_mid, lw=0.3, c='grey', linestyle='-')
    
    
    set_axis(ax)
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def read_band_gnu(filename):
    """ read ***.band.gnu file and return data
    """
    data = np.genfromtxt(filename)
    energies = data[:,0]
    xdiff = energies[1:] - energies[:-1]
    idx_neg = list(np.where(xdiff < 0.)[0])
    idx_neg.append(len(data)-1)
     
    bands = []
    for ib in range(len(idx_neg)):
        if ib == 0:
            idat0 = 0
            idat1 = idx_neg[ib]
        elif ib < len(idx_neg):
            idat0 = idx_neg[ib-1] + 1
            idat1 = idx_neg[ib]
        
        bands.append(data[idat0:idat1+1])
    return np.asarray(bands)

def main(options):
    
    bands = read_band_gnu(options.filename)
    
    plot_band(bands, nelectrons=options.nelectrons)
    
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", type="string",
                      default="Si.band.gnu",
                      help="input file name")
    
    parser.add_option("-n", "--nelectrons", dest="nelectrons", type="int",
                      default=8,
                      help="number of electrons [8]")
    
    (options, args) = parser.parse_args()
    main(options)

