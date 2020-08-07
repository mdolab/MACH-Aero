.. Installation instruction on how to set up external packages need to
   run the MDO Lab code.

.. _installThirdPartyPackages:

Third Party Packages
====================
.. NOTE::
   Before trying to compile everything yourself, including all dependencies, consider using the ``mdolab/public`` Docker image available on `Docker Hub <https://hub.docker.com/r/mdolab/public>`_.

.. _working_stacks:

Supported dependency versions
-----------------------------
This section lists out the dependency versions that have been verified to work with specific code versions.
Here ``version`` refers to the code version, and ``tag`` refers to the Docker image tag.
If you are using the latest code from GitHub, then please use the row that contains the latest ``version``.

.. IMPORTANT::
   Although the code may work with other dependency versions (for example numpy and scipy requirements are not
   strict), we only test code against the dependency versions listed below. Therefore, if you choose to use
   a different dependency version, then you are essentially on your own.

.. list-table::
   :header-rows: 1

   *  - Version
      - Tag
      - OS
      - Compiler
      - OpenMPI
      - mpi4py
      - PETSc
      - petsc4py
      - CGNS
      - python
      - numpy
      - scipy
      - swig

   *  - 2.x
      - py2
      - 18.04
      - gcc/7.4
      - 3.1.4
      - 3.0.2
      - 3.11.0
      - 3.11.0
      - 3.3.0
      - 2.7
      - 1.16.4
      - 1.2.1
      - 2.0.12

   *  - 1.x
      - v1
      - 16.04
      - gcc/7.4
      - 1.10.7
      - 1.3.1
      - 3.7.7
      - 3.7.0
      - 3.2.1
      - 2.7
      - 1.16.4
      - 1.2.1
      - 2.0.12

.. _install_prereq:

Common Prerequisites
--------------------
If they're not available already, common prerequisites can be installed directly from a Debian repository::

   sudo apt-get install python-dev gfortran valgrind cmake libblas-dev liblapack-dev

The packages are required by many of the packages installed later.
On a cluster, check the output of ``module avail`` to see what has already been installed.
They can also be installed locally, but they are common enough that a system install is acceptable.


C and Fortran Based Packages
----------------------------
These packages have minimal dependencies and should be installed first, in the order listed here.
These source code for these packages are often downloaded and installed to ``$HOME/packages/$PACKAGE_NAME``,
which will be adopted as convention for the instructions here.
The environment is adapted for each package by modifying ``$HOME/.bashrc`` or equivalent.


`OpenMPI <http://www.open-mpi.org/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   The version(s) of OpenMPI tested to work with MDO Lab tools is ``3.1.4``

   OpenMPI depends only on a C/Fortran compiler, such as ``gcc/gfortran`` or ``icc/ifort``.

.. NOTE::
   On a cluster, the system administrator will have already compiled various versions of MPI on the system already.
   Do not build/install OpenMPI in this case.

   OpenMPI may also be installed by PETSc (see below), but a separate installation as described here is preferred.

Download and unpack the source directory, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-3.1.4.tar.gz
   tar -xvaf openmpi-3.1.4.tar.gz
   cd openmpi-3.1.4

Add the following lines to ``$HOME/.bashrc`` and ``source`` it:

.. code-block:: bash

   # -- OpenMPI Installation
   export MPI_INSTALL_DIR=$HOME/packages/openmpi-3.1.4/opt-gfortran
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
   export PATH=$MPI_INSTALL_DIR/bin:$PATH

Finally, configure and build the package:

.. code-block:: bash

   # export CC=icc CXX=icpc F77=ifort FC=ifort    # Only necessary if using non-GCC compiler
   ./configure --prefix=$MPI_INSTALL_DIR
   make all install

To verify that paths are as expected run

.. code-block:: bash

   which mpicc
   echo $MPI_INSTALL_DIR/bin/mpicc

The above should print out the same path for both.

.. _install_petsc:

`PETSc <http://www.mcs.anl.gov/petsc/index.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   The version(s) of PETSc tested to work with MDO Lab tools is ``3.11.0``.
   Use other versions at your own risk.

   PETSc depends on OpenMPI, a C/Fortran compiler, and it requires ``cmake`` to build.

PETSc, the Portable Extensible Toolkit for Scientific Computation is a comprehensive library for helping solve large scale PDE problems.

Download and unpack the source directory, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.11.0.tar.gz
   tar -xvaf petsc-3.11.0.tar.gz
   cd petsc-3.11.0

The lite version of the package is smaller but contains no documentation.
Next, configure your environment for PETSc by adding the following lines to your ``$HOME/.bashrc`` and ``source``-ing it:

.. code-block:: bash

   # -- PETSc Installation
   export PETSC_ARCH=real-debug
   export PETSC_DIR=$HOME/packages/petsc-3.11.0/


The ``PETSC_ARCH`` variable is any user-specified string.
It should be set to something representative of the actual architecture.

The next step is to configure PETSc.
There are a huge number and variety of options.
To get a list of all available options run::

   ./configure --help

We explain the relevant options below, but you can jump ahead to
:ref:`configure PETSc <configure_petsc>` and use one of the pre-set list of options there.

#. **Debugging**: To compile without debugging use the switch:

   .. code-block:: bash

      --with-debugging=0

   If you are doing any code development which uses PETSc,
   it is *highly* recommended to use debugging.
   However, if you are doing production runs on an HPC,
   then you should turn this off to improve code performance.

   To further specify compiler optimization flags, use:

   .. code-block:: bash

      --COPTFLAGS=-O3 --CXXOPTFLAGS=-O3 --FOPTFLAGS=-O3

#. **METIS and ParMETIS**: partitioning packages

   If you do not have METIS and ParMETIS installed, include the following line:

   .. code-block:: bash

      --download-metis=yes --download-parmetis=yes

   If they are already installed, you can simply supply the installation directories:

   .. code-block:: bash

      --with-metis --with-metis-dir=<metis-dir> --with-parmetis --with-parmetis-dir=<parmetis-dir>

#. **Complex build**: partitioning packages

   A complex build is configured via:

   .. code-block:: bash

      --with-scalar-type=complex

#. **Other**:
   Various options are also required:

   .. code-block:: bash

      --with-shared-libraries --download-superlu_dist=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11

.. _configure_petsc:

There are many other options, and they enable linking and/or downloading to a variety of other packages.
Putting these options together, some complete examples of configuring PETSc are:

#. Standard debug build (``$PETSC_ARCH=real-debug``):

   .. code-block:: bash

      ./configure --PETSC_ARCH=$PETSC_ARCH --with-scalar-type=real --with-debugging=1 --with-mpi-dir=$MPI_INSTALL_DIR \
         --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
         --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11

#. Debug complex build (``$PETSC_ARCH=complex-debug``):

   .. code-block:: bash

      ./configure --PETSC_ARCH=$PETSC_ARCH --with-scalar-type=complex --with-debugging=1 --with-mpi-dir=$MPI_INSTALL_DIR \
         --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
         --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11

#. Optimized real build on a cluster with existing MPI (``$PETSC_ARCH=real-opt``):

   .. code-block:: bash

      ./configure --with-shared-libraries --download-superlu_dist --download-parmetis=yes --download-metis=yes \
         --with-fortran-bindings=1 --with-debugging=0 --with-scalar-type=real --PETSC_ARCH=$PETSC_ARCH --with-cxx-dialect=C++11

.. NOTE::
   If you are compiling PETSc on Great Lakes, check the cluster-specific setup page for the correct configurations.

After the configuration step, PETSc must be built. This is accomplished with the command provided at the end of the configure script. It will look something like below (the PETSc version should be consistent with the version being installed.)::

   make PETSC_DIR=$HOME/packages/petsc-3.11.0 PETSC_ARCH=$PETSC_ARCH all

After build, follow the the command provided at the end of the print out to test the functionality. It will look something like below::

    make PETSC_DIR=$HOME/packages/petsc-3.11.0 PETSC_ARCH=$PETSC_ARCH test

.. NOTE::
   If your PETSc is not able to find mpi, try:

   #. Add ``--with-mpi-dir=$MPI_INSTALL_DIR`` when you configure PETSc
   #. Check your LD_LIBRARY_PATH order. If you have pytecplot, try moving tecplot LD_LIBRARY_PATH to the last.


.. _install_cgns:

`CGNS Library <http://cgns.github.io/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   The version(s) of CGNS tested to work with MDO Lab tools is ``3.3.0`` and ``3.2.1``.

   CGNS depends on a C/Fortran compiler and requires cmake to build.

The CGNS library is used to provide CGNS functionality for ``ADflow``, `IDWarp`, and ``pyHyp``.

.. WARNING::
   The 3.2.1 version fortran include file contains an error. After
   untaring, manually edit the cgnslib_f.h.in file in the ``src``
   directory and remove all the comment lines at the beginning of the
   file starting with c. This is fixed in subsequent versions.

.. NOTE::
   CGNS now supports two output types: HDF5 and
   the Advanced Data Format (ADF) format. While HDF5 is the
   officially supported format, its compatability with other tools is sparse.
   Therefore, for using MDO Lab codes, the ADF format is recommended.
   Installing and linking HDF5 is therefore not recommended.

Download and unpack the source directory, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz
   tar -xvaf v3.3.0.tar.gz
   cd CGNS-3.3.0

Next, configure your environment for CGNS by adding the following lines to your ``$HOME/.bashrc`` and ``source``-ing it:

.. code-block:: bash

   # -- CGNS
   export CGNS_HOME=$HOME/packages/CGNS-3.3.0/opt-gfortran
   export PATH=$PATH:$CGNS_HOME/bin
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

Next is to configure the package.
Here are some notes for configuring below, or you can jump ahead to the configure commands
:ref:`configure CGNS <configure_cgns>`. 

.. NOTE::

   - If you want to build the CGNS tools to view and edit CGNS files manually,
      set ``-DCGNS_BUILD_CGNSTOOLS = 1``. To enable this option you may need
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

      .. warning:: 
         There is a known bug in CGNS 3.3.0 (fixed in later versions) that crashes the build routine for Ubuntu 18/20 when this CGNS tools option is turned on. You can either turn it off compiling with ``-DCGNS_BUILD_CGNSTOOLS = 0`` or, if you still want to use CGNS tools, you can manually patch the source files using `this PR <https://github.com/CGNS/CGNS/pull/55/files>`_ as a reference.

      **Optional**: If you compiled with ``-DCGNS_BUILD_CGNSTOOLS = 1`` you
      either need to add the binary path to your PATH environmental variable or
      you can install the binaries system wide. By specifying the installation prefix 
      as shown in the later example configure commands, the binary path is in your PATH environmental variables; 
      without specifying the prefix, the default is a system path, which requires sudo.

   - When compiling on a cluster, it helps to set ``-DCGNS_BUILD_CGNSTOOLS = 0``. 
      It will build without the cgnstools which requires additional packages.

   - If you use intel compilers:
      Check ``CMAKE_C_COMPILER:FILEPATH`` and ``CMAKE_FORTRAN_COMPILER:FILEPATH`` in ``CMakeCache.txt`` 
      file after you configure the package. It's likely that CGNS gets compiled with some random old version of gcc stored in ``/bin/``. 
      If they are incorrect, to compile it correctly, remove your old install and set the environment variables ``export CC=$(which icc)`` and ``export FC=$(which ifort)``. 


      Another notice on the intel installs is that the ``config.mk`` files are out of date. 
      With new intel compilers, the actual mpi-wrapped compilers changed names. 
      Check out the compilers_, and modify the ``FF90`` and ``CC`` options in ``config.mk`` files as needed.

   .. _compilers: https://software.intel.com/en-us/mpi-developer-reference-linux-compilation-commands


Make a ``build`` directory, and call cmake from there to configure the package:

.. _configure_cgns:

.. code-block:: bash

   mkdir build       # If it exists from a previous build, remove it first
   cd build
   cmake .. -DCGNS_ENABLE_FORTRAN=1 -DCMAKE_INSTALL_PREFIX=$CGNS_HOME -DCGNS_BUILD_CGNSTOOLS=1



Finally, build and install::

   $ make all install

.. _install_swig:

`SWIG (optional) <https://github.com/swig/swig>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SWIG is a wrapper for external software written in C or C++. It is an **OPTIONAL** component for MACH-Aero, as it is required by only some of its sub-modules (eg. NSGA2 and NOMAD optimizers used by pyOptSparse, as discussed `here <https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/install.html>`_). 

.. WARNING:: 

   SWIG 2.0.12 is the **ONLY** currently supported version. Other versions are not recommended and are installed at your own risk.

Download and unpack the source files, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget http://prdownloads.sourceforge.net/swig/swig-2.0.12.tar.gz
   tar -xzf swig-2.0.12.tar.gz
   cd ./swig-2.0.12

Configure your environment variables by adding the following lines to your ``.bashrc`` file, remembering to ``source ~/.bashrc`` or opening a new terminal once you saved the changes:

.. code-block:: bash

   export SWIG_HOME=$HOME/packages/swig-2.0.12
   export PATH=$PATH:$SWIG_HOME/bin

Then configure SWIG and build the binaries using the following commands:

.. code-block:: bash

   ./configure --prefix=$SWIG_HOME
   make
   make install

.. NOTE::

   The configuration and build of SWIG requires the `PCRE developer package <https://www.pcre.org/>`_. If not already present on your system, you can install it via ``sudo apt-get install libpcre3 libpcre3-dev``

Python Packages
---------------

.. IMPORTANT::
   MDO Lab tools have been tested to work with python 2.
   The MDO Lab is in the process of migrating to python 3;
   however we will continue to support python 2 for the forseeable future.

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

`Numpy <https://numpy.org/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. IMPORTANT::
   Version ``1.13.3`` and ``1.15.4`` of numpy or f2py do **NOT** work.
   See :ref:`working_stacks` for numpy versions that have been tested.
   The version(s) of numpy used here is ``1.16.4``.

Numpy is required for all MDO Lab packages.
It is installed with::

   pip install numpy==1.16.4 --user --no-cache

On a ``conda``-based system, it is recommended to use ``conda`` to install numpy and scipy::

   conda install numpy==1.16.4

`Scipy <http://scipy.org/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Scipy is required for several packages including ``pyOptSparse``, ``pyGeo`` and certain functionality in ``pySpline``.
It is installed with::

   pip install scipy==1.2.1 --user --no-cache

On a ``conda``-based system, it is recommended to use ``conda`` to install numpy and scipy::

   conda install scipy==1.2.1

.. note::
   On a cluster, most likely numpy and scipy will already be
   installed. Unless the version is invalid, use the system-provided installation.

.. _install_mpi4py:

`mpi4py <http://mpi4py.scipy.org/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. IMPORTANT::
   The version(s) of mpi4py tested to work with MDO Lab tools is 3.0.2.

   mpi4py depends on OpenMPI.

   It is recommended that the OpenMPI version matches with the mpi4py version.

mpi4py is the Python wrapper for MPI. This is required for
**all** parallel MDO Lab codes.
It is installed with::

   pip install mpi4py==3.0.2 --user --no-cache

.. NOTE::
   Some function usages have changed in newer versions of mpi4py. Check the `release <https://github.com/mpi4py/mpi4py/blob/master/CHANGES.rst>`_ to see the modifications that might be requried in the code.


.. _install_petsc4py:

`petsc4py <https://bitbucket.org/petsc/petsc4py/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. IMPORTANT::
   The MAJOR.MINOR version of petsc4py **MUST** match the MAJOR.MINOR version of petsc,
   for example petsc 3.11.0 will only work with petsc4py 3.11.X.
   In practice, this means you must request a specific version of petsc4py.

   The version(s) of petsc4py tested to work with MDO Lab tools is 3.11.0, built against petsc version 3.11.0.

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

   pip install petsc4py==3.11.0 --user --no-cache

Advanced install (Multiple PETSc architectures needed)
******************************************************
.. WARNING::
   You must compile a unique petsc4py install for each PETSc architecture.

`Download <https://bitbucket.org/petsc/petsc4py/downloads>`__ the source code and
extract the latest version (the major version should be consistent with
the PETSc version installed, i.e., 3.11.0 here)::

   $ tar -xzf petsc4py-3.11.0.tar.gz

From the petsc4py-3.11.0 directory do a user-space install::

$ python setup.py install --user

This will install the package to the ``.local`` directory in your home
directory which is suitable for both desktop and cluster accounts.
You may seen an error warning related to ``python-mpi``, but this should not be a problem.

.. warning::
   If there is an existing ``build`` directory it must be forcibly removed (``rm -fr build``) before doing another architecture install.
   To install with a different architecture change the ``PETSC_ARCH`` variable in your ``.bashrc`` file and source it, or just type in your terminal to overwrite the old ``PETSC_ARCH``::

      export PETSC_ARCH=<new_architecture>

   Then install the package::

      $ python setup.py install --user


Other Methods and Notes
-----------------------

The MDO Lab tools can be configured to write HDF5 files,
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

   append-path PATH $HOME/opt/petsc/3.7.7/OpenMPI-1.10.7/GCC-7.3.0/bin

MDO Lab tools can be used by configuring your environment with either ``.bashrc`` or environment modules, or some combination of the two.
