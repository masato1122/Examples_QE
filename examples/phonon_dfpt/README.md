Calculation of Phonon Dispersion
=================================

This example can be found [HERE](https://github.com/masato1122/Examples_QE/tree/main/examples/phonon_dfpt).

You can learn how to calculate phonon dispersion based on a density functional perturbation theory (DFPT).

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

```
$ ph.x < ph_G.in | tee ph_G.out
```

## 3. Calculate force constants

Firstly, interatomic force constants (IFCs) in reciprocal space are calculated with DFPT 
(this process takes a few minutes).
For the DFPT calculation, a rough k-mesh is used.

```
$ ph.x < ph.in | tee ph.out
```

Make sure that dynamical matrices (``Si.dyn*``) were obtained.

Then, IFCs are converted to those in the real space:

```
$ q2r.x < q2r.in | tee q2r.out
```

Make sure IFCs in real space (``Si.fc``) were obtained.


## 4. Calculate phonon dispersion

Calculate phonon dispersion with IFCs in reall space:

```
$ matdyn.x < band.in | tee band.out
```

> **NOTE:** ``asr`` parameter in ``band.in`` denotes acoustic sum rule. Because of numerical errors, IFCs do not satisfy the ASR: $\sum_{\mathbf{L}, j}C_{\alpha i, \beta j}(\matbf{R}_L) = 0$


Make sure that ``Si_band.{freq, freq.gp, modes}`` were obtained.
Plot the calculated phonon dispersion.

If python is available, phonon dispersion can be plotted with ``plot_phband.py``:

```
$ python ../tools/plot_phband.py --file_band Si_band.freq --symmetric_names "G:X:U:K:G:L:W:X"
```

## 5. Calculate phonon DOS

Calculate DOS with a fine k-mesh:

```
$ matdyn.x < dos.in | tee dos.out
```

