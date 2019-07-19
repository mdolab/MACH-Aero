.. Installation instruction on how to set up external packages need to
   run the MDOlab code.
   Author: Eirikur Jonsson (eirikurj@umich.edu)
   Modified by Ross S. Chaudhry (rchaud@umich.edu) in July 2019


.. _install3rdPartyPackages:

3rd Party Packages
==================


Before you try to compile **any** of the MDOlab codes, it is **HIGHLY
RECOMMENDED** that you install the following packages below. We recommend
creating a directory to store these external dependencies, such as
``~/packages``.


.. _install_prereq:

Common Prerequisites
--------------------
If they're not available already, common prerequisites can be installed directly from a Debian repository::

   sudo apt-get install python-dev gfortran valgrind cmake

The packages are required by many of the packages installed later.
On a cluster, check the output of ``module avail`` to see what has already been installed.


C and Fotran Based Packages
---------------------------
These packages have minimal dependencies and should be installed first, in the order listed here.
These source code for these packages are often downloaded and installed to ``$HOME/packages/$PACKAGE_NAME``,
which will be adopted as convention for the instructions here.
The environment is adapted for each package by modifying your ``$HOME/.bashrc`` or equivalent.


`OpenMPI <http://www.open-mpi.org/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenMPI version ``1.10.7`` has been tested to work for MDO tools.
OpenMPI depends only a C/Fortran compiler, such as ``gcc/gfortran`` or ``icc/ifort``.

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

PETSc, the Portable Extensible Toolkit for Scientific Computation is a
comprehensive library for helping solve large scale PDE problems.
PETSc is used by :ref:`adflow`, :ref:`pywarp`, :ref:`pyhyp`, Tripan and pyAeroStruct.

Version ``3.7.7`` has been tested with the MDOlab codes and the procedure described below.
Use other versions at your own risk.
PETSc depends on OpenMPI, a C/Fotran compiler, cmake, and valgrind.

Download and unpack the source directory, from your packages directory:

.. code-block:: bash

   cd $HOME/packages
   wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.7.7.tar.gz
   tar -xvaf petsc-3.7.7
   cd petsc-3.7.7

The lite version of the package is smaller but contains no documentation.
Next, configure your environment for PETSc by adding the following lines to your ``$HOME/.bashrc`` and ``source``-ing it:

.. code-block:: bash

   # -- PETSc Installation
   export PETSC_ARCH=real-debug
   export PETSC_DIR=$HOME/packages/petsc-3.7.7/$PETSC_ARCH

   export PATH=$PATH:$PETSC_DIR/bin
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/lib

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

   ./configure --prefix=$PETSC_HOME --PETSC_ARCH=$PETSC_ARCH --with-debugging=yes \
      --download-fblaslapack=yes --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
      --with-shared-libraries --with-fortran-interfaces=yes

2. Debug complex build (``$PETSC_ARCH=complex-debug``):

.. code-block:: bash

   ./configure --with-shared-libraries --download-superlu_dist --download-parmetis=yes --download-metis=yes \
      --with-fortran-interfaces=1 --with-debugging=yes --with-scalar-type=complex --PETSC_ARCH=$PETSC_ARCH

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

Finally, build and install with::
   
   make all install


.. _install_cgns:

`CGNS Library <http://cgns.github.io/>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CGNS library is used to provide CGNS functionality for :ref:`adflow`,
:ref:`pywarp`, and :ref:`pyhyp`.

Versions ``3.3.0`` and ``3.2.1`` have been tested with the MDOlab codes.
CGNS depends on cmake and a C/Fortran compiler.

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
   export CGNS_HOME $HOME/packages/CGNS-3.2.1/opt-gfortran
   export PATH=$PATH:$CGNS_HOME/bin
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

Make a ``build`` directory, and call cmake from there to configure the package:

.. code-block:: bash

   mkdir build       # If it exists from a previous build, remove it first
   cd build
   cmake .. -DCGNS_ENABLE_FORTRAN=1 -DCMAKE_INSTALL_PREFIX=$CGNS_HOME

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
WIP, below is the original

.. _install_mpi4py:

`mpi4py <http://mpi4py.scipy.org/>`_
------------------------------------

``mpi4py`` is the Python wrapper for MPI. This is required for
**all** parallel MDOlab codes. `Download
<https://bitbucket.org/mpi4py/mpi4py/downloads>`__  the source code and untar::

  $ tar -xzf mpi4py-1.3.1.tar.gz

From the ``mpi4py-1.3.1`` directory, do a user-space install::

  $ python setup.py install --user

This will install the package to the ``.local`` directory in your home
directory which is suitable for both desktop and cluster accounts.



.. _install_petsc4py:

`petsc4py <https://bitbucket.org/petsc/petsc4py/downloads>`_
------------------------------------------------------------

``petsc4py`` is the Python wrapper for PETSc. Strictly speaking, this
is only required for the coupled solvers in pyAeroStruct. However, it
*is* necessary if you want to use any of PETSc command-line options
such as -log-summary. `Download
<https://bitbucket.org/petsc/petsc4py/downloads>`__ the source code and
extract the latest version (the major version should be consistent with 
the PETSc version installed, i.e., 3.7.0 here)::

  $ tar -xzf petsc4py-3.7.0.tar.gz

From the petsc4py-3.7.0 directory do a user-space install::

  $ python setup.py install --user

This will install the package to the ``.local`` directory in your home
directory which is suitable for both desktop and cluster accounts.
You may seen an error warning related to ``python-mpi``, but this 
should not be a problem. 

.. WARNING:: 
   You must compile a unique petsc4py install for each petsc
   architecture. This is easy to forget and can cause lots of
   problems. **IF THERE IS AN EXISTING** ``build`` **DIRECTORY IT MUST BE
   FORCIBLY REMOVED** (``rm -fr build``) **BEFORE DOING ANOTHER ARCHITECTURE
   INSTALL**. To install with a different architecture change the
   ``PETSC_ARCH`` variable in your ``.bashrc`` file::

      export PETSC_ARCH=<new_architecture>

   Then install the package::

      $ python setup.py install --user



.. _install_num_sci_py:

`Numpy + Scipy <http://scipy.org/>`_
------------------------------------

Numpy is required for **all** MDOlab packages. Scipy is required for
several packages including :ref:`pyoptsparse`, :ref:`pygeo` and certain
functionality in pytacs and :ref:`pyspline`. For a desktop computer
where you have root access, it is easiest to install numpy from the
package manager::

  sudo apt-get install python-numpy python-scipy

.. note::
   On a cluster, most likely numpy and scipy will already be
   installed. If not, see the the system administrator. If you are
   forced  to do it yourself, refer to the numpy and scipy
   documentation for compilation instructions.




Other Notes
-----------

.. Other installation methods: apt get for openmpi, petsc, etc. System wide install
   or modules instead of bashrc
HDF5
Source code, build, and install is all in $HOME/packages
Another common convention is to use $HOME/src for source code and building, and $HOME/opt for installed files
This separation adds a level of complexity but is more extensible if multiple package versions/installations are going to be used.
Also allows for more complete list of dependencies.
