.. Instructions on how to set up a computer from scratch and be able to 
   run the aero_runs/aero_opt/as_runs/as_opt

.. _installFromScratch:


Installing MDO Lab framework from scratch
=========================================


This tutorial is intended to be a step-by-step guide on how to set up 
the software needed to run MDO problems using the MDO Lab framework 
such as the mdo_tutorial repo. It does not describe how to set up each 
software package rather just the steps needed.
This tutorial assumes that you have a working Linux distribution such as
Ubuntu 12.04 or newer. Ubuntu 14.04 is assumed to be used here.


Installation steps
------------------
The following list what steps are needed. The instructions are divided 
in to four parts

- `3rd party packages`_
- `MDO Lab packages`_
- `Standard MDO Lab Build Procedure`_
- `Environment Setup`_

Since MDO Lab packages depend heavily on 3rd party tools 
and packages it is generally good to start by compiling and testing them. 
Finally, an example ``.bashrc`` file is shown.

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
****************
To install the MDO Lab packages clone each repository from `GitHub <https://github.com/mdolab>`_ and 
follow the installation instructions for each. Some packages are pure 
Python packages so no compilation or setup is needed. For the packages 
that do require compilation, you can follow the standard MDO Lab build procedure below.

The packages needed:

#. `baseClasses <https://github.com/mdolab/baseclasses/>`_
#. `pySpline <https://github.com/mdolab/pyspline/>`_
#. `pyGeo <https://github.com/mdolab/pygeo/>`_
#. `pyWarp <https://github.com/mdolab/pywarp/>`_
#. `IDWarp <https://github.com/mdolab/idwarp/>`_
#. `ADflow <https://github.com/mdolab/adflow/>`_
#. `pyOptSparse <https://github.com/mdolab/pyoptsparse>`_
#. `pyHyp <https://github.com/mdolab/pyhyp>`_
#. `multipoint <https://github.com/mdolab/multipoint/>`_ (for doing multipoint optimization)

Standard MDO Lab Build Procedure
********************************

To start, find a configuration file close to your current setup in::

    $ config/defaults

and copy it to ''config/config.mk''. For example::

    $ cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk

If you are a beginner user installing the packages on a linux desktop, 
you should use the ``config.LINUX_GFORTRAN.mk`` versions of the configuration 
files. The ``config.LINUX_INTEL.mk`` versions are usually used on clusters.
ADflow has been successfully compiled on LINUX with either
ifort or gfortran.

Once you have copied the config file, compile the module by running::

    $ make

in the package's root directory.
If everything was successful, the following lines will be printed to
the screen (near the end)::

   Testing if module <module_name> can be imported...
   Module <module_name> was successfully imported.

If you don't see this, it will be necessary to configure the build
manually. To configure manually, open ``config/config.mk`` and modify options as necessary.

The installation of the TACS package is a little more involved, so follow 
the instructions in its `README.md` file.

Environment Setup
*****************

We recommend that you clone the repos to a ``repos`` folder under your home 
folder ``/home/<your username>/repos``

In order for the MDO framework to find python modules properly its 
necessary to set the ``PYTHONPATH`` environmental variable in your 
``.bashrc`` file

.. code-block:: bash

	#filename .bashrc
	export PYTHONPATH=$PYTHONPATH:$HOME/repos/



Example .bashrc
***************
After installing the above software you should have a ``.bashrc`` file 
that is close to the example shown here below

.. code-block:: bash

	# filename: .bashrc

	# MDO Lab related variables
	export PYTHONPATH=$PYTHONPATH:$HOME/repos/

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

