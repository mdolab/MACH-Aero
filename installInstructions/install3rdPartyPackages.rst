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
This section lists out the dependency versions that have been verified to work with the latest MDO Lab tools available on GitHub.

.. IMPORTANT::
   Although the code may work with other dependency versions (for example NumPy and SciPy requirements are not strict), we only test code against the dependency versions listed below.
   Therefore, if you choose to use a different dependency version, then you are essentially on your own.

   If you are doing a clean install, it's probably best to use the versions listed under the ``latest`` column.
   On the other hand, cluster installs may benefit from the ``stable`` versions.


========= ======= =======
Versions  stable  latest
========= ======= =======
OpenMPI   3.1.*   4.1.*
mpi4py    3.1.4   3.1.4
PETSc     3.15.*  3.18.*
CGNS      4.2.0   4.3.0
Python    3.9.*   3.10.*
NumPy     1.21.*  1.24.3+
SciPy     1.7.*   1.10.*
========= ======= =======

The supported operating systems are Ubuntu 20.04 and 22.04 together with GNU compiler versions 9 and 11, respectively.
For the rest of the instructions, we use angled brackets such as ``<version>`` as placeholders, where you should enter values specific to your installation such as package versions.

.. _install_prereq:

Common Prerequisites
--------------------
If they're not available already, common prerequisites can be installed via ``apt`` under Ubuntu:

.. prompt:: bash

   sudo apt-get install python3-dev gfortran valgrind cmake libblas-dev liblapack-dev build-essential swig

These packages are required by many of the packages installed later.

On a cluster, check the output of ``module avail`` to see what has already been installed.
They can also be installed locally, but they are common enough that they are typically pre-installed.


C and Fortran Based Packages
----------------------------
These packages have minimal dependencies and should be installed first, in the order listed here.
These source code for these packages are often downloaded and installed to ``$HOME/packages/<package name>``,
which will be adopted as convention for the instructions here.
The environment is adapted for each package by modifying ``$HOME/.bashrc`` or equivalent.

.. _install_openmpi:

OpenMPI
~~~~~~~

.. IMPORTANT::
   OpenMPI depends only on a C/Fortran compiler, such as ``gcc/gfortran`` or ``icc/ifort``.

   On a cluster, the system administrator will have already compiled various versions of MPI on the system already.
   Do not build/install OpenMPI in this case, and simply load the correct MPI module.

Download the desired version from the `OpenMPI <http://www.open-mpi.org/>`__ website and place the tarball in your packages directory, ``$HOME/packages``:

.. prompt:: bash

   wget <download URL>

Then, unpack the source code:

.. prompt:: bash

   tar -xvaf openmpi-<version>.tar.gz

Add the following lines to ``$HOME/.bashrc``:

.. code-block:: bash

   # -- OpenMPI Installation
   export MPI_INSTALL_DIR=$HOME/packages/openmpi-<version>/opt-gfortran
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
   export PATH=$MPI_INSTALL_DIR/bin:$PATH

After saving the file, source ``$HOME/.bashrc``:

.. prompt:: bash

   source ~/.bashrc

Go to the OpenMPI directory:

.. prompt:: bash

   cd $HOME/packages/openmpi-<version>

ONLY IF using an Intel compiler, run:

.. prompt:: bash

   export CC=icc CXX=icpc F77=ifort FC=ifort

Finally, configure and build the package:

.. prompt:: bash

   ./configure --prefix=$MPI_INSTALL_DIR

.. prompt:: bash

   make all install

To verify that paths are as expected run

.. prompt:: bash

   which mpicc

and

.. prompt:: bash

   echo $MPI_INSTALL_DIR/bin/mpicc

The above should print out the same path for both.

.. _install_petsc:

PETSc
~~~~~

.. IMPORTANT::
   PETSc depends on OpenMPI, a C/Fortran compiler, and it requires ``cmake`` to build.

PETSc, the Portable Extensible Toolkit for Scientific Computation is a comprehensive library for helping solve large scale PDE problems.

Download the desired version from the `PETSc <http://www.mcs.anl.gov/petsc/index.html>`__ website and place the tarball in your packages directory, ``$HOME/packages``:

.. prompt:: bash

   wget <download URL>

Unpack the source directory in your packages directory:

.. prompt:: bash

   tar -xvaf petsc-<version>.tar.gz

Next, configure your environment for PETSc by adding the following lines to your ``$HOME/.bashrc``:

.. code-block:: bash

   # -- PETSc Installation
   export PETSC_ARCH=real-debug
   export PETSC_DIR=$HOME/packages/petsc-<version>/

After saving the file, source ``$HOME/.bashrc``:

.. prompt:: bash

   source ~/.bashrc


Go to the PETSc directory:

.. prompt:: bash

   cd $HOME/packages/petsc-<version>

The ``PETSC_ARCH`` variable is any user-specified string.
It should be set to something representative of the actual architecture.

The next step is to configure PETSc.
There are a huge number and variety of options.
To get a list of all available options run:

.. prompt:: bash

   ./configure --help


To facilitate installation of PETSc for use with MDO Lab tools, here are some common preset configurations.

* Standard debug build (``PETSC_ARCH=real-debug``):

   .. prompt:: bash

      ./configure --PETSC_ARCH=$PETSC_ARCH --with-scalar-type=real --with-debugging=1 --with-mpi-dir=$MPI_INSTALL_DIR \
         --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
         --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11

* Debug complex build (``PETSC_ARCH=complex-debug``):

   .. prompt:: bash

      ./configure --PETSC_ARCH=$PETSC_ARCH --with-scalar-type=complex --with-debugging=1 --with-mpi-dir=$MPI_INSTALL_DIR \
         --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
         --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11

* Optimized real build on a cluster with existing MPI (``PETSC_ARCH=real-opt``):

   .. prompt:: bash

      ./configure --with-shared-libraries --download-superlu_dist --download-parmetis=yes --download-metis=yes \
         --with-fortran-bindings=1 --with-debugging=0 --with-scalar-type=real --PETSC_ARCH=$PETSC_ARCH --with-cxx-dialect=C++11

.. NOTE::
   If you are compiling PETSc on Great Lakes, check the cluster-specific setup page for the correct configurations.

Here is a short overview of some of the options used above.

* **Debugging**: To compile without debugging use the switch:

   .. code-block:: bash

      --with-debugging=0

   If you are doing any code development which uses PETSc, it is *highly* recommended to use debugging.
   However, if you are doing production runs on an HPC, then you should turn this off to improve code performance.

   To further specify compiler optimization flags, use:

   .. code-block:: bash

      --COPTFLAGS=-O3 --CXXOPTFLAGS=-O3 --FOPTFLAGS=-O3

* **METIS and ParMETIS**: partitioning packages

   If you do not have METIS and ParMETIS installed, include the following line:

   .. code-block:: bash

      --download-metis=yes --download-parmetis=yes

   If they are already installed, you can simply supply the installation directories:

   .. code-block:: bash

      --with-metis --with-metis-dir=<metis-dir> --with-parmetis --with-parmetis-dir=<parmetis-dir>

* **Complex build**: partitioning packages

   A complex build is configured via:

   .. code-block:: bash

      --with-scalar-type=complex

* **Other**: Various options are also required:

   .. code-block:: bash

      --with-shared-libraries --download-superlu_dist=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11

After the configuration step, PETSc must be built. This is accomplished with the command provided at the end of the configure script.
It will look something like below (the PETSc version should be consistent with the version being installed.):

.. prompt:: bash

   make PETSC_DIR=$HOME/packages/petsc-<version> PETSC_ARCH=$PETSC_ARCH all

After build, follow the command provided at the end of the print out to test the functionality. It will look something like below:

.. prompt:: bash

    make PETSC_DIR=$HOME/packages/petsc-<version> PETSC_ARCH=$PETSC_ARCH test

.. NOTE::
   If your PETSc is not able to find MPI, try:

   #. Add ``--with-mpi-dir=$MPI_INSTALL_DIR`` when you configure PETSc
   #. Check your ``LD_LIBRARY_PATH`` order. If you have PyTecplot, try moving the entry for PyTecplot in the ``LD_LIBRARY_PATH`` to the end, by modifying your ``.bashrc``.


.. _install_cgns:

CGNS Library
~~~~~~~~~~~~

.. IMPORTANT::
   CGNS depends on a C/Fortran compiler. It can be built using either CMake or GNU make.
   The instructions here use CMake.

CGNS is a general file format for storing CFD data, and is used by ``ADflow``, ``IDWarp``, ``pyHyp``, and ``cgnsUtilities``.
The CGNS Library provides Fortran bindings to read/write files in that format.

.. NOTE::
   CGNS now supports two output types: HDF5 and the Advanced Data Format (ADF) format.
   While HDF5 is the officially supported format, its compatibility with other tools is sparse.
   Therefore, for using MDO Lab codes, the ADF format is recommended.
   The rest of the instructions use ADF and not HDF5.

Download the desired version from the `CGNS <https://cgns.github.io/download.html>`__ website and place the tarball in your packages directory, ``$HOME/packages``:

.. prompt:: bash

   wget <download URL>

Unpack the source directory in your packages directory:

.. prompt:: bash

   tar -xvaf v<version>.tar.gz

Next, configure your environment for CGNS by adding the following lines to your ``$HOME/.bashrc``:

.. code-block:: bash

   # -- CGNS
   export CGNS_HOME=$HOME/packages/CGNS-<version>/opt-gfortran
   export PATH=$PATH:$CGNS_HOME/bin
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

After saving the file, source ``$HOME/.bashrc``:

.. prompt:: bash

   source ~/.bashrc

Go to the CGNS directory:

.. prompt:: bash

   cd $HOME/packages/CGNS-<version>

To configure the package, run:

.. prompt:: bash

   cmake -D CGNS_ENABLE_FORTRAN=ON -D CMAKE_INSTALL_PREFIX=$CGNS_HOME -D CGNS_ENABLE_64BIT=OFF -D CGNS_ENABLE_HDF5=OFF -D CGNS_BUILD_CGNSTOOLS=OFF -D CMAKE_C_FLAGS="-fPIC" -D CMAKE_Fortran_FLAGS="-fPIC" .

If your compilers are not located at ``/usr/bin/gcc``, either because you are on an HPC system or using Intel compilers, you must adjust the configure command.
This is done by passing additional variables to ``cmake``:

.. prompt:: bash

   cmake <options> -D CMAKE_C_COMPILER=/path/to/ccompiler -D CMAKE_Fortran_COMPILER=/path/to/fcompiler .

where ``CMAKE_C_COMPILER`` sets the path to the C compiler, and ``CMAKE_Fortran_COMPILER`` sets the path to the Fortran compiler.
If your compilers are on the ``$PATH`` (likely if you are using the module system on a cluster), you can use ``CMAKE_C_COMPILER=$(which icc)`` and ``CMAKE_Fortran_COMPILER=$(which ifort)`` for Intel compilers, or correspondingly ``CMAKE_C_COMPILER=$(which gcc)`` and ``CMAKE_Fortran_COMPILER=$(which gfortran)`` for GNU compilers.


Finally, build and install:

.. prompt:: bash

   make install



Installing CGNS Tools (Optional)
********************************
The CGNS Library comes with a set of tools to view and edit CGNS files manually.
To install these tools, use the flag ``-D CGNS_BUILD_CGNSTOOLS=ON`` during the configure step.
Note that these tools should be installed on a local computer and not on a cluster.

To enable this option you may need to install the following packages:

.. prompt:: bash

   sudo apt-get install libxmu-dev libxi-dev

CGNS library sometimes complains about missing includes and libraries.
Most of the time this is either Tk/TCL or OpenGL.
This can be solved by installing the following packages.
Note that the version of these libraries might be different on your machine:

.. prompt:: bash

   sudo apt-get install freeglut3

.. prompt:: bash

   sudo apt-get install tk8.6-dev

If needed, install the following package as well:

.. prompt:: bash

   sudo apt-get install freeglut3-dev

If you compiled with ``-D CGNS_BUILD_CGNSTOOLS=ON``, you either need to add the binary path to your PATH environmental variable or you can install the binaries system wide.
By specifying the installation prefix as shown in the example configure commands above, the binary path is in your PATH environmental variables;
without specifying the prefix, the default is a system path, which requires sudo.

Python Packages
---------------
In this guide, python packages are installed using ``pip``.
Other methods, such as from source or using ``conda``, will also work.

.. note::
   A dedicated Python virtual environment, for example generated using ``venv``, is highly recommended.

When installing the same package multiple times with different dependencies,
for example ``petsc4py`` with different petsc builds, the pip cache can become incorrect.
Therefore, we recommend the ``--no-cache`` flag when installing python packages with ``pip``.

.. _install_numpy:

NumPy
~~~~~

.. IMPORTANT::
   Version ``1.13.3`` and ``1.15.4`` of numpy or f2py do **NOT** work.
   See :ref:`working_stacks` for numpy versions that are tested.

NumPy is required for all MDO Lab packages.
It is installed with:

.. prompt:: bash

   pip install numpy==<version>

SciPy
~~~~~
SciPy is required for several packages including ``pyOptSparse``, ``pyGeo`` and certain functionality in ``pySpline``.
It is installed with:

.. prompt:: bash

   pip install scipy==<version>


.. note::
   On a cluster, most likely numpy and scipy will already be installed.
   Unless the version is invalid, use the system-provided installation which should offer better performance.

.. _install_mpi4py:

mpi4py
~~~~~~
.. IMPORTANT::
   mpi4py depends on OpenMPI.
   Since mpi4py generally lags in version, it is recommended to use a version that matches as closely as possible to the installed OpenMPI version.

mpi4py is the Python wrapper for MPI. This is required for **all** parallel MDO Lab codes.

Simple install with pip
***********************
It is installed with:

.. prompt:: bash

   pip install mpi4py==<version>

.. NOTE::
   Some function usages have changed in newer versions of mpi4py. Check the `release <https://github.com/mpi4py/mpi4py/blob/master/CHANGES.rst>`_ to see the modifications that might be requried in the code.

Advanced install
****************
Alternatively, installing from source is also possible.
First, download the source code from `releases <https://github.com/mpi4py/mpi4py/releases>`__, and extract it into the packages directory.
Then, either run ``pip install .`` or ``python setup.py install`` in the root directory.
Installing from source has the advantage of having access to the tests, which can be used to verify both the OpenMPI and mpi4py installations.

To run the tests, go to the ``test`` directory, and type:

.. prompt:: bash

   python runtests.py


.. _install_petsc4py:

petsc4py
~~~~~~~~
.. IMPORTANT::
   The MAJOR.MINOR version of petsc4py **MUST** match the MAJOR.MINOR version of PETSc.
   For example, PETSc 3.14.X will only work with petsc4py 3.14.Y.
   In practice, this means you must request a specific version of petsc4py.

   petsc4py depends on PETSc and its dependencies.

``petsc4py`` is the Python wrapper for PETSc.

If you want to make developments or multiple PETSc architectures are needed, you should install petsc4py manually, which described in **Advanced install**.
Manually installing provide you useful run tests.

If you know you will **only** need real PETSc architecture, you can use pip.

Simple install with pip
***********************

It is installed with:

.. prompt:: bash

   pip install petsc4py==<version> --no-cache

Build from source (Required for multiple PETSc architectures)
*************************************************************
.. WARNING::
   You must compile a unique petsc4py install for each PETSc architecture.

If using PETSc < 3.14, `Download <https://bitbucket.org/petsc/petsc4py/downloads>`__ the source code and
extract the correct version matching your PETSc version:

.. prompt:: bash

   tar -xzf petsc4py-<version>.tar.gz
   cd petsc4py-<version>

From 3.14 onwards, petsc4py is included in the PETSc source code, in which case you can skip the above step and simply go straight to the petsc4py source directory:

.. prompt:: bash

   cd $PETSC_DIR/src/binding/petsc4py

Then install:

.. prompt:: bash

   pip install .

.. warning::
   If there is an existing ``build`` directory it must be forcibly removed (``rm -fr build``) before doing another architecture install.
   To install with multiple architectures change the ``PETSC_ARCH`` variable to contain all the architecture you want to install petsc4py for::

      export PETSC_ARCH=<petsc_arch_1>:<petsc_arch_2>:<petsc_arch_3>:...

   Then install the package:

   .. prompt:: bash

      pip install .

   Don't forget to switch the ``PETSC_ARCH`` variable back to a single value after installing

Installing from source has the advantage of having access to the tests, which can be used to verify both the PETSc and petsc4py installations.

To run the tests, go to the ``test`` directory, and type:

.. prompt:: bash

   python runtests.py

Other Methods and Notes
-----------------------
The build examples described here are all installed *locally* (e.g. ``$HOME/...``) rather than system-wide (e.g. ``/usr/local/...``).
Local installations are generally preferred.
Installing packages system-wide requires root access, which is an increased security risk when downloading packages from the internet.
Also, it is typically easier to uninstall packages or otherwise revert changes made at a local level.
Finally, local installations are required when running on a cluster environment.

The build and installation paradigm demonstrated here puts source code, build files, and installed packages all in ``$HOME/packages``.
Another common convention is to use ``$HOME/src`` for source code and building,
and ``$HOME/opt`` for installed packages.
This separation adds a level of complexity but is more extensible if multiple package versions/installations are going to be used.

When configuring your environment, the examples shown here set environment variables, ``$PATH``, and ``$LD_LIBRARY_PATH`` in ``.bashrc``.
If multiple versions and dependencies are being used simultaneously,
for example on a cluster, the paradigm of `environment modules <http://modules.sourceforge.net>`__ is often used (e.g. ``module use petsc``).
A module file is simply a text file containing lines such as:

.. code-block:: bash

   append-path PATH $HOME/opt/petsc/3.7.7/OpenMPI-1.10.7/GCC-7.3.0/bin

MDO Lab tools can be used by configuring your environment with either ``.bashrc`` or environment modules, or some combination of the two.
