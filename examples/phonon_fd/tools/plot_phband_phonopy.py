# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
import yaml
    
def extract_dispersion(obj):
    
    nk = len(obj)
    nbands = len(obj[0]['band'])
    kpoints = np.zeros((nk, 3))
    kdistances = np.zeros(nk)
    frequencies = np.zeros((nk, nbands))
    for ik in range(nk):
        kpoints[ik] = np.asarray(obj[ik]['q-position'])
        kdistances[ik] = obj[ik]['distance']
        for ib in range(nbands):
            frequencies[ik][ib] = obj[ik]['band'][ib]['frequency']
    
    ##
    dks = np.zeros((nk-1, 3))
    dk_abs = np.zeros(nk-1)
    for j in range(3):
        dks[:,j] = np.diff(kpoints[:,j])
    
    for ik, dk in enumerate(dks):
        dk_abs[ik] = np.linalg.norm(dk)
    
    idx_div = np.where(abs(dk_abs) < 1e-5)[0]
    
    ### idx_sections
    ### 1st section : from idx_sections[0][0] to idx_sections[0][1]
    ### 2st section : from idx_sections[1][0] to idx_sections[1][1]
    idx_sections = []
    for isec, idx in enumerate(idx_div):
        if isec == 0:
            i0 = 0
            i1 = idx 
        else:
            i0 = idx_sections[-1][1] + 1
            i1 = idx 
        idx_sections.append([i0, i1])
    ##
    i0 = idx_div[-1] + 1
    i1 = nk - 1
    idx_sections.append([i0, i1])
    
    for isec, idx in enumerate(idx_sections):
        i0 = idx[0]
        i1 = idx[1]
     
    return kpoints, kdistances, frequencies, idx_sections

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl.initialize import (set_matplot, set_axis, set_legend)

def plot_band(ks, fs, xticks=None, xticklabels=None, 
        figname='fig_phband_phonopy.png', 
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.6, lw=0.5, ms=2.0):
    
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
        
    ax = plt.subplot()
    ax.set_xlabel('')
    ax.set_ylabel('Frequency (${\\rm cm^{-1}}$)')
    
    nb = len(fs[0])
    for ib in range(nb):
        ax.plot(
                ks, fs[:,ib], linestyle='-', lw=lw, marker='None', 
                mfc='none', mew=lw
                )
    
    ### symmetric points
    if xticks is not None and xticklabels is not None:
        for xtick in xticks:
            ax.axvline(xtick, linestyle='-', lw=0.3, c='grey')
        
        if len(xticks) == len(xticklabels):
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticklabels)
    
    ax.axhline(0, lw=0.3, linestyle='-', c='grey')
    set_axis(ax)
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def main(options):
    
    with open(options.filename) as file:
        obj = yaml.safe_load(file)

    kpoints, kdistances, fs, idx_sections = extract_dispersion(obj['phonon'])

    ###
    xticks = []
    xticks.append(kdistances[0])
    for isec, idx in enumerate(idx_sections):
        i1 = idx[1]
        xticks.append(kdistances[i1])
    
    xticklabels = options.symmetric_names.split(":")
    
    plot_band(kdistances, fs, xticks=xticks, xticklabels=xticklabels)

    
if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option("-f", "--filename", dest="filename", type="string",
            default="band.yaml", 
            help="band file generated by Phonopy [band.yaml]")
    
    parser.add_option("--symmetric_names", dest="symmetric_names", 
            type="string",
            default="G:X:U:K:G:L:W:X", 
            help="band file generated by Phonopy [band.yaml]")
    
    (options, args) = parser.parse_args()
    main(options)

