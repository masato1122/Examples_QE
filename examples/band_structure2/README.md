Calculation of band structure with QuantumEspresso (QE)
========================================================

You can learn how to calculate electronic states such as band structure and density of states (DOS) 
with QuantumEspresso (QE) following the process shown below.


A few thing before starting the analysis 
-----------------------------------------

1. Check if you have properly got important files.

```
$ ls ../pseudo
README.md    Si.pbesol-n-rrkjus_psl.1.0.0.UPF

$ ls ../tools
mk_pwinput.py   pw_keys.py

```

2. Take a look a python script.

``mk_pwinput.py`` is used to make input scripts of QE.
You can check what kind of options the code has with "-h" option.

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

For example, you can assign a structure file name with "-f" or "--filename" option.

```
$ python ../tools/mk_pwinput.py -f ../Si.cif

```



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

