# Examples_QE

These example jobs for QuantumEspresso can be found in a [GitHub repository](https://github.com/masato1122/Examples_QE).

Examples in the above repository were created mainly for those who want to learn first-principles calculations.
Basic calculations such as DOS and band structure can be practiced.

Prerequisite
------------

To use python scripts prepared, the following libralies need to be installed in advance 
while the python scripts are not absolutely necessary.

* python
* pymatgen
* seekpath
* pyyaml

These python libralies can be installed with the following command.
If you have troubles, you can skip this part.

```
pip install pymatgen seekpath seekpath pyyaml
pip install pymatgen --upgrade
```

> **NOTE:** If you don't have python on your computer, you need to install python. Anaconda is a useful installer of a set of different python libraries: https://www.anaconda.com/products/distribution.


Installation of the examples
-----------------------------

```
git clone https://github.com/masato1122/Examples_QE.git
```

If you don't have ``git`` command, download a zip file and unzip under the directory you like.


Band structure
---------------

``./examples/band_structure`` contains an example to calculate the electron band structure of silicon.

Move to this directory in your terminal with ``cd ./Examples_QE/examples/band_structure`` and
follow the description written in 
https://github.com/masato1122/Examples_QE/tree/main/examples/band_structure.


Phonon dispersion
------------------

will be uploaded...

