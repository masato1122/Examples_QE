Calculation of band structure with QuantumEspresso (QE)
========================================================

One can learn how to calculate electronic states such as band structure and density of states (DOS) 
with QuantumEspresso (QE) following the process described below.


A few things before starting the analysis 
------------------------------------------

1. Check a pseudopotential functional file

```
$ ls ../pseudo
README.md    Si.pbesol-n-rrkjus_psl.1.0.0.UPF
```

A UPF (unified pseudopotential functional) file used in this example can be found in ``../pseudo`` directory.
If you want, you can download UPF files of other elements from 
https://www.materialscloud.org/discover/sssp/table/efficiency.

2. Take a look at python scripts

Python scripts generating input scripts for QE are prepared in ``../tools``.

```
$ ls ../tools
mk_pwinput.py   pw_keys.py
```

``mk_pwinput.py`` is used to make input scripts of QE. 
(Users don't need to use ``pw_keys.py`` which is called from ``mk_pwinput.py``.)
One can check options of this code with "-h" option.

```
$ python ../tools/mk_pwinput.py -h
Usage: mk_pwinput.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename=FILENAME
                        structure file name [../Si.cif]
  --reciprocal_density=RECIPROCAL_DENSITY
                        kmesh density in the reciprocal space [20]
  --property=PROPERTY   property analyzed (scf, dos, bands, ...) [scf]
  --pseudo_dir=PSEUDO_DIR
                        directory of peudofunctions [../pseudo]
  --outdir=OUTDIR       output directory [./out]
  --ecutwfc=ECUTWFC     kinetic energy cutoff for wavefunctionswith the unit
                        of Ry [60.0]
  --frac_ecutrho=FRAC_ECUTRHO
                        kinetic energy cutoff for charge density and potential
                        [4.0]
  --conv_thr=CONV_THR   convergence threshold for selfconsistency [1e-6]
```

For example, a structure file can be given with "-f" or "--filename" option.

```
$ python ../tools/mk_pwinput.py -f ../Si.cif

```

If you want to know details of input parameters of pw.x of QE, see 
https://www.quantum-espresso.org/Doc/INPUT_PW.html.


Calcualtion process
--------------------

1. Self-consistent field (SCF) calculation

```
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property scf \
    --reciprocal_density 20 

pw.x < scf.in | tee scf.out
```

2. Non self-consistent field (NSCF) calculation

Calculate density of states (DOS) and partial DOS (PDOS):

```
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property dos \
    --reciprocal_density 40

pw.x < nscf_dos.in | tee nscf_dos.out
dos.x < dos.in | tee dos.out
projwfc.x < pdos.in | tee pdos.out
```

Calculate electronic band structure:

```
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property bands \
    --reciprocal_density 40 

bands.x < bands.in | tee bands.out
plotband.x < plotband.in
```

