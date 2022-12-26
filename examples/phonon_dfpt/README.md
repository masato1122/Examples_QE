Calculation of Phonon Dispersion
=================================

This example can be found [HERE](https://github.com/masato1122/Examples_QE/tree/main/examples/phonon_dfpt).

With this example, you can learn how to calculate phonon dispersion based on a density functional perturbation theory (DFPT).

# Contents

* ``scripts`` : input scripts for simulations

* ``results`` : results: figures, output files, ...

* ``shell`` : shell scripts to run every calculations

# Calcution process

## 1. Copy input scripts

```
$ cp ./scripts/* ./
```

## 2. Run an SCF calculation

First of all, run the SCF calculation same as the calculation of electron band structure.

```
$ pw.x < scf.in | tee scf.out
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

If python is available, the input script ``band.in`` can be generated with the following command.

```
$ python ../tools/mk_phband_input.py -f ../Si.cif
```

Calculate phonon dispersion with IFCs in reall space:

```
$ matdyn.x < band.in | tee band.out
```

> **NOTE:** ``asr`` parameter in ``band.in`` denotes acoustic sum rule. \
Because of numerical errors, IFCs do not strictly satisfy the ASR: $\sum_{\mathbf{L}, j} C_{\alpha i, \beta j}(\mathbf{R}_L) = 0$, where $C$ is IFC, $\alpha, \beta$ denote the atomic site, $i, j$ denote the direction, and $\mathbf{R_L}$ denotes the cell.


Make sure that ``Si_band.{freq, freq.gp, modes}`` were obtained.
Plot the calculated phonon dispersion.

If python is available, phonon dispersion can be plotted with ``plot_phband.py``:

```
$ python ../tools/plot_phband.py --file_band Si_band.freq --symmetric_names "G:X:U:K:G:L:W:X"
```

## 5. Calculate phonon DOS

Calculate phonon DOS with a fine k-mesh:

```
$ matdyn.x < dos.in | tee dos.out
```

Plot the result:

```
$ python ../tools/plot_dos.py -f Si.dos
```

The above process can be run with ``run_all.sh``:

```
$ cp ./shell/run_all.sh ./
$ sh run_all.sh
```

## 6. Visualize of phonon modes at $\Gamma$ point

Install ``XCrySDen`` from http://www.xcrysden.org/Download.html.

```
$ ph.x < ph_G.in | tee ph_G.out
$ cat ph_G.out | grep freq
```

Six eigenvalues, triple degenerate acoustic and optical modes, are obtained.
To make the frequency of the acoustic modes zero, the structure optimization and more accurate calculations 
(large k-mesh, larger cutoff energy, ...) are required.
Make sure that the dynamic matrix at $\Gamma$ point (``Si_G.dyn``) was obtained.

Calculate eigenvectors with the obtained dynamical matrix.

```
$ dynmat.x < eigen_G.in | tee eigen_G.out
```

Make sure that ``eigen_G.axsf`` was obtained.

1. Run XCrysDen, then select [File] => [Open Structure] => [Open AXSF].

2. Select one of the six displace vectors.

3. Select [Hide] => [Display] => [Forces].

4. To modify the length of arrows, select [Modify] => [Force Settings] and modify "Length Factor".





