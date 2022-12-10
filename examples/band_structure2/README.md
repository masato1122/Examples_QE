Calculation of band structure with QuantumEspresso (QE)
========================================================

A few thing before starting the analysis 
-----------------------------------------

1. Check if you have important files

```
$ ls ../pseudo
README.md    Si.pbesol-n-rrkjus_psl.1.0.0.UPF

$ ls ../tools
mk_pwinput.py   pw_keys.py
```

2. Take a look a python script

``mk_pwinput.py`` is used to make input scripts of QE.


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

