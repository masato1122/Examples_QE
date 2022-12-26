# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl.initialize import (set_matplot, set_axis, set_legend)

def add_lines_for_symmetric_points(
        ax, kpoints, filename="nscf_bands.in", symmetry_names=None
        ):
    """
    Args
    ----
    """
    lines = open(filename, 'r').readlines()
    for il, line in enumerate(lines):
        data = line.split()
        if len(data) == 0:
            continue
        if "K_POINT" in line:
            ik_init = il
    
    ### parse K_POINT section in "filename"
    nk_div = int(lines[ik_init+1].split()[0])
    ik0 = ik_init + 2
    ik1 = ik_init + 2 + nk_div - 1
    nk_each = []
    idx_div = []
    idx_div.append(0)
    nk_sum = 0
    for il in range(ik0, ik1):
        data = lines[il].split()
        nk = int(float(data[-1]))
        nk_each.append(nk)
        nk_sum += nk
        if il < ik1:
            idx_div.append(nk_sum)
        else:
            idx_div.append(nk_sum - 1)
    
    ### add vertical lines
    for isym, ik in enumerate(idx_div):
        xsym = kpoints[ik]
        ax.axvline(xsym, lw=0.3, c='black', linestyle='-')
        
    ### xticklabels
    if symmetry_names is not None:
        
        labels = symmetry_names.split(":")
        
        xticks = []
        xticklabels = []
        for isym, ik in enumerate(idx_div):
            name = labels[isym]
            if name[0] == "G":
                name = "${\\rm \\Gamma}$"
            
            xsym = kpoints[ik]
            if isym == 0:
                xticks.append(xsym)
                ni = labels[isym]
                xticklabels.append(ni)
            else:
                if abs(kpoints[ik] - kpoints[idx_div[isym-1]]) < 1e-3:
                    name0 = xticklabels[-1]
                    ni = "${\\rm ^{%s}/_{%s}}$" % (name0, name)
                    xticklabels[-1] = ni
                else:
                    xticks.append(xsym)
                    ni = labels[isym]
                    xticklabels.append(ni)
         
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)
     
    ##### add new ticks
    ##flag_new = False
    ##if symmetry_names is not None:
    ##    xticks = kpoints[idx_div]
    ##    labels = symmetry_names.split(":")
    ##    ##
    ##    labels_mod = []
    ##    for ll in labels:
    ##        if ll[0] == "G":
    ##            labels_mod.append("${\\rm \\Gamma}$")
    ##        else:
    ##            labels_mod.append(ll)
    ##    ##
    ##    if len(xticks) == len(labels_mod):
    ##        flag_new = True
    ##        ax.set_xticks(xticks)
    ##        ax.set_xticklabels(labels_mod)
    
    #### delete original ticks
    if flag_new == False:
        ax.tick_params(
                labelbottom=False, bottom=False,
                labeltop=False, top=False, which='both'
                )
    
def plot_band(
        bands, nelectrons=None, figname='fig_band.png', 
        symmetry_names=None,
        dpi=300, fontsize=7, fig_width=2.8, aspect=0.6, lw=0.5, ms=0.5
        ):
    
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
    
    ### add vertical lines
    try:
        kpoints = bands[0][:,0]
        add_lines_for_symmetric_points(
                ax, kpoints, filename="nscf_bands.in",
                symmetry_names=symmetry_names
                )
    except Exception:
        pass
    
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

    plot_band(
            bands, nelectrons=options.nelectrons,
            symmetry_names=options.symmetry_names  
            )
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", type="string",
                      default="Si.band.gnu",
                      help="input file name")
    
    parser.add_option("-n", "--nelectrons", dest="nelectrons", type="int",
                      default=8,
                      help="number of electrons [8]")
    
    parser.add_option("--symmetry_names", dest="symmetry_names", 
                      type="string",
                      default="G:X:U:K:G:L:W:X",
                      help="number of electrons [8]")
    
    (options, args) = parser.parse_args()
    main(options)

