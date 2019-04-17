.. Installation instruction on how to set up external packages need to
   run the MDOlab code.
   Author: Eirikur Jonsson (eirikurj@umich.edu)


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
Common prerequisites can be installed directly from a Debian repository::

   sudo apt-get install python-dev gfortran valgrind cmake cmake-curses-gui

The packages are required by many of the packages installed later.




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




.. _install_petsc:

`PETSc <http://www.mcs.anl.gov/petsc/index.html>`_
--------------------------------------------------

PETSc, the Portable Extensible Toolkit for Scientific Computation is a
comprehensive library for helping solve large scale PDE problems.
PETSc is used by :ref:`adflow`, :ref:`pywarp`, :ref:`pyhyp`, Tripan and pyAeroStruct.

.. NOTE::
   Version 3.7.7 of PETSc has been released and has been tested
   with the MDOlab codes and the procedure described below.

`Download <http://www.mcs.anl.gov/petsc/download/index.html>`__ the
PETSc 3.7.7 tarball from the PETSc site. The lite version is ok but
contains no documentation. Put in your packages directory and untar::

  $ tar -xzf petsc-3.7.7.tar.gz

Before compiling, PETSc must first be configured. There are a huge
number and variety of options. To get a list of all available options run::

  $ ./configure --help

PETSc depends on additional software and packages. (This step can be
skipped if you installed the general requirements above)::

  sudo apt-get install cmake valgrind

PETSc configurations options
****************************

Here we describe a few important options that are necessary
for use with MDOlab codes. A few complete examples are provided later.

1. **Debugging**: To compile without debugging use the switch::

      --with-debugging=no

   It is HIGHLY recommended to use debugging until you are ready to
   perform production runs use a debug build.

2. **MPI**: Provides parallel functionality to PETSc.

   Configure will automatically look for MPI compilers mpicc/mpif77
   etc and use them if found in your ``PATH`` (if already installed).

   It is generally better to let PETSc do the job of configuring and
   building a working MPI implementation. To use this option, include
   the following in the configure::

      --download-openmpi=1

   It is also necessary to specify the C/C++/Fortran compilers for PETSc
   to "wrap" into the mpicc, mpicxx and mpif90. This way, the **same**
   compilers are used to build MPI and PETSc. This avoids that
   libraries such as MPI are compiled with different C or Fortran
   compilers if installed from other sources. To set compiles options
   use the following configure options::

      --with-cc=gcc
      --with-cxx=g++
      --with-fc=gfortran

   As noted before PETSc will use to use the compilers specified in
   your ``PATH``. If you want to use Intel's Ifort compiler this can
   be done using::

      --with-fc=ifort

   .. NOTE::
      On a cluster, compiling MPI is generally undesirable since the system
      administrator will have already compiled various versions of MPI on the
      system. In this case, the PETSc configure should automatically pick up
      the mpicc/mpicxx/mpif90 compilers already in your ``PATH``.

   For more information refer to `PETSc documentation on MPI
   <http://www.mcs.anl.gov/petsc/documentation/installation.html#mpi>`_

3. **BLAS and LAPACK**: Linear algebra packages.

   If you do not have BLAS and LAPACK installed you can include
   the following in the configure::

      --download-fblaslapack=1

4. **Other**:
   Various options are also required::

      --with-shared-libraries --download-superlu_dist=yes --download-parmetis=yes --download-metis=yes --with-fortran-interfaces=1

   Specifically, :ref:`pyWarp` uses the ``superlu_dist``.

Here are a few complete examples of configuring PETSc:

1. Debug build, downloading openmpi and fblaslapack, real scalar type (if you plan to use complex-step with PETSc, don't include the ``download-openmpi`` option and follow the openmpi installation instructions described later)::

    $ ./configure --with-shared-libraries --download-superlu_dist --download-parmetis --download-metis --with-fortran-interfaces --with-debugging=yes --with-scalar-type=real --download-openmpi --download-fblaslapack --PETSC_ARCH=real-debug --with-cc=gcc --with-cxx=g++ --with-fc=gfortran

2. Same as above but with Intel fortran compiler::

    $ ./configure --with-shared-libraries --download-superlu_dist --download-parmetis --download-metis --with-fortran-interfaces --with-debugging=yes --with-scalar-type=real --download-openmpi --download-fblaslapack --PETSC_ARCH=real-debug  --with-cc=gcc --with-cxx=g++ --with-fc=ifort

3. Debug complex build on a cluster with existing MPI::

    $ ./configure --with-shared-libraries --download-superlu_dist --download-parmetis=yes --download-metis=yes --with-fortran-interfaces=1 --with-debugging=yes --with-scalar-type=complex --PETSC_ARCH=complex-debug

4. Optimized real build on a cluster with existing MPI. (For production runs on a cluster you *MUST* use an optimized build.)::

    $ ./configure --with-shared-libraries --download-superlu_dist --download-parmetis=yes --download-metis=yes --with-fortran-interfaces=1 --with-debugging=no --with-scalar-type=real --PETSC_ARCH=real-opt

5. Workstation debug build, downloading fblaslapack, real scalar type with MPI installed locally (see OpenMPI `user wide install`_ section)::

   $ ./configure --with-shared-libraries --download-superlu_dist --download-parmetis=yes --download-metis=yes --with-fortran-interfaces=1 --with-debugging=yes --with-scalar-type=real --download-fblaslapack --PETSC_ARCH=real-debug-gfortran-3.7.7 --with-mpi-dir=/home/<your-user-name>/packages/openmpi-1.10.7/opt-gfortran

.. NOTE::
   Note that the ``PETSC_ARCH`` option is any user specified
   string. Typically you should use something that is representative of
   the actual architecture.

Installation
************
After the configuration step, PETSc must be built. This is
accomplished with the command provided at the end of the configure
script. It will look something like below (the PETSc version should be consistent with the version being installed.)::

   $ make PETSC_DIR=$HOME/packages/petsc-3.7.7 PETSC_ARCH=real-debug all

The last step is to add ``PETSC_DIR`` and ``PETSC_ARCH`` entries to
your .bashrc file. You also must add an entry to ``LD_LIBRARY_PATH``
variable if you compiled MPI automatically with PETSc. This is
essential! It should look something like this: (Make sure the CORRECT
directory and name are used!))::

    # PETSc ARCH and DIR
    export PETSC_DIR=$HOME/packages/petsc-3.7.7
    export PETSC_ARCH=real-debug

    # Library Path for MPI
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib

    # Path for MPI -- configuration with MPI
    export PATH=$PETSC_DIR/$PETSC_ARCH/bin:$PATH
    export PATH=$PETSC_DIR/$PETSC_ARCH/include:$PATH

Make sure the .bashrc file is sourced before trying to compile any other code::

   $ source ~/.bashrc

Now that you have built a single PETSc build, you can configure other
architectures. Generally you will want an optimized architecture when
starting production runs.

.. NOTE::
   After the paths are setup above you do not
   need to use the ``--download-openmpi`` option again as PETSc will find
   the MPI already compiled.

`openmpi <http://www.open-mpi.org/>`_
-------------------------------------

.. NOTE::
   If openmpi was installed with PETSc there is no need to compile openmpi separately. However, if one will be using PETSc real and complex data you must compile it separately and not install it with PETSc.

`Download <https://download.open-mpi.org/release/open-mpi/v1.10/openmpi-1.10.7.tar.gz>`__ the source, put in your packages directory and untar::

   $ tar -xzf openmpi-1.10.7.tar.gz

System wide install
*******************
If not already in place add the following to your .bashrc

.. code-block:: bash

   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
   export PATH=/usr/local/bin:$PATH

To compile and install system wide openmpi you need to open a new terminal with root privileges and export the FC environmental variable to indicate which Fortran compiler. To configure and make and you will need to do the following

.. code-block:: bash

   sudo gnome-terminal
   source /home/<your_user_name>/.bashrc     # to get the the environment variables you need
   export FC=ifort                           # or FC=gfortran depending on your system
   cd /home/<your_user_name>/packages/openmpi-1.10.7
   ./configure
   make
   make install
   exit

User wide install
*****************
Installing for user only (recommended) allows for a easier and better control similar to different PETSc configuration and install. In practice multiple configurations are however not needed and in most cases this is only done once for the user. The user may want to upgrade MPI and can thus compile a new version easily in a similar manner and then change only the ``MPI_INSTALL_DIR`` environment variable in order to change MPI versions or builds.

Add the following to your .bashrc

.. code-block:: bash
   
   export MPI_INSTALL_DIR=$HOME/packages/openmpi-1.10.7/opt-gfortran
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
   export PATH=$MPI_INSTALL_DIR/bin:$PATH

Once you have saved the .bashrc then in a new command line window (or source the .bashrc file to update the variables) we can configure and install MPI. The important variable that has to be set is ``MPI_INSTALL_DIR``. To verify that it is set to the correct location do ``echo $MPI_INSTALL_DIR``. To configure and install do

.. code-block:: bash
   
   export FC=gfortran                       # or FC=ifort or other, depending on compiler used on system
   ./configure --prefix=$MPI_INSTALL_DIR
   make all install

To verify that paths are as expected run

.. code-block:: bash

   which mpicc
   echo $MPI_INSTALL_DIR/bin/mpicc

The above should print out the same path for both.



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



.. _install_cgns:

`CGNS Library <http://cgns.sourceforge.net>`_
---------------------------------------------

The CGNS library is used to provide CGNS functionality for :ref:`adflow`,
:ref:`pywarp`, and :ref:`pyhyp`. `Download
<http://cgns.sourceforge.net/download.html>`__ the latest version and
untar. The latest CGNS version (3.2) is recommended,
but the older versions of 3.1.x and 2.5.x may also be used. After
downloading, untar::

   $ tar -xzf cgnslib_3.2.1.tar.gz

.. WARNING::
   The 3.2.1 version fortran include file is bad. After
   untaring, manually edit the cgnslib_f.h.in file in the ``src``
   directory and remove all the comment lines at the beginning of the
   file starting with c. This may be fixed in subsequent versions.

.. NOTE::
   CGNS now supports two versions: One based on HDF5 and one based on
   the Advanced Data Format (ADF) format. While the HDF5 format is the
   officially supported one, most other software doesn't support HDF5
   files at all, and thus these files are practically
   useless. Furthermore, compiling HDF5 is a nightmare, (especially in
   parallel) and it is thus recommended that ADF format is used until
   further notice.

Since the CGNS lib (version 3.1 and up) use cmake for configuring the
build these programs also have to be installed. On a desktop, this can
be installed using.::

  sudo apt-get install cmake cmake-curses-gui

and it most likely already available as a module on a cluster.

Enter cgnslib_3.2.1 and type::

   $ cmake .

By default, the CGNS library does not include the Fortran bindings
that are required for MDOlab codes. This needs to be enabled using the
cmake configure utility, `ccmake`.::

   $ ccmake .

A "GUI" appears and toggle ENABLE_FORTRAN by pressing [enter] (should
be OFF when entering the screen for the first time, hence set it to ON). Type
'c' to reconfigure and 'g' to generate and exit.

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


Then build the library using::

   $ make

.. NOTE::
   **Optional**: If you compiled with the CGNS_BUILD_CGNSTOOLS flag ON you
   either need to add the binary path to your PATH environmental variable or
   you can install the binaries system wide. To do so issue the command::

   $ sudo make install

We also have to make the location of this library available to the
linker. To do this add the following line to your .bashrc file::

  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(HOME)/packages/cgnslib_3.2.1/src

Now, for pyHyp, ADflow, pyWarp and cgnsUtilities, the required include
flags and linking flags will be::

  CGNS_INCLUDE_FLAGS=-I$(HOME)/packages/cgnslib_3.2.1/src
  CGNS_LINKER_FLAGS=-L$(HOME)/packages/cgnslib_3.2.1/src -lcgns
