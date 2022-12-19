
#### make an input script
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property dos \
    --reciprocal_density 80

### perform non-SCF calculation 
### which calculate wavefunctions and eigenvalues with a fixed charge distribution
pw.x < nscf_dos.in | tee nscf_dos.out

### calculate DOS with the given eigenvalues
dos.x < dos.in | tee dos.out

### calculate partial DOS
projwfc.x < pdos.in | tee pdos.out

### calculate partial DOS for each orbital
sumpdos.x Si.pdos_*Si*s* > s_orbital.txt
sumpdos.x Si.pdos_*Si*p* > p_orbital.txt

### plot DOS
python ../tools/plot_dos.py --filename Si.dos
python ../tools/plot_pdos.py

