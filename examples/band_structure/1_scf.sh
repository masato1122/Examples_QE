
### make an input script
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property scf \
    --reciprocal_density 20 

### perform a SCF calculation to obtain charge distribution
pw.x < scf.in | tee scf.out

### calculate charge density
pp.x < pp.in | tee pp.out

