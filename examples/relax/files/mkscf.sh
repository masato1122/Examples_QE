#!/bin/sh
WORKDIR=$(cd $(dirname $0); pwd)

#alat=10.2273

if [ $# -ge 1 ]; then
    alat=$1
else
    echo -n "Input file name: "
    read alat
fi

OFILE=scf.in
cat >$OFILE<<EOF
&CONTROL
  calculation = 'scf',
  outdir = './out',
  prefix = 'Si',
  pseudo_dir = '../pseudo',
  restart_mode = 'from_scratch',
/
&SYSTEM
  ecutwfc = 60.0,
  occupations = 'fixed',
  ibrav = 2,
  celldm(1) = $alat,
  nat = 2,
  ntyp = 1,
/
&ELECTRONS
  conv_thr = 1d-06,
  mixing_beta = 0.7
/
&IONS
/
&CELL
/
ATOMIC_SPECIES
  Si  28.0855 Si.pbesol-n-rrkjus_psl.1.0.0.UPF
ATOMIC_POSITIONS crystal
  Si 0.250000 0.250000 0.250000
  Si 0.500000 0.500000 0.500000
K_POINTS automatic
  4 4 4 0 0 0
EOF

