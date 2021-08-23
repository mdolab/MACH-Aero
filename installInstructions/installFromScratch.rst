.. Instructions on how to set up a computer from scratch and be able to 
   run the aero_runs/aero_opt/as_runs/as_opt

.. _installFromScratch:


Installing MACH-Aero From Scratch
=================================
This tutorial is intended to be a step-by-step guide on how to set up the software needed to run ``MACH-Aero``.
The focus here is on installing common dependencies shared across the various packages.
A general description for installing packages within ``MACH-Aero`` is also provided, but please refer to the documentation site for each package for specific instructions.
This tutorial assumes that you have a working Linux distribution such as Ubuntu 18.04.

The following list what steps are needed. The instructions are divided into three parts

- `Third party packages`_
- `MDO Lab packages`_
- `Standard MDO Lab Build Procedure`_

Since MDO Lab packages depend heavily on third party tools and packages, it is generally good to start by compiling and testing them. 
Finally, an example ``.bashrc`` file is shown.

- `Example .bashrc`_

Third party packages
--------------------
To install, follow the instructions on :ref:`this page <installThirdPartyPackages>`.

MDO Lab packages
----------------
To install the MDO Lab packages clone each repository from `GitHub <https://github.com/mdolab>`_ and follow the installation instructions found in the documentation of each package.
Below, we give an overview of the general process, which consists of two parts.
The building step is required for Fortran/C-based codes, and not needed if the package is purely written in Python.
After this optional step, all packages must be installed as a Python package.

The packages needed are:

#. `baseClasses <https://github.com/mdolab/baseclasses>`_
#. `pySpline <https://github.com/mdolab/pyspline>`_
#. `pyGeo <https://github.com/mdolab/pygeo>`_
#. `IDWarp <https://github.com/mdolab/idwarp>`_
#. `ADflow <https://github.com/mdolab/adflow>`_
#. `pyOptSparse <https://github.com/mdolab/pyoptsparse>`_

Optional packages are:

#. `pyHyp <https://github.com/mdolab/pyhyp>`_
#. `multipoint <https://github.com/mdolab/multipoint>`_
#. `cgnsUtilities <https://github.com/mdolab/cgnsutilities>`_ 
#. `DAFoam <https://github.com/mdolab/dafoam>`_

Standard MDO Lab Build Procedure
--------------------------------

The following general instructions apply to all the packages and repos maintained by the MDO Lab. Note that the `Compilation`_ step is not required if the package is entirely written in Python.

Compilation
~~~~~~~~~~~
To start, find a configuration file close to your current setup in

:: 

    config/defaults

and copy it to ``config/config.mk``. For example

.. prompt:: bash

    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk

If you are a beginner user installing the packages on a Linux desktop, you should use the ``config.LINUX_GFORTRAN.mk`` versions of the configuration files.
The ``config.LINUX_INTEL.mk`` versions are usually used on HPC systems, in conjunction with Intel compilers.
Our codes can be successfully compiled on Linux with either ``ifort`` or ``gfortran``.

.. note::
   For Intel builds, the ``config.mk`` files are potentially out of date. 
   With new intel compilers, the actual mpi-wrapped compilers changed names. 
   Check out the compilers_, and modify the ``FF90`` and ``CC`` options in ``config.mk`` files as needed.

.. _compilers: https://software.intel.com/en-us/mpi-developer-reference-linux-compilation-commands

Once you have copied the config file, compile the module by running

.. prompt:: bash

    make

in the package's root directory.
If everything was successful, the following lines will be printed to the screen (near the end)::

   Testing if module <module_name> can be imported...
   Module <module_name> was successfully imported.

If you don't see this, it will be necessary to configure the build manually.
To configure manually, open ``config/config.mk`` and modify options as necessary.
Remember to type ``make clean`` to remove outdated build files, before building again.

Installation
~~~~~~~~~~~~
To install the Python package, type

.. prompt:: bash

   pip install .

If you are not using a virtual environment, you may need the ``--user`` flag to perform a user install.
If you plan to modify the source code, we recommend using the ``-e`` option, e.g. ``pip install -e .`` so that you do not need to install each time the code is modified.


Example ``.bashrc``
-------------------
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
