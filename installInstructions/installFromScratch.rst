.. Instructions on how to set up a computer from scratch and be able to 
   run the aero_runs/aero_opt/as_runs/as_opt
   Author: Eirikur Jonsson (eirikurj@umich.edu)
    

.. _installFromScratch:


Installing MDO Lab framework from scratch
========================================


This tutorial is intended to be a step-by-step guide on how to set up 
the software needed to run MDO problems using the MDO Lab framework 
such as the mdo_tutorial repo. It does not describe how to set up each 
software package rather just the steps needed.
This tutorial assumes that you have a working Linux distribution such as
Ubuntu 12.04 or newer. Ubuntu 14.04 is assumed to be used here.


Installation steps
------------------
The following list what steps are needed. The instructions are divided 
in to two parts

- Installing `3rd party packages`_
- `MDOLab packages`_

Since MDO Lab packages depend heavily on 3rd party tools 
and packages it is generally good to start with that. Finally an 
example ``.bashrc`` file is shown.

- `Example .bashrc`_



3rd party packages
******************
To install follow the link for each package.

#. :ref:`install_prereq` 
#. :ref:`install_num_sci_py`
#. :ref:`install_petsc`
#. :ref:`install_mpi4py`
#. :ref:`install_petsc4py`
#. :ref:`install_cgns`

MDO Lab packages
***************
To install the MDO Lab packages clone each repository from `GitHub <https://github.com/mdolab>`_ and 
follow the installation instructions for each. Some packages are pure 
Python packages so no compilation or setup is needed. For the packages 
that do require compilation, copy one of the configuration files 
(e.g., ``config.LINUX_GFORTRAN.mk``) from the package's ``config/defaults`` 
directory to the package's ``config`` directory and rename it ``config.mk``. 
Then use the command ``make`` (in the package's root directory) to compile. 
If you are a beginner user installing the packages on a linux desktop, you 
you should use the ``config.LINUX_GFORTRAN`` versions of the configuration 
files. The ``config.LINUX_INTEL`` versions are usually used on clusters.
The installation of the TACS package is a little more involved, so follow 
the instructions in its `README.md` file.

We recommend that you clone the repos to a ``repos`` folder under your home 
folder ``/home/<your username>/repos``

In order for the MDO framework to find python modules properly its 
necessary to set the ``PYTHONPATH`` environmental variable in your 
``.bashrc`` file

.. code-block:: bash

	#filename .bashrc
	export PYTHONPATH=$PYTHONPATH:$HOME/repos/

The packages needed:

#. `baseClasses <https://github.com/mdolab/baseclasses/>`_
#. `pySpline <https://github.com/mdolab/pyspline/>`_
#. `pyGeo <https://github.com/mdolab/pygeo/>`_
#. `pyWarp <https://github.com/mdolab/pywarp/>`_
#. `IDWarp <https://github.com/mdolab/idwarp/>`_
#. `ADflow <https://github.com/mdolab/adflow/>`_
#. `pyOptSparse <https://github.com/mdolab/pyoptsparse>`_
#. `pyHyp <https://github.com/mdolab/pyhyp>`_
#. `repostate <https://github.com/mdolab/repostate/>`_
#. `multipoint <https://github.com/mdolab/multipoint/>`_ (for doing multipoint optimization)
#. TACS (for structural/aerostructural)
#. Tripan (for aero/aerostructural using panel methods)

To install SNOPT within pyOptSparse, clone the repository ``mdolabexternal``, then copy the contents of ``mdolabexternal/SNOPT`` to ``pyoptsparse/pyoptsparse/pySNOPT/source`` before compiling pyoptsparse.


Example .bashrc
***************
After installing the above software you should have a ``.bashrc`` file 
that is close to the example shown here below

.. code-block:: bash

	# filename: .bashrc

	# MDO Lab related variables
	export PYTHONPATH=$PYTHONPATH:$HOME/repos/

	# Paths for external packages
	export PATH=$PATH:$HOME/repos/tacs/extern/f5totec
	export PATH=$PATH:$HOME/repos/cgnsutilities/bin

	# PETSc ARCH and DIR
	export PETSC_DIR=$HOME/packages/petsc-3.7.7
	export PETSC_ARCH=real-debug

	# Library Path for MPI
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib

	# Path for MPI -- configuration with MPI
	export PATH=$PETSC_DIR/$PETSC_ARCH/bin:$PATH
	export PATH=$PETSC_DIR/$PETSC_ARCH/include:$PATH

	# LD Library paths
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/repos/pyoptsparse/pyoptsparse/pyIPOPT/Ipopt/lib
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/cgnslib_3.2.1/src

