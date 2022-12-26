## make an input file for phonon dispersion
python ../tools/mk_phband_input.py -f ../Si.cif

## calculate phonon dispersion
matdyn.x < band.in | tee band.out

## plot phonon dispersion
labels="G:X:U:K:G:L:W:X"
python ../tools/plot_phband.py \
    --file_band Si_band.freq \
    --symmetric_names "$labels"

