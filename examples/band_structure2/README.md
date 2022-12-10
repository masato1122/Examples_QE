Calculation of band structure with QuantumEspresso (QE)
========================================================

One can learn how to calculate electronic states such as band structure and density of states (DOS) 
with QuantumEspresso (QE) following the process described below.


A few things before starting the analysis 
------------------------------------------

# 1. Check a pseudopotential functional file

```
$ ls ../pseudo
README.md    Si.pbesol-n-rrkjus_psl.1.0.0.UPF
```

A UPF (unified pseudopotential functional) file used in this example can be found in ``../pseudo`` directory.
If you want, you can download UPF files of other elements from 
https://www.materialscloud.org/discover/sssp/table/efficiency.

2. Take a look at python scripts

Python scripts generating input scripts for QE are prepared in ``../tools``.

```
$ ls ../tools
mk_pwinput.py   pw_keys.py
```

``mk_pwinput.py`` is used to make input scripts of QE. 
(Users don't need to use ``pw_keys.py`` which is called from ``mk_pwinput.py``.)
One can check options of this code with "-h" option.

```
$ python ../tools/mk_pwinput.py -h
Usage: mk_pwinput.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename=FILENAME
                        structure file name [../Si.cif]
  --reciprocal_density=RECIPROCAL_DENSITY
                        kmesh density in the reciprocal space [20]
  --property=PROPERTY   property analyzed (scf, dos, bands, ...) [scf]
  --pseudo_dir=PSEUDO_DIR
                        directory of peudofunctions [../pseudo]
  --outdir=OUTDIR       output directory [./out]
  --ecutwfc=ECUTWFC     kinetic energy cutoff for wavefunctionswith the unit
                        of Ry [60.0]
  --frac_ecutrho=FRAC_ECUTRHO
                        kinetic energy cutoff for charge density and potential
                        [4.0]
  --conv_thr=CONV_THR   convergence threshold for selfconsistency [1e-6]
```

For example, a structure file can be given with "-f" or "--filename" option.

```
$ python ../tools/mk_pwinput.py -f ../Si.cif
```

If you want to know details of input parameters of pw.x of QE, see 
https://www.quantum-espresso.org/Doc/INPUT_PW.html.


Calcualtion process
--------------------

1. Self-consistent field (SCF) calculation

First of all, the charge distribution in the crystal structure is calculated with SCF method. 
The input script for the SCF calculation (``scf.in``) can be generated as below.

```
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property scf \
    --reciprocal_density 20 
```

Check ``scf.in`` is generated properly:

```
$ less scf.in
&CONTROL
  outdir = './out',
  prefix = 'Si',
  pseudo_dir = '../pseudo',
/
&SYSTEM
  ecutwfc = 60.0,
...
```

The SCF calculation can be conducted with ``pw.x`` (``pw.exe`` for Windows).

a) To print the result in the terminal and output in a file (``scf.out``):
```
pw.x < scf.in | tee scf.out
```

b) To output in a file only:
```
pw.x < scf.in > scf.out
```

Make sure that you have got ``./out`` directory after the calculation.

```
$ ls ./out
Si.save Si.xml
```

Wavefunctions (wfc\*.dat) obtained with the SCF calculation were saved in ``./out/Si.save``.


2. DOS with non self-consistent field (NSCF) calculation

Once wavefunctions, namely charge density, are obtained,
electronic states such as density of states (DOS) and band structure
can be calculated with the obtained wavefunctions.

Make an input script for DOS:

```
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property dos \
    --reciprocal_density 40
```

> **_NOTE:_** 
The k-mesh density, defined by "--reciprocal_density" option, for DOS (40)
is larger than that for the SCF calculation (20). 
In general, the SCF calculation is conducted with a coarser k-mesh 
because the SCF takes longer time.

Make sure that ``nscf_dos.in``, ``dos.in``, and ``pdos.in`` were generated with the above command.

```
$ ls
README.md  dos.in  nscf_dos.in  out  pdos.in  scf.in  scf.out
```

Run a NSCF calculation for DOS:

```
$ pw.x < nscf_dos.in | tee nscf_dos.out
```

You can find more wfc\*.dat files in ``./out/Si.save``.

```
$ ls ./out/Si.save
```

Calculte DOS with ``dos.x``:

```
dos.x < dos.in | tee dos.out
```

Partical DOS (PDOS) which represent DOS on each site (atom) can also be calculated with ``projwfc.x``:

```
projwfc.x < pdos.in | tee pdos.out
```

PDOS is saved in ``Si.pdos_atm***_wfc***`` files.


3. Band structure

Calculate electronic band structure:

```
python ../tools/mk_pwinput.py \
    --filename ../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property bands \
    --reciprocal_density 40 

bands.x < bands.in | tee bands.out
plotband.x < plotband.in
```

