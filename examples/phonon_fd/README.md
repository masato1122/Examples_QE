Calculation of Phonon Dispersion with Finite-displacement
=========================================================

# Install Phonopy

```
$ pip install phonopy
```

# Calcute atomic forces in supercells with displacements

## Make a supercell from an input file of QE

```
$ cd ./1_forces
$ phonopy --qe -d --dim="2 2 2" -c ../../band_structure/scripts/scf.in
```

2x2x2 supercells are created. 
Make sure that following files were generated.

```
$ ls
phonopy_disp.yaml  supercell-001.in  supercell.in
```

* ``supercell.in``: pristine supercell structure
* ``supercell-***.in``: supercells in which an atom is slightly displaced
* ``phonpy_disp.yaml``: info of the displaced structures


## Prepare input scripts of QE

```
$ header=../scripts/header.in
$ cat ${header} supercell.in >| pristine.in
$ for i in 001; do
$     cat ${header} supercell-${i}.in >| Si-${i}.in
$ done
```

``Si-***.in`` were generated.

Note that following parameters are set in ``header``.

```
tprnfor = .true.
nat = 16
```

## Calculate atomic forces with QE

```
$ for label in pristine Si-001; do
$    pw.x < ${label}.in | tee ${label}.out
$ done
```

Make sure following files are generated.

```
$ ls *.out
pristine.out  Si-001.out
```

## Extract displacements and forces from output files

The following command create ``FORCE_SETS``.

```
$ phonopy -f Si-001.out
```

## Calculate force constants

```
$ phonopy --qe -c ../scripts/scf.in -p band.conf
```


## Reference

* https://phonopy.github.io/phonopy/qe.html


