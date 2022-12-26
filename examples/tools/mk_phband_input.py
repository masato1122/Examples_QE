# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
from pymatgen.core.structure import Structure
from pymatgen.symmetry.kpath import KPathSeek
import f90nml

from inout.kpath import get_kpath

def get_default_params(prefix):
    
    params = {}
    params['flfrc'] = "%s.fc" % (prefix)
    params['flfrq'] = "%s_band.freq" % (prefix)
    params['flvec'] = "%s_band.modes" % (prefix)
    params['dos'] = False
    params['q_in_band_form'] = True
    return {'input': params}

def write_phband_input(outfile, params, klist, names):
    
    with open(outfile, 'w') as f:
        f90nml.write(params, f)
        print(" Output", outfile)
    
    ## k-points
    lines = []
    lines.append("%d" % len(klist))
    for k, name in zip(klist, names):
        lines.append("%10.5f %10.5f %10.5f  %3d  !  %s" % (
            k[0], k[1], k[2], k[3], name
            ))
    ofs = open(outfile, 'a')
    ofs.write("\n".join(lines))
    ofs.close()

def main(options):
    
    ### Read the give structure file and get the primitive cell
    struct_tmp = Structure.from_file(options.filename)
    structure = struct_tmp.get_primitive_structure()
    prefix = structure.composition.reduced_formula
    
    ### parameters of phonon calculation
    params = get_default_params(prefix)
    
    ### k-points and symmetric names
    klist, names = get_kpath(
            structure, delta_k=0.02,
            style=options.style, verbosity=0
            )
    
    print("")
    print(" style : %s" % options.style)
    for k, name in zip(klist, names):
        print("%10.5f %10.5f %10.5f  %d  !  %s" % (
                k[0], k[1], k[2], k[3], name
                ))
    
    ###
    write_phband_input(options.outfile, params, klist, names)

    
if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option("-f", "--filename", dest="filename", type="string",
            default="../Si.cif", help="input file name [../Si.cif]")
    
    parser.add_option("--style", dest="style", type="string",
            default="tpiba", help="kpoint style [tpiba]")
    
    parser.add_option("--outfile", dest="outfile", type="string",
            default="band.in", help="output file name [phband.in]")
    
    (options, args) = parser.parse_args()
    main(options)

