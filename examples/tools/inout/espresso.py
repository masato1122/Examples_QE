# -*- coding: utf-8 -*-
import numpy as np
from pymatgen.io.pwscf import PWInput
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.symmetry.kpath import KPathSeek
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer as spg_analyze

def generate_pwinput(structure, parameters, 
                     propt='scf', pseudo=None,
                     reciprocal_density=(1,1,1),
                     ):
    """
    Args
    -----
    structure : pymatgen Structure obj
        primitive crystal structure
        
    parameters: dict
        dictionary of input paraeters for pw.x.
        See https://www.quantum-espresso.org/Doc/INPUT_PW.html for details.
    
    property : string
        "scf", "dos", "bands", etc.
    """
    ### prefix
    if 'prefix' in parameters:
        prefix = parameters['prefix']
    else:
        prefix = structure.composition.reduced_formula
    
    #### get a crystal system
    ##ibrav = get_ibrav(structure)
    
    ### k-points
    if propt == 'bands':
        style = 'crystal_b'
        from .kpath import get_kpath
        kpts, _ = get_kpath(structure, style=style)
        kpts_shift = []
    
    else:
        kpts, kpts_shift, style = generate_kmesh_density(
                structure, reciprocal_density=reciprocal_density
                )
    
    ### get the default parameters
    default_params = get_default_params(propt.lower(), prefix)
    ##default_params['ibrav'] = ibrav
    
    ### merge "parameters" and "default_params"
    parameters.update(default_params)
    
    ### get nbnd: number of electronic states (bands) to be calcualted.
    if propt == 'bands':
        nbnd = get_suggested_nbnd(frac=1.5)
        parameters['nbnd'] = nbnd

    ### generate dict for PWInput
    keys_set = list(parameters.keys())
    pwinput_dict = {}
    
    for sec in pw_keys:
        for name in pw_keys[sec]:
            if name in keys_set:
                if sec not in pwinput_dict:
                    pwinput_dict[sec] = {}
                pwinput_dict[sec][name] = parameters[name]
    
    ### get PWInput
    pwinput = PWInput(
            structure, pseudo=pseudo,
            control=pwinput_dict['control'],
            system=pwinput_dict['system'],
            electrons=pwinput_dict['electrons'],
            kpoints_mode=style,
            kpoints_grid=kpts,
            kpoints_shift=kpts_shift,
            )
    
    ##
    return pwinput

#def update_pwinput(pwinput_orig, new_params):
#    
#    pwinput_new = pwinput_orig.copy()
#
#    orig_params = pwinput_orig.as_dict()
#    for section in pw_keys:
#        for name in pw_keys[section]:
#            if name in new_params:
#                pwinput_new[section][name] = new_params[name]
#
    
def get_ibrav(structure):
    spg = spg_analyze(structure)
    system = spg.get_crystal_system().lower()
    data = spg.get_symmetry_dataset()
    bravais = data['international'][0].upper()
    ##
    
    ibrav = 0
    if system == 'cubic':
        if bravais == "P":
            ibrav = 1
        elif bravais == "F":
            ibrav = 2
        elif bravais == "I":
            ibrav = 3
    
    return ibrav

def get_suggested_nbnd(frac=1.5, file_scfout='scf.out'):
    try:
        out = _read_pwout(file_scfout)
        nbnd = int(out['nelectrons'] * frac + 0.5)
    except Exception:
        nbnd = 10
    return nbnd

def get_default_params(propt, prefix):
    """ Get the default dictionary for the given property.
    Args
    ----
    propt : string
        property (scf, dos, bands, etc)

    prefix : string
        prefix, usually chemical formula
        
    """
    default_dict = {}
    default_dict['prefix'] = prefix
    
    if propt == 'scf':
        default_dict = {
                'calculation': 'scf',
                'restart_mode': 'from_scratch',
                'occupations': 'fixed',
                }
    
    elif propt == 'dos':
        default_dict = {
                'calculation': 'nscf',
                'occupations': 'tetrahedra',
                }
    elif propt == 'bands':
        default_dict = {
                'calculation': 'bands',
                'occupations': 'fixed',
                }
    
    else:
        print("")
        print(" Error: %s is not supported." % propt)
        print("")
        exit()
    
    return default_dict

def _read_pwout(file_out):
    """ Read nscf_dos.out file
    """
    out = {}
    try:
        lines = open(file_out, 'r').readlines()
        for il, line in enumerate(lines):
            data = line.split()
            if len(data) == 0:
                continue
            if "Fermi energy" in line:
                out['efermi'] = float(data[-2])
            
            if "number of electrons" in line:
                nel = data[-1]
                out['nelectrons'] = int(float(data[-1]))
    except Exception:
        pass
    return out

def _read_dosfile(file_dos):
    """ Read {prefix}.dos file
    """
    out = {}
    try:
        line = open(file_dos, 'r').readline()
        data = line.split()
        efermi = float(data[-2])
        ##
        data = np.genfromtxt(file_dos)
        emin = data[0,0]
        emax = data[-1,0]
        out['efermi'] = efermi
        out['emin'] = emin
        out['emax'] = emax
    except Exception:
        pass
    return out

def write_additional_file(propt, info):
    """ Generate additional input scripts for pw.x
    """
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
        #indata[key]['degauss'] = 0.01
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
    if propt == 'scf':
        nml = {}
        nml['inputpp'] = {}
        nml['inputpp']['outdir'] = info['outdir']
        nml['inputpp']['prefix'] = info['prefix']
        nml['inputpp']['plot_num'] = 0
        nml['plot'] = {}
        nml['plot']['iflag'] = 3
        nml['plot']['output_format'] = 6
        nml['plot']['fileout'] = info['prefix'] + "_rho.cube"
        nml['plot']['nx'] = 64
        nml['plot']['ny'] = 64
        nml['plot']['nz'] = 64
        outfile = 'pp.in'
        with open(outfile, 'w') as f:
            f90nml.write(nml, f)
            print(" Output", outfile)
    
    elif propt == 'plotband':

        lines = []
        file_band = info['prefix'] + '.band'
        file_xmgr = info['prefix'] + '.band.xmgr'
        file_ps = info['prefix'] + '.band.ps'
        file_dos = info['prefix'] + ".dos"
        file_dosout = "./nscf_dos.out"
        
        ### read DOS data
        out = _read_pwout(file_dosout)
        out2 = _read_dosfile(file_dos)
        out.update(out2)
        
        try:
            emin = out['emin']
            emax = out['emax']
            efermi = out['efermi']
        except Exception:
            emin = -20
            emax = 20
            efermi = 0
        
        lines.append(file_band)
        delta_e = emax - emin
        lines.append("%f  %f" % (emin - 0.05*delta_e, emax + 0.05*delta_e))
        lines.append(file_xmgr)
        lines.append(file_ps)
        lines.append("%f" % efermi)
        lines.append("1 %f" % efermi)
        
        outfile = "plotband.in"
        with open(outfile, 'w') as f:
            f.write("\n".join(lines))
            print(" Output", outfile)


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
    
    #if 'monkhorst' in kpoints.style.name.lower():
    #    style = 'automatic'
    #else:
    #    style = 'gamma'
    
    style = 'automatic'
    return kpts, kpts_shift, style

#def get_kpath(structure, delta_k=0.02):
#    """ Generate and return kpoint path for band structure
#    Args
#    ----
#    structure : Pymatgen Structure obj
#        primitive cell
#
#    delta_k : float
#    """
#    kpath = KPathSeek(structure).kpath
#    kpoints = kpath['kpoints']
#    path = kpath['path']
#    
#    print("")
#    print(" k-path generated by SeeK-path")
#    for kline in path:
#        for kp in kline:
#            print(" %10.5f" * 3 % tuple(kpoints[kp]), " ", kp)
#    print("")
#    
#    count = 0
#    klist = []
#    klengths = []
#    kpre = None
#    for kline in path:
#        for ik, kp in enumerate(kline):
#
#            #klist.append(" %12.8f" * 3 % tuple(kpoints[kp]))
#            klist.append(list(kpoints[kp]))
#            
#            ### calculate number of k-points between two symmetric points
#            if ik < len(kline) - 1:
#                knext = np.asarray(kpoints[kline[ik+1]])
#                kl = np.linalg.norm(np.asarray(kpoints[kp]) - knext)
#                nk = int(kl / delta_k + 0.5)
#            else:
#                nk = 20
#            
#            #klist[-1].append("  %d  ! %s" % (nk, kp))
#            klist[-1].append(nk)
#            count += 1
#    ###
#    #klist[0] = "%d\n" % count
#    return klist


pw_keys = {
        'control':(
            ## string
            'calculation', 
            'title', 
            'restart_mode', 
            'verbosity', 
            'outdir', 
            'wfcdir', 
            'prefix', 
            'disk_io', 
            'pseudo_dir', 
            ## int
            'nstep', 
            'iprint', 
            'nberrycyc', 
            'gdir', 
            'nppstr', 
            ## bool
            'wf_collect', 
            'tstress', 
            'tprnfor', 
            'lkpoint_dir', 
            'tefield', 
            'dipfield', 
            'lelfield', 
            'lorbm', 
            'lberry', 
            'gate', 
            'lfcp', 
            'trism'
            ## float
            'dt', 
            'max_seconds', 
            'etot_conv_thr', 
            'forc_conv_thr', 
            ),
        'system':(
            ### int
            "ibrav", "nat", "ntyp", "nbnd",
            "nr1", "nr2", "nr3",
            "nr1s", "nr2s", "nr3s",
            "nspin",
            "nqx1", "nqx2", "nqx3",
            "edir",
            "report",
            "esm_nfit",
            "dftd3_version",
            "space_group",
            "origin_choice",
            ### real
            "celldm",
            "A", "B", "C",
            "cosAB", "cosAC", "cosBC",
            "tot_charge",
            "starting_charge",
            "tot_magnetization",
            "starting_magnetization",
            "ecutwfc", "ecutrho", "ecutfock",
            "degauss",
            "ecfixed",
            "qcutz",
            "q2sigma",
            "exx_fraction",
            "screening_parameter",
            "ecutvcut",
            "localization_thr",
            "emaxpos",
            "eopreg",
            "eamp",
            "fixed_magnetization",
            "lambda",
            "esm_w",
            "esm_efield",
            "gcscf_mu", "gcscf_conv_thr", "gcscf_beta",
            "london_s6", "london_c6", "london_rvdw", "london_rcut",
            "ts_vdw_econv_thr",
            "xdm_a1", "xdm_a2",
            "zgate",
            "block_1", "block_2", "block_height",
            ### real, array
            "Hubbard_occ", "Hubbard_alpha", "Hubbard_beta",
            "starting_ns_eigenvalue",
            "angle1", "angle2",
            ### bool
            "nosym",
            "nosym_evc",
            "noinv",
            "no_t_rev",
            "force_symmorphic",
            "use_all_frac",
            "noncolin",
            "ace",
            "x_gamma_extrapolation",
            "dmft",
            "ensemble_energies",
            "lforcet",
            "lspinorb",
            "lgcscf",
            "london",
            "dftd3_threebody",
            "ts_vdw_isolated",
            "xdm",
            "uniqueb",
            "rhombohedral",
            "relaxz",
            "block",
            ### string
            "occupations",
            "one_atom_occupations",
            "starting_spin_angle",
            "smearing",
            "input_dft",
            "exxdiv_treatment",
            "dmft_prefix",
            "constrained_magnetization",
            "assume_isolated",
            "esm_bc",
            "vdw_corr",
            ),
        'electrons': (
            "electron_maxstep",
            "scf_must_converge",
            "conv_thr",
            "adaptive_thr",
            "conv_thr_init",
            "conv_thr_multi",
            "mixing_mode",
            "mixing_beta",
            "mixing_ndim",
            "mixing_fixed_ns",
            "diagonalization",
            "diago_thr_init",
            "diago_cg_maxiter",
            "diago_ppcg_maxiter",
            "diago_david_ndim",
            "diago_rmm_ndim",
            "diago_rmm_conv",
            "diago_gs_nblock",
            "diago_full_acc",
            "efield",
            "efield_cart",
            "efield_phase",
            "startingpot",
            "startingwfc",
            "tqr",
            "real_space",
            ),
        'ions': (
            "ion_positions",
            "ion_velocities",
            "ion_dynamics",
            "pot_extrapolation",
            "wfc_extrapolation",
            "remove_rigid_rot",
            "ion_temperature",
            "tempw",
            "tolp",
            "delta_t",
            "nraise",
            "refold_pos",
            "upscale",
            "bfgs_ndim",
            "trust_radius_max",
            "trust_radius_min",
            "trust_radius_ini",
            "w_1",
            "w_2",
            "fire_alpha_init",
            "fire_falpha",
            "fire_nmin",
            "fire_f_inc",
            "fire_f_dec",
            "fire_dtmax",
            ),
        'cells': (
            "cell_dynamics",
            "press",
            "wmass",
            "cell_factor",
            "press_conv_thr",
            "cell_dofree",
                ),
        'fcp':(
            "fcp_mu",
            "fcp_dynamics",
            "fcp_conv_thr",
            "fcp_ndiis",
            "fcp_mass",
            "fcp_velocity",
            "fcp_temperature",
            "fcp_tempw",
            "fcp_tolp",
            "fcp_delta_t",
            "fcp_nraise",
            "freeze_all_atoms",
            ),
        'rism':(
            "nsolv",
            "closure",
            "tempv",
            "ecutsolv",
            "solute_lj",
            "solute_epsilon",
            "solute_sigma",
            "starting1d",
            "starting3d",
            "smear1d",
            "smear3d",
            "rism1d_maxstep",
            "rism3d_maxstep",
            "rism1d_conv_thr",
            "rism3d_conv_thr",
            "mdiis1d_size",
            "mdiis3d_size",
            "mdiis1d_step",
            "mdiis3d_step",
            "rism1d_bond_width",
            "rism1d_dielectric",
            "rism1d_molesize",
            "rism1d_nproc",
            "rism3d_conv_level",
            "rism3d_planar_average",
            "laue_nfit",
            "laue_expand_right",
            "laue_expand_left",
            "laue_starting_right",
            "laue_starting_left",
            "laue_buffer_right",
            "laue_buffer_left",
            "laue_both_hands",
            "laue_wall",
            "laue_wall_z",
            "laue_wall_rho",
            "laue_wall_epsilon",
            "laue_wall_sigma",
            "laue_wall_lj6",
            ),
        }

