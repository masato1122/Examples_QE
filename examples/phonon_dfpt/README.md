Calculation of Phonon Dispersion
=================================

This example can be found [HERE](https://github.com/masato1122/Examples_QE/tree/main/examples/phonon_dfpt).

You can learn how to calculate phonon dispersion based on a density functional perturbation theory.

# Contents

* ``scripts`` : input scripts for simulations

* ``results`` : results: figures, output files, ...

* ``shell`` : shell scripts to run every calculations

# Calcution process

## 0. Copy input scripts

```
$ cp ./scripts/* ./
```

## 1. Run an SCF calculation

First of all, run the SCF calculation same as the calculation of electron band structure.

```
$ pw.x < scf.in | tee scf.out
``` 

## 2. Calcualte eigenvalues at $\Gamma$ point



