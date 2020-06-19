.. Instructions on how to set up a computer from scratch and be able to 
   run the aero_runs/aero_opt/as_runs/as_opt

.. _installFromScratch:


Installing MDO Lab framework from scratch
=========================================


This tutorial is intended to be a step-by-step guide on how to set up the software needed to run MDO problems using the MDO Lab framework such as the `MACH-Aero-tutorial` repo.
It does not describe how to set up each software package rather just the steps needed.
This tutorial assumes that you have a working Linux distribution such as Ubuntu 18.04.

Installation steps
------------------
The following list what steps are needed. The instructions are divided into three parts

- `3rd party packages`_
- `MDO Lab packages`_
- `Standard MDO Lab Build Procedure`_

Since MDO Lab packages depend heavily on 3rd party tools and packages, it is generally good to start by compiling and testing them. 
Finally, an example ``.bashrc`` file is shown.

- `Example .bashrc`_

3rd party packages
******************
To install, follow the link for each package.

#. :ref:`install_prereq` 
#. :ref:`install_num_sci_py`
#. :ref:`install_petsc`
#. :ref:`install_mpi4py`
#. :ref:`install_petsc4py`
#. :ref:`install_cgns`

MDO Lab packages
****************
To install the MDO Lab packages clone each repository from `GitHub <https://github.com/mdolab>`_ and follow the installation instructions for each.
Some packages are pure Python packages so no compilation or setup is needed.
For the packages that do require compilation, you can follow the standard MDO Lab build procedure below.

The packages needed are:

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

If you are a beginner user installing the packages on a Linux desktop, you should use the ``config.LINUX_GFORTRAN.mk`` versions of the configuration files.
The ``config.LINUX_INTEL.mk`` versions are usually used on clusters, in conjunction with Intel compilers.
Our codes can be successfully compiled on Linux with either ``ifort`` or ``gfortran``.

Once you have copied the config file, compile the module by running::

    $ make

in the package's root directory.
If everything was successful, the following lines will be printed to the screen (near the end)::

   Testing if module <module_name> can be imported...
   Module <module_name> was successfully imported.

If you don't see this, it will be necessary to configure the build manually.
To configure manually, open ``config/config.mk`` and modify options as necessary.

.. NOTE::
   If you are using Python 2, please set ``PYTHON-CONFIG = python-config`` in the ``config/config.mk``.
   Also, make sure to specify the appropriate CGNS version.

Lastly, to build and install the Python interface, type::

   pip install .

If you are developing code, we recommend using the ``-e`` option, e.g. ``pip install -e .`` so that you do not need to install each time you modify the Python code.


Example ``.bashrc``
*******************
After installing the above software you should have something similar to the following somewhere in your ``~/.bashrc`` file

.. code-block:: bash

	# -- PETSc
	export PETSC_DIR=$HOME/packages/petsc-<x.y.z>
	export PETSC_ARCH=real-debug

	# -- OpenMPI Installation
	export MPI_INSTALL_DIR=$HOME/packages/openmpi-<x.y.z>/opt-gfortran
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
	export PATH=$MPI_INSTALL_DIR/bin:$PATH

	# -- CGNS
	export CGNS_HOME=$HOME/packages/CGNS-<x.y.z>/opt-gfortran
	export PATH=$PATH:$CGNS_HOME/bin
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

	# -- MDO Lab
	export PATH=$PATH:$HOME/repos/cgnsutilities/bin
	# export PYTHONPATH=$PYTHONPATH:$HOME/repos  # only if you are not installing all packages using pip
