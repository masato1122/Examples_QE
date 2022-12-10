Calculation process
===================

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

