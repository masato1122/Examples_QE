#!/bin/sh
WORKDIR=$(cd $(dirname $0); pwd)

num=1
for lat in 10.0 10.1 10.2 10.3 10.4; do

OFILE=scf.in
cat >$OFILE<<EOF
&CONTROL
    calculation='scf',
    outdir='./out',
    prefix='Si',
    pseudo_dir='../../pseudo',
    restart_mode='from_scratch',
/
&SYSTEM
    ibrav=2,
    celldm(1)=${lat}
    nat=2,
    ntyp=1,
    ecutwfc=60.0,
    ecutrho=720.0,
/
&ELECTRONS
    mixing_beta=0.7,
    conv_thr=1d-8,
/
ATOMIC_SPECIES
    Si 28.0855 Si.pbesol-n-rrkjus_psl.1.0.0.UPF
ATOMIC_POSITIONS (alat)
    Si  0.00  0.00  0.00
    Si  0.25  0.25  0.25
K_POINTS automatic
    4 4 4 1 1 1
EOF
pw.x < $OFILE | tee relax${num}.out
num=`expr $num + 1`

done

