# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
from phonopy.interface.qe import read_pwscf, PH_Q2R

def main(options):

    cell, _ = read_pwscf(options.file_prim)
    q2r = PH_Q2R(options.file_fc)
    q2r.run(cell)
    q2r.write_force_constants(fc_format='txt')

if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option("--file_prim", dest="file_prim", type="string",
            default="./scripts/scf.in",
            help="QE input script containing the primitive cell")
    
    parser.add_option("--file_fc", dest="file_fc", type="string",
            default="../phonon_dfpt/results/Si.fc",
            help="file of force constants calculated with QE")
    
    (options, args) = parser.parse_args()
    main(options)

