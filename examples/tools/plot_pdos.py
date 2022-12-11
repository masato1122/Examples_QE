# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl.initialize import (set_matplot, set_axis, set_legend, set_spaces)

def set_legend2(ax1, ax2):
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    leg = ax1.legend(h1+h2, l1+l2,
                     fontsize=6, labelspacing=0.3, handlelength=1.0,
                     fancybox=False, edgecolor='grey',
                     loc='best')
    leg.get_frame().set_linewidth(0.5)

def plot_pdos(all_pdos, efermi=None, figname='fig_pdos.png', 
        dpi=300, fontsize=7, fig_width=2.8, lw=0.5, ms=0.5):
    
    cmap = plt.get_cmap("tab10")
    set_matplot(fontsize=fontsize)
     
    ndat = len(all_pdos)
    
    aspect = 0.6 * ndat
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
    set_spaces(plt, hspace=0.4)

    markers = ['o', 'x', '^', 's']
    for idat, each in enumerate(all_pdos):
        
        ax = plt.subplot(ndat, 1, idat+1)
        ax.set_title(each['filename'])
         
        if idat == ndat - 1:
            ax.set_xlabel('Energy (eV)')
        
        ax.set_ylabel('DOS (a.u.)')
        #ax2.set_ylabel('Int. DOS (state)')
        
        filename = each['filename']
        xdat = each['data'][:,0]
        
        ### LDOS
        ydat = each['data'][:,1]
        ax.plot(xdat, ydat, linestyle='None', lw=lw, 
                marker=markers[0], markersize=ms,
                mec=cmap(0), mfc='none', mew=lw, label="LDOS")
        
        ### PDOS
        npdos = len(each['data'][0]) - 2
        for ip in range(npdos):
            label = "PDOS(%d)" % (ip+1)
            ydat = each['data'][:,2+ip] + 0.05*(ip+1)
            ax.plot(xdat, ydat, linestyle='None', lw=lw, 
                    marker=markers[(ip+1)%len(markers)], markersize=ms,
                    mec=cmap(1+ip), mfc='none', mew=lw, label=label)
        
        if efermi is not None:
            ax.axvline(efermi, lw=0.3, c='grey')
        
        set_axis(ax)
        set_legend(ax, loc='best', fs=6)
    
    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print(" Output", figname)
    return fig

def read_all_pdos_file():
    import glob
    line = "*.pdos_atm*"
    fns = glob.glob(line)
    all_pdos = []
    for fn in fns:
        dos_each = np.genfromtxt(fn)
        all_pdos.append(
                {
                    'filename': fn,
                    'data': dos_each,
                    }
                )
    return all_pdos

def main(options):
    
    all_pdos = read_all_pdos_file()

    plot_pdos(all_pdos, efermi=options.efermi)
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-e", "--efermi", dest="efermi", type="float",
                      default=None, 
                      help="fermi energy [None]")
    (options, args) = parser.parse_args()
    main(options)

