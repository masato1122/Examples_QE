python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property bands

pw.x < nscf_bands.in | tee nscf_bands.out
bands.x < bands.in | tee bands.out
plotband.x < plotband.in

python ../tools/plot_band.py -f Si.band.gnu -n 8


