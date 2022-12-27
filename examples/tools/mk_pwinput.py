# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
from pymatgen.core.structure import Structure
from inout.espresso import generate_pwinput, write_additional_file

def main(options):
    
    ### pseudopotentials
    pseudo = {"Si": "Si.pbesol-n-rrkjus_psl.1.0.0.UPF"} 
    
    ### conver to a dictionary
    dict_options = eval(str(options))
    
    ### Read the give structure file and get the primitive cell
    if options.primitive:
        struct_tmp = Structure.from_file(options.filename)
        structure = struct_tmp.get_primitive_structure()
    else:
        structure = Structure.from_file(options.filename)
    
    ### add prefix to the dictionary
    prefix = structure.composition.reduced_formula
    dict_options['prefix'] = prefix
    
    ### get the analyzed property
    propt = options.property.lower()
    
    ### generate an object which contains parameters for pw.x (or pw.exe)
    pwinput = generate_pwinput(
            structure, 
            dict_options, 
            propt=propt, 
            pseudo=pseudo,
            reciprocal_density=options.reciprocal_density
            )
    
    ### output files
    if options.property == 'scf':
        outfile = 'scf.in'
    else:
        outfile = 'nscf_' + options.property + ".in"
        
    pwinput.write_file(outfile)
    print(" Output", outfile)
    
    write_additional_file(propt, dict_options)
    if propt == 'dos':
        write_additional_file('pdos', dict_options)
    if propt == 'bands':
        write_additional_file('plotband', dict_options)
    

if __name__ == '__main__':
    
    parser = OptionParser()
    
    parser.add_option("-f", "--filename", dest="filename", type="string",
                      default="../Si.cif", 
                      help="structure file name [../Si.cif]")
    
    parser.add_option("--primitive", dest="primitive", type="int",
                      default=1, 
                      help="get primitive structure (0.Off, 1.On [1]")
    
    parser.add_option("--reciprocal_density", dest="reciprocal_density", 
                      type="float", default=20, 
                      help="k-mesh density in the reciprocal space [20]")
    
    parser.add_option("--property", dest="property", type="string",
                      default='scf',
                      help="property analyzed (scf, dos, bands, ...) [scf]")
    
    parser.add_option("--pseudo_dir", dest="pseudo_dir", type="string",
                      default="../pseudo", 
                      help="directory of peudofunctional files [../pseudo]")
    
    parser.add_option("--outdir", dest="outdir", type="string",
                      default="./out", 
                      help="output directory [./out]")
    
    parser.add_option("--ecutwfc", dest="ecutwfc", type="float",
                      default=60.0, 
                      help="kinetic energy cutoff for wavefunctions "\
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

