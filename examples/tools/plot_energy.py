# -*- coding: utf-8 -*-
import os.path
import numpy as np
from optparse import OptionParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl.initialize import (set_matplot, set_axis, set_legend)
from scipy import interpolate

try:
    from pymatgen.analysis.eos import EOS
except ImportError:
    print(" Install pymatgen package with the following command:")
    print(" > pip isntall pymatgen")

Bohr2Ang = 0.529177249
Ry2Ev = 13.605698066819

def plot_energy(
        lengths, energies, figname='fig.png', 
        dpi=300, fontsize=7, fig_width=2.0, aspect=0.9, lw=0.5, ms=2.0):
    """ 
    Args
    ------
    lengths : float
        lattice constant with the unit of Angstrom

    energies : float
        energies with the unit of eV
    
    """
    set_matplot(fontsize=fontsize)
    fig = plt.figure(figsize=(fig_width, aspect*fig_width))
        
    ax = plt.subplot()
    ax.set_xlabel('Lattice constant (${\\rm \\AA}$)')
    ax.set_ylabel('Total energy (eV)')
    
    ax.plot(lengths, energies, linestyle='None', lw=lw, 
            marker='o', markersize=ms, mfc='none', mew=lw, mec='black')
        
    try:
        print("\n Fitting with Murnaghan equation of state.")
    
        ### fitting with an equation of state
        eos = EOS(eos_name='murnaghan')
        volumes = np.power(lengths, 3) * 0.25
        eos_fit = eos.fit(volumes, energies)
        
        nfit = 31
        vol_fit = np.linspace(np.min(volumes), np.max(volumes), nfit)
        ene_fit = eos_fit.func(vol_fit)
        lat_fit = np.power(vol_fit*4., 1./3.)
        ax.plot(lat_fit, ene_fit, linestyle='-', lw=lw, c="black", marker=None,
                label="Murnaghan EOS")
        
        ##
        ## Warning: bulk modulus may not correct.
        ##
        msg = "\n Bulk modulus: %.2f GPa" % eos_fit.b0_GPa
        msg += "\n Minimum energy: %.3f eV" % eos_fit.e0
        msg += "\n Optimal lattice constant: %.3f $\\rm{\\AA}$" % (
                np.power(eos_fit.v0*4., 1./3.))
        ax.text(0.97, 0.8, msg, fontsize=5, transform=ax.transAxes,
                horizontalalignment="right", verticalalignment="top")
        print(msg)
    
    except Exception:
        print("\n Intepolate data to plot a line")
        xnew = np.linspace(np.min(volumes), np.max(volumes), 31)
        func = interpolate.interp1d(volumes, energies, kind="cubic")
        ynew = func(xnew)
        ax.plot(xnew, ynew, linestyle='-', lw=lw, c="black", 
                label="interpolated")
    
    ###
    set_axis(ax)
    set_legend(ax, fs=6)

    fig.savefig(figname, dpi=dpi, bbox_inches='tight')
    print("\n Output", figname)
    return fig

def main(options):
    
    ### read file
    dump = np.genfromtxt(options.filename)
    lengths = dump[:,0] * Bohr2Ang      ## Ang
    energies = dump[:,1] * Ry2Ev        ## eV
    
    plot_energy(lengths, energies, figname=options.figname)

if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option("-f", "--filename", dest="filename", type="string",
            default="energy.txt", 
            help="file contains lattice parameter and energy [energy.txt]")
    
    parser.add_option(
            "--figname", dest="figname", type="string",
            default="fig_energy.png", 
            help="figure name [fig_energy.png]")
    
    (options, args) = parser.parse_args()
    main(options)

