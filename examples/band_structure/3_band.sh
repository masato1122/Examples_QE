
## make an input script
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property bands

## perform NSCF calculation
pw.x < nscf_bands.in | tee nscf_bands.out

## calculate band structure
bands.x < bands.in | tee bands.out

## plot band structure
plotband.x < plotband.in

python ../tools/plot_band.py \
    -f Si.band.gnu -n 8 \
    --symmetry_names "G:X:U:K:G:L:W:X"

