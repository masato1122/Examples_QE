#####################
## SCF calculation ##
#####################
pw.x < scf.in | tee scf.out

#####################
## force constants ##
#####################
ph.x < ph.in | tee ph.out
q2r.x < q2r.in | tee q2r.out

#######################
## phonon dispersion ##
#######################
## make an input file for phonon dispersion
python ../tools/mk_phband_input.py -f ../Si.cif

## calculate phonon dispersion
matdyn.x < band.in | tee band.out

## plot phonon dispersion
labels="G:X:U:K:G:L:W:X"
python ../tools/plot_phband.py \
    --file_band Si_band.freq \
    --symmetric_names "$labels"

#########
## DOS ##
#########
matdyn.x < dos.in | tee dos.out
python ../tools/plot_dos.py -f Si.dos

######################
## phonon vibration ##
######################
ph.x < ph_G.in | tee ph_G.out
dynmat.x < eigen_G.in | tee eigen_G.out

