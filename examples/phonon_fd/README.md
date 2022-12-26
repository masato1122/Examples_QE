Calculation of Phonon Dispersion with Finite-displacement
=========================================================

In this example, phonon dispersion is calculated with the finite displacement method, 
which may be more intuitive than the DFPT.

# Install Phonopy

Phonopy is a widely used software for lattice dynamics with a user-friendly python interface.

```
$ pip install phonopy
```

Make sure that ``phonopy`` command is available.

```
$ phonopy -h
```


# Calcute atomic forces in supercells with displacements

Please also read the official homepage: https://phonopy.github.io/phonopy/qe.html.

## Make a supercell from an input file of QE

```
$ cd ./1_forces
$ phonopy --qe -d --dim="2 2 2" -c ../../band_structure/scripts/scf.in
```

2x2x2 supercells are created as below. 

```
$ ls
phonopy_disp.yaml  supercell-001.in  supercell.in
```

* ``supercell.in``: pristine supercell structure
* ``supercell-***.in``: supercells in which an atom is slightly displaced
* ``phonpy_disp.yaml``: info of the displacements


## Prepare input scripts of QE

```
header=../scripts/header.in
cat ${header} supercell.in > pristine.in
for i in 001; do
    cat ${header} supercell-${i}.in > Si-${i}.in
done
```

``Si-001.in`` were generated.

Note that following parameters are set in ``header``.

```
tprnfor = .true.
nat = 16
```

``tprnfor`` is set to be ``.true.`` shen atomic forces are calculated and 
``nat`` is the number of atoms in a supercell.


## Calculate atomic forces with QE

```
for label in pristine Si-001; do
    pw.x < ${label}.in | tee ${label}.out
done
```

Make sure following files are generated.

```
$ ls *.out
pristine.out  Si-001.out
```

## Extract forces from output files

The following command create ``FORCE_SETS``.

```
$ phonopy -f Si-001.out
```

## Calculate force constants

```
$ cp ../scripts/band.conf ./
$ phonopy --qe -c ../scripts/scf.in -p band.conf
```


