Calculation of Phonon Properties with Finite-displacement approach
===================================================================

In this example, phonon dispersion is calculated with the finite displacement method, 
which may be more intuitive than the DFPT.

# Installation of Phonopy

Phonopy is a widely used software for lattice dynamics with a user-friendly python interface.
To in stall Phonopy, it is recommended to install python environment with Anaconda.

1. Download an installer from https://www.anaconda.com and install python with the installer.

2. Make a virtual environment in which Phonopy will be installed.

```
$ conda create -n py37 python3.7 nanotechnology
```

Activate the created environment
```
$ conda activate nanotechnology
```

If you want to delete the environment after the lecture, you can delete as below.

```
$ conda remove -n nanotechnology --all
```

3. Install Phonopy

```
$ conda install -c conda-forge phonopy
```

Make sure that ``phonopy`` command is available.

```
$ phonopy -h
```

# Phonon dispersion

An example to calculate phonon dispersion of Si can be found in ``./dispersion``.
Change directory with the following command and see explanations HERE: 
https://github.com/masato1122/Examples_QE/tree/main/examples/phonon_fd/dispersion.

```
$ cd ./dispersion
```

