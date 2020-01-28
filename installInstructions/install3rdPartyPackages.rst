.. Installation instruction on how to set up external packages need to
   run the MDOlab code.

.. _install3rdPartyPackages:

3rd Party Packages
==================


Before compiling **any** of the MDOlab codes, it is **HIGHLY
RECOMMENDED** that you install the following packages below.


.. _install_prereq:

Common Prerequisites
--------------------
If they're not available already, common prerequisites can be installed directly from a Debian repository::

   sudo apt-get install python-dev gfortran valgrind cmake

The packages are required by many of the packages installed later.
On a cluster, check the output of ``module avail`` to see what has already been installed.
They can also be installed locally, but they are common enough that a system install is acceptable.


C and Fortran Based Packages
----------------------------
These packages have minimal dependencies and should be installed first, in the order listed here.
These source code for these packages are often downloaded and installed to ``$HOME/packages/$PACKAGE_NAME``,
which will be adopted as convention for the instructions here.
The environment is adapted for each package by modifying ``$HOME/.bashrc`` or equivalent.


`OpenMPI <http://www.open-mpi.org/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   The version(s) of OpenMPI tested to work with MDOlab tools is ``1.10.7``

   OpenMPI depends only on a C/Fortran compiler, such as ``gcc/gfortran`` or ``icc/ifort``.

.. NOTE::
   On a cluster, the system administrator will have already compiled various versions of MPI on the system already.
   Do not build/install OpenMPI in this case.

.. NOTE::
   OpenMPI may also be installed by PETSc (see below), but a separate installation as described here is preferred.

Download and unpack the source directory, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget https://download.open-mpi.org/release/open-mpi/v1.10/openmpi-1.10.7.tar.gz
   tar -xvaf openmpi-1.10.7.tar.gz
   cd openmpi-1.10.7

Add the following lines to ``$HOME/.bashrc`` and ``source`` it:

.. code-block:: bash

   # -- OpenMPI Installation
   export MPI_INSTALL_DIR=$HOME/packages/openmpi-1.10.7/opt-gfortran
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
   export PATH=$MPI_INSTALL_DIR/bin:$PATH

Finally, configure and build the package:

.. code-block:: bash

   export CC=icc CXX=icpc F77=ifort FC=ifort    # Only necessary if using non-GCC compiler
   ./configure --prefix=$MPI_INSTALL_DIR
   make all install

To verify that paths are as expected run

.. code-block:: bash

   which mpicc
   echo $MPI_INSTALL_DIR/bin/mpicc

The above should print out the same path for both.

.. _install_petsc:

`PETSc <http://www.mcs.anl.gov/petsc/index.html>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   The version(s) of PETSc tested to work with MDOlab tools is ``3.7.7``.
   Use other versions at your own risk.

   PETSc depends on OpenMPI, a C/Fortran compiler, and valgrind, and it requires cmake to build.

PETSc, the Portable Extensible Toolkit for Scientific Computation is a
comprehensive library for helping solve large scale PDE problems.
PETSc is used by :ref:`adflow`, :ref:`pywarp`, :ref:`pyhyp`, Tripan and pyAeroStruct.

Download and unpack the source directory, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.7.7.tar.gz
   tar -xvaf petsc-3.7.7.tar.gz
   cd petsc-3.7.7

The lite version of the package is smaller but contains no documentation.
Next, configure your environment for PETSc by adding the following lines to your ``$HOME/.bashrc`` and ``source``-ing it:

.. code-block:: bash

   # -- PETSc Installation
   export PETSC_ARCH=real-debug
   export PETSC_DIR=$HOME/packages/petsc-3.7.7/


The ``PETSC_ARCH`` variable is any user-specified string.
It should be set to something representative of the actual architecture.

The next step is to configure PETSc.
There are a huge number and variety of options.
To get a list of all available options run::

   ./configure --help

The relevant configuration options for MDOlab codes are:

1. **Debugging**: To compile without debugging use the switch::

      --with-debugging=no

   It is HIGHLY recommended to use debugging until you are ready to
   perform production runs use a debug build.

2. **BLAS and LAPACK**: Linear algebra packages.

   If you do not have BLAS and LAPACK installed you can include
   the following in the configure::

      --download-fblaslapack=1

3. **METIS and ParMETIS**: partitioning packages

   If you do not have METIS and ParMETIS installed, include the following line::

      --download-metis=yes --download-parmetis=yes

4. **Other**:
   Various options are also required::

      --with-shared-libraries --download-superlu_dist=yes --with-fortran-interfaces=1

   Specifically, :ref:`pyWarp` uses the ``superlu_dist``.

There are many other options, and they enable linking and/or downloading to a variety of other packages.
Putting these options together, some complete examples of configuring PETSc are:

1. Standard debug build (``$PETSC_ARCH=real-debug``):

.. code-block:: bash

   ./configure --PETSC_ARCH=$PETSC_ARCH --with-scalar-type=real --with-debugging=yes --with-mpi-dir=$MPI_INSTALL_DIR \
      --download-fblaslapack=yes --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
      --with-shared-libraries=yes --with-fortran-interfaces=yes

2. Debug complex build (``$PETSC_ARCH=complex-debug``):

.. code-block:: bash

   ./configure --PETSC_ARCH=$PETSC_ARCH --with-scalar-type=complex --with-debugging=yes --with-mpi-dir=$MPI_INSTALL_DIR \
      --download-fblaslapack=yes --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
      --with-shared-libraries=yes --with-fortran-interfaces=yes

3. Optimized real build on a cluster with existing MPI (``$PETSC_ARCH=real-opt``). (For production runs on a cluster you *MUST* use an optimized build.):

.. code-block:: bash

   ./configure --with-shared-libraries --download-superlu_dist --download-parmetis=yes --download-metis=yes \
      --with-fortran-interfaces=1 --with-debugging=no --with-scalar-type=real --PETSC_ARCH=$PETSC_ARCH

4. Optimized build, referencing an existing parmetis/metis and hdf5 installation
   (using the ``$HOME/opt`` installation directory convention):

.. code-block:: bash

   ./configure --prefix=/home/rchaud/opt/petsc/3.7.7/hdf5-1.8.21/OpenMPI-1.10.7/GCC-7.3.0 \
      --with-shared-libraries --PETSC_ARCH=linux-gnu-real-opt --with-debugging=no \
      --download-fblaslapack=1 --download-superlu_dist=1 \
         --with-metis    --with-metis-dir=/home/rchaud/opt/parmetis/4.0.3/OpenMPI-1.10.7/GCC-7.3.0 \
      --with-parmetis --with-parmetis-dir=/home/rchaud/opt/parmetis/4.0.3/OpenMPI-1.10.7/GCC-7.3.0 \
      --with-hdf5 --with-hdf5-dir=/home/rchaud/opt/hdf5/1.8.21/OpenMPI-1.10.7/GCC-7.3.0 \
      --with-fortran-interfaces

5. Debug build which downloads and installs OpenMPI also (not recommended):

.. code-block:: bash

   ./configure --with-shared-libraries --download-superlu_dist --download-parmetis --download-metis \
      --with-fortran-interfaces --with-debugging=yes --with-scalar-type=real --download-fblaslapack \
      --PETSC_ARCH=$PETSC_ARCH --download-openmpi --with-cc=gcc --with-cxx=g++ --with-fc=gfortran

After the configuration step, PETSc must be built. This is accomplished with the command provided at the end of the configure script. It will look something like below (the PETSc version should be consistent with the version being installed.)::
   
   make PETSC_DIR=$HOME/packages/petsc-3.7.7 PETSC_ARCH=$PETSC_ARCH all

After build, follow the the command provided at the end of the print out to test the functionality. It will look something like below::

    make PETSC_DIR=$HOME/packages/petsc-3.7.7 PETSC_ARCH=$PETSC_ARCH test

.. NOTE::
   If your PETSc is not able to find mpi, try::

   1. Add ``--with-mpi-dir=$MPI_INSTALL_DIR`` when you configure PETSc

   2. Check your LD_LIBRARY_PATH order. If you have pytecplot, try moving tecplot LD_LIBRARY_PATH to the last.


.. _install_cgns:

`CGNS Library <http://cgns.github.io/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   The version(s) of CGNS tested to work with MDOlab tools is ``3.3.0`` and ``3.2.1``.

   CGNS depends on a C/Fortran compiler and requires cmake to build.

The CGNS library is used to provide CGNS functionality for :ref:`adflow`,
:ref:`pywarp`, and :ref:`pyhyp`.

.. WARNING::
   The 3.2.1 version fortran include file contains an error. After
   untaring, manually edit the cgnslib_f.h.in file in the ``src``
   directory and remove all the comment lines at the beginning of the
   file starting with c. This is fixed in subsequent versions.

.. NOTE::
   CGNS now supports two output types: HDF5 and
   the Advanced Data Format (ADF) format. While HDF5 is the
   officially supported format, its compatability with other tools is sparse.
   Therefore, for using MDOlab codes, the ADF format is recommended.
   Installing and linking HDF5 is therefore not recommended.

Download and unpack the source directory, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget https://github.com/CGNS/CGNS/archive/v3.2.1.tar.gz
   tar -xvaf v3.2.1.tar.gz
   cd CGNS-3.2.1

Next, configure your environment for CGNS by adding the following lines to your ``$HOME/.bashrc`` and ``source``-ing it:

.. code-block:: bash

   # -- CGNS
   export CGNS_HOME=$HOME/packages/CGNS-3.2.1/opt-gfortran
   export PATH=$PATH:$CGNS_HOME/bin
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

Make a ``build`` directory, and call cmake from there to configure the package:

.. code-block:: bash

   mkdir build       # If it exists from a previous build, remove it first
   cd build
   cmake .. -DCGNS_ENABLE_FORTRAN=1 -DCMAKE_INSTALL_PREFIX=$CGNS_HOME -DCGNS_BUILD_CGNSTOOLS=1

Finally, build and install::

   make all install

Now, for pyHyp, ADflow, pyWarp and cgnsUtilities, the required include
flags and linking flags will be:

.. code-block:: bash

   CGNS_INCLUDE_FLAGS=-I$(CGNS_HOME)/include
   CGNS_LINKER_FLAGS=-L$(CGNS_HOME)/lib -lcgns

.. NOTE::
   **Optional**: To build the CGNS tools to view and edit CGNS files manually,
   toggle the CGNS_BUILD_CGNSTOOLS option. To enable this option you may need
   to install the following packages::

   $ sudo apt-get install libxmu-dev libxi-dev
   
   CGNS library sometimes complains about missing includes and libraries
   Most of the time this is either Tk/TCL or OpenGL. This can be solved by
   installing the following packages. Note that the version of these
   libraries might be different on your machine ::

      $ sudo apt-get install freeglut3
      $ sudo apt-get install tk8.6-dev
      # If needed
      $ sudo apt-get install freeglut3-dev

   **Optional**: If you compiled with the CGNS_BUILD_CGNSTOOLS flag ON you
   either need to add the binary path to your PATH environmental variable or
   you can install the binaries system wide. To do so issue the command::

   $ sudo make install

Python Packages
---------------

.. IMPORTANT::
   MDOlab tools have been tested to work with python2.
   The MDOlab is in the process of migrating to python3;
   support for python2 will be dropped before python2 EOL (January 2020).

In this guide, python packages are installed using ``pip``.
Other methods, such as from source or using ``conda``, will also work.
Local installations (with ``--user``) are also recommended but not required.
If pip is not available, install it using:

.. code-block:: bash

   cd $HOME/PACKAGES
   wget https://bootstrap.pypa.io/get-pip.py
   python get-pip.py --user

When installing the same package multiple times with different dependencies,
for example ``petsc4py`` with different petsc builds, the pip cache can become incorrect.
Therefore, we recommend the ``--no-cache`` flag when installing python packages with pip.

.. _install_num_sci_py:

.. _install_numpy:

`Numpy <https://numpy.org/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   Version ``1.13.3`` and ``1.15.4`` of numpy or f2py do **NOT** work.
   See :ref:`working_stacks` for numpy versions that have been tested.
   The version(s) of numpy used here is ``1.16.4``.

Numpy is required for all MDOlab packages.
It is installed with::

   pip install numpy==1.16.4 --user --no-cache

`Scipy <http://scipy.org/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. IMPORTANT::
   The version(s) of scipy tested to work with MDOlab tools is ``1.2.2``.

   Scipy depends on numpy

Scipy is required for several packages including :ref:`pyoptsparse`, :ref:`pygeo` and certain
functionality in pytacs and :ref:`pyspline`.
It is installed with::

   pip install --user --no-cache scipy==1.2.2

.. note::
   On a cluster, most likely numpy and scipy will already be
   installed. Unless the version is invalid, use the system-provided installation.

.. _install_mpi4py:

`mpi4py <http://mpi4py.scipy.org/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. IMPORTANT::
   The version(s) of mpi4py tested to work with MDOlab tools is 3.0.2.

   mpi4py depends on OpenMPI.

   It is recommended that the OpenMPI version matches with the mpi4py version.

mpi4py is the Python wrapper for MPI. This is required for
**all** parallel MDOlab codes.
It is installed with::

   pip install --user --no-cache mpi4py==3.0.2

.. NOTE::
   Some function usages have changed in newer versions of mpi4py. Check the `release <https://github.com/mpi4py/mpi4py/blob/master/CHANGES.rst>`_ to see the modifications that might be requried in the code.


.. _install_petsc4py:

`petsc4py <https://bitbucket.org/petsc/petsc4py/downloads>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. IMPORTANT::
   The MAJOR.MINOR version of petsc4py **MUST** match the MAJOR.MINOR version of petsc,
   for example petsc 3.7.7 will only work with petsc4py 3.7.X.
   In practice, this means you must request a specific version of petsc4py.

   The version(s) of petsc4py tested to work with MDOlab tools is 3.7.0, built against petsc version 3.7.7.

   petsc4py depends on petsc and its dependencies.

``petsc4py`` is the Python wrapper for PETSc. Strictly speaking, this
is only required for the coupled solvers in pyAeroStruct. However, it
*is* necessary if you want to use any of PETSc command-line options
such as -log-summary.

If you want to make developments or multiple PETSc architectures are needed, you should install petsc4py manually, which decribed in **Advanced install**.
Manually installing provide you useful run tests.

If you know you will **only** need real PETSc architecture, you can use pip.

Simple install with pip
***********************

It is installed with::

   pip install --user --no-cache petsc4py==3.7.0

Advanced install (Multiple PETSc architectures needed)
******************************************************
.. WARNING:: 
   You must compile a unique petsc4py install for each PETSc architecture.

`Download <https://bitbucket.org/petsc/petsc4py/downloads>`__ the source code and
extract the latest version (the major version should be consistent with 
the PETSc version installed, i.e., 3.7.0 here)::

$ tar -xzf petsc4py-3.7.0.tar.gz

.. note::
   For petsc4py 3.7.0, before installing::

   $ export LDSHARED=-shared.

From the petsc4py-3.7.0 directory do a user-space install::

$ python setup.py install --user

This will install the package to the ``.local`` directory in your home
directory which is suitable for both desktop and cluster accounts.
You may seen an error warning related to ``python-mpi``, but this 
should not be a problem. 

   
**IF THERE IS AN EXISTING** ``build`` **DIRECTORY IT MUST BE
FORCIBLY REMOVED** (``rm -fr build``) **BEFORE DOING ANOTHER ARCHITECTURE
INSTALL**. To install with a different architecture change the
``PETSC_ARCH`` variable in your ``.bashrc`` file and source it, or just type in your terminal to overwrite the old ``PETSC_ARCH``::

   export PETSC_ARCH=<new_architecture>

Then install the package::

   $ python setup.py install --user




.. _working_stacks:

Working Stacks
--------------
This section includes the stacks successfully used by MDOlab members.
This section is a work in progress.

.. First entry (18.04) This is Ross S. Chaudhry's configuration on Xeon desktop, used to build this guide. Added to the table July 2019
   Second entry (16.04) is Eirikur's configuration. Added to the table July 2019


.. list-table::
   :widths: 14 12 8 9 9 7 9 9 7 9 9
   :header-rows: 1

   *  - OS
      - Compiler
      - cmake
      - OpenMPI
      - PETSc
      - CGNS
      - python
      - numpy
      - scipy
      - mpi4py
      - petsc4py

   *  - Ubuntu 18.04
      - GCC 7.3.0
      - 3.14.5
      - 1.10.7
      - 3.7.7
      - 3.2.1
      - 2.7.15+
      - 1.16.4
      - 1.2.2
      - 3.0.2
      - 3.7.0

   *  - Ubuntu 16.04
      - GCC 5.4.0
      - 3.5.1
      - 1.10.7
      - 3.7.7
      - 3.2.1
      - 2.7.12
      - 1.11.0
      - 1.1.0
      - 1.3.1
      - 3.7.0

Other Methods and Notes
-----------------------

The MDOlab tools can be configured to write HDF5 files,
by building CGNS with hdf5 compatability.
Generally, there is no need for this functionality and it increases the build complexity.
However, it has been done in the past with ``hdf5 1.8.21``.

The build examples described here are all installed *locally* (eg. ``$HOME/...``)
rather than system-wide (eg. ``/usr/local/...``).
Local installations are generally preferred.
Installing packages system-wide requires root access, which is an increased security risk when downloading packages from the internet.
Also, it is typically easier to uninstall packages or otherwise revert changes made at a local level.
Finally, local installations are required when running on a cluster environment.

The build and installation paradigm demonstrated here puts
source code, build files, and installed packages all in ``$HOME/packages``.
Another common convention is to use ``$HOME/src`` for source code and building,
and ``$HOME/opt`` for installed packages.
This separation adds a level of complexity but is more extensible if multiple package versions/installations are going to be used.

When configuring your environment, the examples shown here set environment variables, ``$PATH``, and ``$LD_LIBRARY_PATH`` in ``.bashrc``.
If multiple versions and dependencies are being used simultaneously,
for example on a cluster, the paradigm of `environment modules <http://modules.sourceforge.net>` is often used (eg. ``module use petsc``).
A module file is simply a text file containing lines such as::

   append-path PATH /home/rchaud/opt/petsc/3.7.7/OpenMPI-1.10.7/GCC-7.3.0/bin

MDOlab tools can be used by configuring your environment with either ``.bashrc`` or environment modules, or some combination of the two.
