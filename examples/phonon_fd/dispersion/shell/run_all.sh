prefix=Si

file_scf=../scripts/Si.in

#### 1. make a supercell
phonopy --qe -d --dim="2 2 2" -c $file_scf --amplitude 0.01

### 2. prepare files to calculate atomic forces with QE
header=../scripts/header.in
cat ${header} supercell.in > pristine.in
for i in 001; do
    cat ${header} supercell-${i}.in > ${prefix}-${i}.in
done

### 3. calculate forces with QE
cp ./results/Si-001.out ./
##for label in pristine Si-001; do
#for label in Si-001; do
#    pw.x < ${label}.in | tee ${label}.out
#done

### 4. extract atomic forces
phonopy -f Si-001.out

### 5. calculate phonon dispersion
cp ../scripts/band.conf ./
phonopy --qe -c $file_scf -p band.conf

### 6. plot phonon dispersion
python ../tools/plot_phband_phonopy.py

