# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
from pymatgen.core.structure import Structure
from pymatgen.symmetry.kpath import KPathSeek

def get_kpath(structure, delta_k=0.02, style='crystal_b', verbosity=1):
    """ Generate and return kpoint path for band structure
    Args
    ----
    structure : Pymatgen Structure obj
        primitive cell

    delta_k : float
    """
    kpath = KPathSeek(structure).kpath
    kpoints_tmp = kpath['kpoints']
    path = kpath['path']
    
    ### reciprocal lattice
    lat = structure.lattice.matrix
    alat = np.linalg.norm(lat[0]) * np.sqrt(2.)
    
    ##rec_lat = structure.lattice.reciprocal_lattice.matrix
    rec_lat = structure.lattice.reciprocal_lattice_crystallographic.matrix
    rec_lat = alat * rec_lat
    
    ### convert style of k-points
    kpoints = {}
    for name in kpoints_tmp:
        if style == 'crystal_b':
            kpoints[name] = kpoints_tmp[name]
        elif style == 'tpiba':
            kpoints[name] = np.dot(rec_lat, kpoints_tmp[name])
        else:
            print("")
            print(" ERROR: Style %s is not supported." % style)
            exit()

    if verbosity == 1:
        print("")
        print(" k-path generated by SeeK-path : %s" % style)
        for kline in path:
            for kp in kline:
                print(" %10.5f" * 3 % tuple(kpoints[kp]), " ! ", kp)
        print("")

    count = 0
    klist = []
    klengths = []
    names = []
    kpre = None
    
    for il, kline in enumerate(path):
        for ik, kp in enumerate(kline):

            #klist.append(" %12.8f" * 3 % tuple(kpoints[kp]))
            klist.append(list(kpoints[kp]))

            ### calculate number of k-points between two symmetric points
            if ik == len(kline) - 1:
                nk = 1
            else:
                if il < len(path) - 1:
                    knext = np.asarray(kpoints[path[il+1][0]])
                else:
                    knext = np.asarray(kpoints[kline[ik+1]])
                kl = np.linalg.norm(np.asarray(kpoints[kp]) - knext)
                nk = int(kl / delta_k + 0.5)
            
            klist[-1].append(nk)
            names.append(kp)
            count += 1
    ###
    return klist, names


def main(options):
    
    ### Read the give structure file and get the primitive cell
    struct_tmp = Structure.from_file(options.filename)
    structure = struct_tmp.get_primitive_structure()
    
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

    
if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option("-f", "--filename", dest="filename", type="string",
            default="../Si.cif", help="input file name")
    
    parser.add_option("--style", dest="style", type="string",
            default="tpiba", help="style of k-points representation")
    
    (options, args) = parser.parse_args()
    main(options)

