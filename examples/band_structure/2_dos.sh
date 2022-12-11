
### make an input script
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property dos \
    --reciprocal_density 40

### perform non-SCF calculation 
### which calculate wavefunctions and eigenvalues with a fixed charge distribution
pw.x < nscf_dos.in | tee nscf_dos.out

### calculate DOS with the given eigenvalues
dos.x < dos.in | tee dos.out

### calculate partial DOS
projwfc.x < pdos.in | tee pdos.out

### plot DOS
python ../tools/plot_dos.py --filename Si.dos
python ../tools/plot_pdos.py

