#!/bin/sh
#PBS -q default
#PBS -l nodes=1:ppn=24
#PBS -j oe
#PBS -N phonon

export LANG=C
export OMP_NUM_THREADS=1
cd $PBS_O_WORKDIR
rm phonon.o*

nprocs=24

MPIRUN=/opt/intel/oneapi/mpi/2021.6.0/bin/mpirun

#####################
## SCF calculation ##
#####################
$MPIRUN -np $nprocs pw.x < scf.in | tee scf.out

#####################
## force constants ##
#####################
$MPIRUN -np $nprocs ph.x < ph.in | tee ph.out
$MPIRUN -np $nprocs q2r.x < q2r.in | tee q2r.out

#######################
## phonon dispersion ##
#######################
## make an input file for phonon dispersion
python ../tools/mk_phband_input.py -f ../Si.cif

## calculate phonon dispersion
$MPIRUN -np $nprocs matdyn.x < band.in | tee band.out

## plot phonon dispersion
labels="G:X:U:K:G:L:W:X"
python ../tools/plot_phband.py \
    --file_band Si_band.freq \
    --symmetric_names "$labels"

#########
## DOS ##
#########
$MPIRUN -np $nprocs matdyn.x < dos.in | tee dos.out
$MPIRUN -np $nprocs python ../tools/plot_dos.py -f Si.dos

######################
## phonon vibration ##
######################
#$MPIRUN -np $nprocs ph.x < ph_G.in | tee ph_G.out
#matdyn.x < eigen_G.in | tee eigen_G.out

