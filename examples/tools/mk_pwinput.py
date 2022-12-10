# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
from pymatgen.core.structure import Structure
from pymatgen.io.pwscf import PWInput
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.symmetry.kpath import KPathSeek

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

def get_kpath(structure, dk=0.05):
    """ Generate and return kpoint path for band structure
    Args
    ----
    structure : Pymatgen Structure obj
        primitive cell
    """
    kpath = KPathSeek(structure).kpath
    kpoints = kpath['kpoints']
    path = kpath['path']
    
    count = 0
    klist = []
    klist.append("")
    for kline in path:
        for kp in kline:
            klist.append(" %13.8f" * 3 % tuple(kpoints[kp]))
            klist[-1] += " %d\n" % (30)
            count += 1
    
    klist[0] = "%d\n" % count
    return klist

def genereate_pwinputs(dict_options):
    """ 
    Args
    -----
    dict_options : dict
    """
    ### generate pwinput_dict
    keys_set = list(dict_options.keys())
    pwinput_dict = {}
    from pw_keys import pw_keys
    for sec in pw_keys:
        for name in pw_keys[sec]:
            if name in keys_set:
                if sec not in pwinput_dict:
                    pwinput_dict[sec] = {}
                pwinput_dict[sec][name] = dict_options[name]
    ##
    return pwinput_dict

def write_additional_file(propt, info):
    
    import f90nml
    
    indata = {}
    if propt == 'dos':
        key = propt
        indata[key] = {}
        indata[key]['outdir'] = info['outdir']
        indata[key]['prefix'] = info['prefix']
        file_dos = info['prefix'] + '.dos'
        indata[key]['fildos'] = file_dos
    elif propt == 'pdos':
        key = 'projwfc'
        indata[key] = {}
        indata[key]['outdir'] = info['outdir']
        indata[key]['prefix'] = info['prefix']
        indata[key]['degauss'] = 0.01
    elif propt == 'bands':
        key = 'bands'
        indata[key] = {}
        indata[key]['outdir'] = info['outdir']
        indata[key]['prefix'] = info['prefix']
        file_band = info['prefix'] + '.band'
        indata[key]['filband'] = file_band
        indata[key]['lsym'] = True
    else:
        pass
    
    if len(indata) > 0: 
        outfile = propt + '.in'
        with open(outfile, 'w') as f:
            f90nml.write(indata, f)
            print(" Output", outfile)
    
    ###
    if propt == 'plotband':
        
        lines = []
        file_band = info['prefix'] + '.band'
        file_xmgr = info['prefix'] + '.band.xmgr'
        file_ps = info['prefix'] + '.band.ps'
        file_dos = info['prefix'] + '.dos'
        
        ##
        try:
            with open(file_dos) as f:
                lines_dos = f.readlines()
                data = lines_dos[0].split()
                efermi = float(data[-2])
        except Exception:
            efermi = 0.
            print(" WARRNING: fermi energy cannot be found in %s." % (
                file_dos))
        
        lines.append(file_band)
        lines.append("0 14")
        lines.append(file_xmgr)
        lines.append(file_ps)
        lines.append("%f" % efermi)
        lines.append("1 %f" % efermi)
        
        outfile = "plotband.in"
        with open(outfile, 'w') as f:
            f.write("\n".join(lines))

def main(options):
    
    ### pseudopotentials
    pseudo = {"Si": "Si.pbesol-n-rrkjus_psl.1.0.0.UPF"} 
    
    ### conver to a dictionary
    dict_options = eval(str(options))
    
    ### structure
    ### read the crystal structure from the structure file and obtain the
    ### primitive structure
    struct_tmp = Structure.from_file(options.filename)
    structure = struct_tmp.get_primitive_structure()
    dict_options['prefix'] = structure.composition.reduced_formula
    
    ### calculation
    propt = options.property.lower()
    if propt == 'scf':
        calc = 'scf'
    elif propt == 'dos':
        calc = 'nscf'
        dict_options['occupation'] = 'tetrahedra'
    elif propt == 'bands':
        calc = 'bands'
        dict_options['occupation'] = 'fixed'
    else:
        print(" Error: %s is not supported." % propt)
        exit()
    
    ### kmesh density
    if propt == 'bands':
        style = 'crystal_b'
        kpts = get_kpath(structure)
        kpts_shift = []
    else:
        kpts, kpts_shift, style = generate_kmesh_density(
                structure, reciprocal_density=options.reciprocal_density
                )
    
    ### input parameters for pw.x (or pw.exe)
    pwinput_dict = genereate_pwinputs(dict_options)
    
    pwinput = PWInput(
            structure, pseudo=pseudo,
            control=pwinput_dict['control'],
            system=pwinput_dict['system'],
            electrons=pwinput_dict['electrons'],
            kpoints_mode=style,
            kpoints_grid=kpts,
            kpoints_shift=kpts_shift,
            )
    
    ### output files
    if options.property == 'scf':
        outfile = 'scf.in'
    else:
        outfile = 'nscf_' + options.property + ".in"
        
        write_additional_file(propt, dict_options)
        if propt == 'dos':
            write_additional_file('pdos', dict_options)
        if propt == 'bands':
            write_additional_file('plotband', dict_options)

    pwinput.write_file(outfile)
    print(" Output", outfile)
    

if __name__ == '__main__':
    
    parser = OptionParser()
    
    parser.add_option("-f", "--filename", dest="filename", type="string",
                      default="../Si.cif", 
                      help="structure file name [../Si.cif]")
    
    parser.add_option("--reciprocal_density", dest="reciprocal_density", 
                      type="float", default=20, 
                      help="kmesh density in the reciprocal space [20]")
    
    parser.add_option("--property", dest="property", type="string",
                      default='scf',
                      help="property analyzed (scf, dos, bands, ...) [scf]")
    
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

