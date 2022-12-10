# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
from pymatgen.core.structure import Structure
from pymatgen.io.pwscf import PWInput
from pymatgen.io.vasp.inputs import Kpoints

def generate_kmesh_density(structure, reciprocal_density=20):
    """ Generate and return kmesh density based on the density in the 
    reciprocal space.
    
    Args
    ----
    structure : Pymatgen Structure obj
        crystal structure

    reciprocal_density : int
        number of grids
    
    """
    vol = structure.lattice.reciprocal_lattice.volume
    kppa = reciprocal_density * vol * structure.num_sites
    kpoints = Kpoints.automatic_density(structure, kppa)
    kpts = kpoints.kpts[0]
    kpts_shift = kpoints.kpts_shift 
    if 'monkhorst' in kpoints.style.name.lower():
        style = 'automatic'
    else:
        style = 'gamma'
    return kpts, kpts_shift, style

def main(options):
    
    ### read the crystal structure from the structure file and obtain the
    ### primitive structure
    struct_tmp = Structure.from_file(options.filename)
    structure = struct_tmp.get_primitive_structure()
    prefix = structure.composition.reduced_formula
    
    ###
    #symbols = [el.name for el in structure.species]
    #list_of_symbols = list(set(symbols))
    
    ### pseudopotentials
    pseudo = {"Si": "Si.pbesol-n-rrkjus_psl.1.0.0.UPF"} 
    
    ### kmesh density
    kpts, kpts_shift, style = generate_kmesh_density(
            structure, reciprocal_density=options.reciprocal_density
            )
    
    ### control
    control = {
            'prefix': prefix,
            'calculation': options.calculation,
            'pseudo_dir': options.pseudo_dir,
            'outdir': options.outdir,
            }

    ### system
    system = {
            'ecutwfc' : options.ecutwfc,
            'ecutrho' : options.ecutwfc * options.frac_ecutrho,
            }

    ### electrons
    electrons = {
            'conv_thr': options.conv_thr
            }
    
    pwinput = PWInput(
            structure, pseudo=pseudo,
            control=control,
            system=system,
            electrons=electrons,
            kpoints_mode=style,
            kpoints_grid=kpts,
            kpoints_shift=kpts_shift,
            )
    
    outfile = options.calculation + '.in'
    pwinput.write_file(outfile)
    print(" Output", outfile)
    
    
if __name__ == '__main__':
    
    parser = OptionParser()
    
    parser.add_option("-f", "--filename", dest="filename", type="string",
                      default="../Si.cif", 
                      help="file name of a structure [../Si.cif]")
    
    parser.add_option("--reciprocal_density", dest="reciprocal_density", 
                      type="float", default=20, 
                      help="kmesh density in the reciprocal space [20]")
    
    parser.add_option("--calculation", dest="calculation", type="string",
                      default="scf", 
                      help="calculation (scf, nscf, bands, relax, ...) [scf]")
    
    parser.add_option("--pseudo_dir", dest="pseudo_dir", type="string",
                      default="../pseudo", 
                      help="directory of peudofunctions [../pseudo]")
    
    parser.add_option("--outdir", dest="outdir", type="string",
                      default="./out", 
                      help="output directory [./out]")
    
    parser.add_option("--ecutwfc", dest="ecutwfc", type="float",
                      default=60.0, 
                      help="kinetic energy cutoff for wavefunctions"\
                              "with the unit of Ry [60.0]")
    
    parser.add_option("--frac_ecutrho", dest="frac_ecutrho", type="float",
                      default=4.0, 
                      help="kinetic energy cutoff for charge density "\
                              "and potential [4.0]")
     
    parser.add_option("--conv_thr", dest="conv_thr", type="float",
                      default=1e-6, 
                      help="convergence threshold for selfconsistency [1e-6]")
     
    (options, args) = parser.parse_args()
    main(options)

