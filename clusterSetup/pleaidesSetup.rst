.. Documentation of initial setup on the NASA Pleiades cluster.
   Note that the user is assumed to have already gotten an account
   setup, and has access to one of the pfe nodes on the cluster.
   Author: David Burdette (daburdet@umich.edu)
   Edited by: John Jasa (johnjasa@umich.edu)

.. _pleiades:

Pleiades Cluster Setup
======================

This guide is intended to assist users with setting up the MDOlab software
on the NASA Pleiades Cluster.  The user will first need to create a NAS
account and get access to the cluster. An overview of the Pleiades system
including current usage information can be found at
http://www.nas.nasa.gov/hecc/resources/pleiades.html and user documentation
for the cluster is available at http://www.nas.nasa.gov/hecc/support/kb/ .

Requesting a NAS account
------------------------

The process to add new users is as follows, as told by one of the NAS account administrators:

**If they do not already have a NASA Identity** (which is probably the case for your students), they will need to be approved by NASA Security. In this case, you will need to request a NASA Identity on their behalf by selecting option #3 at the following URL: https://www.nas.nasa.gov/hecc/portal/accounts. After their NASA Identity is approved by NASA Security, we will be in contact with them and will help them through the rest of the process.

**If they do already have a NASA Identity**, they will not need their account approved by NASA Security. In this case, they can request a NAS account directly online by selecting option #2 at the same URL: https://www.nas.nasa.gov/hecc/portal/accounts (they will need to know your GID# for this step).

This means that you need to ask Professor Martins for the GID# for the NAS account.


Connecting to the NAS servers
-----------------------------

Read this article for details of how to connect to NAS:
https://www.nas.nasa.gov/hecc/support/kb/two-step-connection-using-public-key-and-securid-passcode_231.html

To make connecting more convenient, you should also set up public key authentication
and SSH passthrough so you don't have to type as many passwords.
Read more about setting up a public key here
https://www.nas.nasa.gov/hecc/support/kb/setting-up-public-key-authentication_230.html
and about SSH passthrough here
https://www.nas.nasa.gov/hecc/support/kb/setting-up-ssh-passthrough_232.html .

Note that any time the terminal prompts you for your password, it's a
password that you've selected, while the PASSCODE is the series of digits
from your authentication device (either your key fob or phone app).

.. note::

    Although a bit confusing, SFE is a portal to PFE, which is where
    you actually move and store files. So you first SSH into SFE
    then SSH into PFE from SFE. On PFE you can store your repos
    and packages directories and files.

When logged onto PFE, you can perform the following command:

::

    cd /nobackup/<username>

where <username> is your NAS username to access the 'scratch' directory.
This is where you store run scripts and where your output files will be saved.
Note that this is called nobackup for a reason -- it periodically gets erased
and is not meant for long-term storage.

Building Numpy and Python3 on Pleiades
--------------------------------------

Seems like there are problems with the default numpy installation on Pleiades.
The codes run, but there are some weird performance issues.
To avoid these problems, users can build their own numpy, along with Python3 on Pleiades, using spack.

This part of the guide is based on a GoogleDoc created by Kenneth Moore, Justin Gray, and possibly other authors from NASA.

All the compilation we have here can be done on the login nodes, you don't need to access a compute node for these.

IMPORTANT: After you follow these instructions, even if you had a working build of the repos you are using, you should build all of them again with ``make clean & make``.

Steps to build Python 3.6
^^^^^^^^^^^^^^^^^^^^^^^^^

Clone spack in your home directory

::

    git clone https://github.com/LLNL/spack

Create a ``~/.spack/packages.yaml`` file.
In this file, you should use spaces instead of tabs for indenting the text.
The file should contain the following:

::

    packages:
      openssl:
          # Use the system-provided OpenSSL
          paths:
              openssl@1.0.1e arch=linux-rhel6-x86_64: /usr
              openssl@1.0.2j arch=linux-sles12-x86_64: /usr
          buildable: False
      python:
          version: [3.6.2]
      py-numpy:
          version: [1.12.1]

Then do
::

    module purge
    cd spack
    bin/spack install -j 4 py-scipy
    bin/spack install -j 4 py-cython

This may take a while.

Check if it worked:

::

    export SPACK_ROOT=$PWD
    . share/spack/setup-env.sh
    spack load python
    spack load py-numpy
    spack load py-scipy

At this point, you have your own python, numpy, and scipy installations under the spack environment.

Example .bashrc
::

    # These commands are executed on a login or start of a PBS job.
    # First, run the NAS standard setup.

    if [ -e /usr/local/lib/init/global.profile ]; then
           . /usr/local/lib/init/global.profile
    fi

    # Add your commands here to extend your PATH, etc.


    # Load what modules are left
    module load mpi-sgi/mpt
    module load comp-intel
    module load pkgsrc

    # NOTE from Ken: This is a problem.
    # you won’t be able to build smt if you load this module.
    # Could make an argument for either not loading it ever,
    # or loading it before building the spack stack. I am not
    # sure which version of gcc is better for what.
    # default is 4.x; module load is 6.x
    module load gcc

    export PYTHONUNBUFFERED=True


    # stuff for ADflow
    export PYTHONPATH=$PYTHONPATH:$HOME/repos/
    export PATH=$PATH:${HOME}/.local/bin
    export PATH=$PATH:${HOME}/repos/cgnsutilities/bin/
    export PATH=$PATH:${HOME}/packages/cloc-1.64/
    export PETSC_DIR=$HOME/packages/petsc/

    export PETSC_ARCH=real-opt-intel
    #export PETSC_ARCH=real-debug-intel

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/cgnslib_3.2.1/src

    # More useful aliases.
    alias myjobs='qstat -u $YOUR_USERNAME$'
    alias emacs='emacs -nw'
    alias ls='ls --color=auto'
    alias san16='qsub -I -q devel -lselect=1:ncpus=16:model=san,walltime=1:00:00'
    alias ivy20='qsub -I -q devel -lselect=1:ncpus=20:model=ivy,walltime=1:00:00'
    alias ivy40='qsub -I -q devel -m b -lselect=2:ncpus=20:model=ivy,walltime=2:00:00'
    alias ivy60='qsub -I -q devel -m b -lselect=3:ncpus=20:model=ivy,walltime=1:00:00'
    alias ivy80='qsub -I -q devel -m b -lselect=4:ncpus=20:model=ivy,walltime=1:00:00'
    alias has24='qsub -I -q devel -lselect=1:ncpus=24:model=has,walltime=0:30:00'
    alias ivy40n='qsub -I -q normal -m b -lselect=2:ncpus=20:model=ivy,walltime=2:00:00'
    alias shares='qstat -W shares=-'

    alias bro28='qsub -I -q devel -lselect=1:ncpus=28:model=bro,walltime=0:30:00'
    alias bro1_devel='qsub -I -q devel -m b -lselect=1:ncpus=28:model=bro,walltime=2:00:00'
    alias bro2_devel='qsub -I -q devel -m b -lselect=2:ncpus=28:model=bro,walltime=2:00:00'
    alias bro2_mem='qsub -I -q devel -m b -lselect=2:ppn=10:model=bro,walltime=1:00:00'


    # Finally put the ~/bin dir at the beginning where we fix all
    # the pkgsrc stuff
    PATH=$HOME/bin:$PATH

    # weird stuff that numpy seems to want!
    export MPI_UNBUFFERED_STDIO=true
    export OMP_NUM_THREADS=1


    # use the spack build for python
    export SPACK_ROOT=${HOME}/spack
    . ${HOME}/spack/share/spack/setup-env.sh
    spack load python
    spack load py-numpy
    spack load py-scipy
    spack load py-cython

.. note::
    After this step, you might have issues with gcc.
    If you have these, you can add ``CC=icc CXX=icc`` before the command to try again with the intel compilers.
    Do not define these as environment variables, because this might break some other code that has to be compiled with gcc, like pyoptsparse.

Create a symlink for ``python`` pointing to the spack python.
To do this, there are a few steps:
First, in your home directory, make a folder called ``bin`` with

::

    cd ~
    mkdir bin

Now, we need to figure out where spack installed python.
For this, do:

::

    which python

This should print the directory where the python executable we installed with spack is.
This will look something like:

::

    /home1/ayildiri/spack/opt/spack/linux-sles12-x86_64/gcc-4.8/python-3.6.2-4t2uzuuk3mc5iohwyqkizo5tn4bqkn7m/bin/python3.6

To create the symlink for python, copy this directory and use it instead of ``$SOURCE`` in the command below:

::

    ln -s $SOURCE $HOME/bin/python

Similarly, creating a symlink for f2py and f2py3.6 is required.
You can put these symlinks in ``~/bin/``.
To do so, we again need to locate where the spack installed f2py is.
The f2py executable will be located under where py-numpy is installed under spack.
To locate this, you can look into the directory where the spack installed python is.
In that directory, the different packages are installed under the folder that starts with ``gcc``.
After you have found this location, go into the folder that starts with py-numpy, and the f2py3.6 executable will be located in the bin folder there.
Simply copy the path to f2py3.6 there, and use it instead of the $SOURCE below:

::

    ln -s $SOURCE $HOME/bin/f2py
    ln -s $SOURCE $HOME/bin/f2py3.6


At this point you should log out and log back in to get a clean shell environment.
You did a ``module purge`` and that causes bad things for the rest of the build.
Get a new shell with a clean module load from your ``.bashrc``.

Note from Ken : pip and setuptools seem to be broken in the spack packages.
At this point, I had to clone their repos and install both from source.

Building OpenMDAO
^^^^^^^^^^^^^^^^^

You can put these stuff in your ``~/packages``.
Also, make sure to remove any of the previous builds of these packages if you have any.
To do this, you can simply remove the whole folder with ``rm -f ./FOLDER_NAME`` as we will be cloning them from the source.

Clone mpi4py repo from https://bitbucket.org/mpi4py/mpi4py and checkout the 2.0.0 tag with

::

    git clone https://bitbucket.org/mpi4py/mpi4py.git
    cd ./mpi4py
    git checkout 2.0.0

Then do
::

    python setup.py install

Clone petsc repo from https://bitbucket.org/petsc/petsc, and checkout the v3.7.5 tag with:

::

    git clone https://bitbucket.org/petsc/petsc.git
    cd ./petsc
    git checkout v3.7.5

To configure petsc:

Note 1: configure can only be run from python 2:

Note 2: ``PETSC_DIR`` in ``.bashrc`` must point to this folder before configuring.

::

    python2 ./configure --with-shared-libraries --with-fortran-interfaces=1 --with-debugging=no --with-petsc-arch=real-opt-intel --download-fblaslapack=1 --with-ssl=0

Follow instructions that are printed to the terminal after petsc configures to build petsc.

Clone the petsc4py repo from https://bitbucket.org/petsc/petsc4py, and checkout the 3.7.0 tag with

::

    git clone https://bitbucket.org/petsc/petsc4py.git
    cd ./petsc4py
    git checkout 3.7.0

Then do
::

    python setup.py install

At this point, you should also install pip, because it may be broken with the spack python build.
To do this, just execute following commands:

::

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py

Clone OpenMDAO with

::

    git clone https://github.com/OpenMDAO/OpenMDAO.git


and do
::

    pip install -e .


.. note::
    Update from Ken
    We know this revision is working: 2077:1311e20b7e96

    Update to Latest: repos pull -u
    Roll back to original: repos checkout 2077

    Always make clean followed by make

    MYSTERY from Ken:
    Did justin load the gcc module before building the spack python stack?
    It certainly would explain things. However, it is not part of these
    Instructions, and I didn’t try it (which led to alternative solution detailed in bashrc)

Build Swig
----------

You will need swig to compile some python applications that also use C/C++ language.
Since we now have our own python, the default swig available on the system does not work properly.
First, you need to get a tarball from the `Swig download page <http://www.swig.org/download.html>`_.
You can follow the `Unix installation guide <http://www.swig.org/Doc3.0/Preface.html#Preface_unix_installation>`_ available on swig's website to build your own.
Then, you can build swig directly into ``~/bin/`` by doing

::

    ./configure --prefix=$HOME/bin/
    make
    make install

After that, you should add this to your path by adding

::

    # add the path for swig if you compiled your own
    export PATH=$HOME/bin/swig/bin:$PATH

to your ``.bashrc``.

Build OpenVSP on Pleiades
-------------------------

There are a number of tricks to get OpenVSP compiled properly without the GUI on Pleiades.
We will be mostly following the `instructions for Ubuntu 16.04 on OpenVSP's wiki page <http://openvsp.org/wiki/doku.php?id=ubuntu_instructions>`_, but with some minor modifications.
You can install this under your ``~/packages/``.

::

    mkdir OpenVSP

    cd OpenVSP
    mkdir repo build buildlibs

    git clone https://github.com/OpenVSP/OpenVSP.git repo

Before we start building, we need to specify which python version we are using so that cmake grabs the correct one while building the python api.
To do this, you need to edit the file `OpenVSP/repo/src/python_api/CMakeLists.txt`.
On the 8th line of that file, there is a check for swig that looks like this:
::

    IF( SWIG_FOUND )
            INCLUDE(${SWIG_USE_FILE})
            FIND_PACKAGE(PythonLibs)
    ENDIF( SWIG_FOUND )

Below the ``INCLUDE(#{SWIG_USE_FILE})`` command, you should include a line specifying the python version you want to use.
For example, if you have installed Python3.6 with spack, this should look like:

::

    IF( SWIG_FOUND )
            INCLUDE(${SWIG_USE_FILE})
            SET(Python_ADDITIONAL_VERSIONS 3.6)
            FIND_PACKAGE(PythonLibs)
    ENDIF( SWIG_FOUND )

Now, you are ready to build the libraries OpenVSP uses.
Follow these instructions:

::

    cd buildlibs

    CC=icc CXX=icc cmake -DCMAKE_BUILD_TYPE=Release -DVSP_USE_SYSTEM_FLTK=false -DVSP_USE_SYSTEM_CPPTEST=false -DVSP_USE_SYSTEM_LIBXML2=true -DVSP_USE_SYSTEM_EIGEN=false -DVSP_USE_SYSTEM_FLTK=false -DVSP_USE_SYSTEM_GLM=true -DVSP_USE_SYSTEM_GLEW=true -DVSP_USE_SYSTEM_CMINPACK=false ../repo/Libraries -DCMAKE_BUILD_TYPE=Release -DVSP_NO_GRAPHICS=true

    make -j8

Another useful modification is to change some of these libraries.
When you are projecting points onto a geometry, the code will hijack your stdout and may print useless statements because some internal projection condition is not met.
To disable these, you can comment the lines in the Code-Eli library.
To do so, you first need to build the libs, as Code-Eli only consists of header files that OpenVSP build uses.
This also means that this modification is undone everytime you re-build the libraries from scratch.
These ``cout`` statements are found in the file ``OpenVSP/buildlibs/CODEELI-prefix/src/CODEELI/include/eli/geom/intersect/minimum_distance_curve.hpp``.
To disable this output, you can comment lines 55, 60, 82, and 87.
Because CodeELI only consists of header files OpenVSP uses, this modification will be reflected in your build when you build OpenVSP itself.
If you re-make the buldlibs, this change will be lost, as the makefile makes a clean copy of this file included within a tarball that comes with the OpenVSP repo.

Finally, to build OpenVSP itself,

::

    cd ../build

    CC=icc CXX=icc cmake ../repo/src/ -DVSP_LIBRARY_PATH=$HOME/packages/OpenVSP/buildlibs -DCMAKE_BUILD_TYPE=Release -DVSP_NO_GRAPHICS=true

    make -j8

    make package

We need to set our path variables to access the python interface.
You can simply add these lines to your ``.bashrc``:

::

    export PYTHONPATH=$PYTHONPATH:$HOME/packages/OpenVSP/build/python_api

Example .bashrc
---------------

Here is an example .bashrc file to use if you will just use the system python and numpy.
Furthermore, even if you have installed your own python and numpy, you can still grab some usefull stuff from this ``.bashrc``, so we will keep it here for redundancy.

::

    # $Header: /cvsroot/bcfg2/bcfg2/Cfg/etc/skel_NAS/.profile/.profile,v 1.1 2009/12/11 16:05:13 dtalcott Exp $
    # These commands are executed on a login or start of a PBS job.
    # First, run the NAS standard setup.

    if [ -e /usr/local/lib/init/global.profile ]; then
        . /usr/local/lib/init/global.profile
    fi

    # # Add your commands here to extend your PATH, etc.
    # =========== THIS WORKS WITH SLES 12 ==========

    module load pkgsrc
    module load gcc
    module load /nasa/intel/Compiler/2017.1.132/2017.1.132.modulefile
    module load mpi-sgi/mpt.2.15r20
    module load python/2.7.12

    # ==============================================

    export PYTHONPATH=$PYTHONPATH:$HOME/repos/
    export PATH=:${HOME}/.local/lib/python2.7/site-packages/mpi4py/bin:${PATH}
    export PATH=$PATH}:${HOME}/repos/tacs/extern/f5totec
    export PATH=$PATH:$HOME/repos/cgnsutilities/bin
    export PETSC_DIR=$HOME/packages/petsc-3.7.3/
    export PETSC_ARCH=real-opt-intel
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/cgnslib_3.2.1/src

    alias scq='qstat -u  <email>'
    alias ls='ls --color=auto'
    alias emn='emacs -nw'
    alias ytd='acct_ytd -c all'
    #alias qlist='qstat -W o=+model,mission,pri -i'

    export $EMAIL='<email@umich.edu>'

    alias ivy40_120='qsub -I -q debug -m b -lselect=2:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'
    alias ivy40_30='qsub -I -q debug -m b -lselect=2:ncpus=20:model=ivy,walltime=0:30:00 -M $EMAIL'
    alias ivy40n='qsub -I -q normal -m b -lselect=2:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'

    alias ivy1_devel='qsub -I -q devel -m b -lselect=1:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'
    alias ivy2_devel='qsub -I -q devel -m b -lselect=2:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'
    alias ivy3_devel='qsub -I -q devel -m b -lselect=3:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'
    alias ivy4_devel='qsub -I -q devel -m b -lselect=4:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'
    alias ivy5_devel='qsub -I -q devel -m b -lselect=5:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'
    alias ivy6_devel='qsub -I -q devel -m b -lselect=6:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'
    alias ivy7_devel='qsub -I -q devel -m b -lselect=7:ncpus=20:model=ivy,walltime=2:00:00 -M $EMAIL'

    alias has1_devel='qsub -I -q devel -m b -lselect=1:ncpus=24:model=has,walltime=2:00:00 -M $EMAIL'
    alias has2_devel='qsub -I -q devel -m b -lselect=2:ncpus=24:model=has,walltime=2:00:00 -M $EMAIL'
    alias has3_devel='qsub -I -q devel -m b -lselect=3:ncpus=24:model=has,walltime=2:00:00 -M $EMAIL'
    alias has4_devel='qsub -I -q devel -m b -lselect=4:ncpus=24:model=has,walltime=2:00:00 -M $EMAIL'
    alias has5_devel='qsub -I -q devel -m b -lselect=5:ncpus=24:model=has,walltime=2:00:00 -M $EMAIL'
    alias has6_devel='qsub -I -q devel -m b -lselect=6:ncpus=24:model=has,walltime=2:00:00 -M $EMAIL'
    alias has7_devel='qsub -I -q devel -m b -lselect=7:ncpus=24:model=has,walltime=2:00:00 -M $EMAIL'

    alias bro1_devel='qsub -I -q devel -m b -lselect=1:ncpus=28:model=bro,walltime=2:00:00 -M $EMAIL'
    alias bro2_devel='qsub -I -q devel -m b -lselect=2:ncpus=28:model=bro,walltime=2:00:00 -M $EMAIL'
    alias bro3_devel='qsub -I -q devel -m b -lselect=3:ncpus=28:model=bro,walltime=2:00:00 -M $EMAIL'
    alias bro4_devel='qsub -I -q devel -m b -lselect=4:ncpus=28:model=bro,walltime=2:00:00 -M $EMAIL'
    alias bro5_devel='qsub -I -q devel -m b -lselect=5:ncpus=28:model=bro,walltime=2:00:00 -M $EMAIL'
    alias bro6_devel='qsub -I -q devel -m b -lselect=6:ncpus=28:model=bro,walltime=2:00:00 -M $EMAIL'
    alias bro7_devel='qsub -I -q devel -m b -lselect=7:ncpus=28:model=bro,walltime=2:00:00 -M $EMAIL'


The first portion should provide all of the environment changes
required to allow use of the MDOlab software. The latter half contains  additional
aliased commands which are helpful when operating on Pleiades. Note that
the user will need to adjust ``<email@umich.edu>`` in the script below.

Next, add the following line the end of your ``.profile`` file,
in the same home directory as your ``.bashrc`` file.
This will correctly source the ``.bashrc`` file when you start a new terminal session.

::

    source ~/.bashrc

Example MPI file
----------------

In addition to the ``.bashrc`` file in your home directory, you also need an ``mpi.cfg`` file in your home directory.
Here is a sample one that was confirmed to work in September 2017:

::

    # Some Linux distributions have RPM's for some MPI implementations.
    # In such a case, headers and libraries usually are in default system
    # locations, and you should not need any special configuration.

    # If you do not have MPI distribution in a default location, please
    # uncomment and fill-in appropriately the following lines. Yo can use
    # as examples the [mpich2], [openmpi],  and [deinompi] sections
    # below the [mpi] section (wich is the one used by default).

    # If you specify multiple locations for includes and libraries,
    # please separate them with the path separator for your platform,
    # i.e., ':' on Unix-like systems and ';' on Windows


    # Default configuration
    # ---------------------
    [mpi]

    define_macros = SGI_MPI=1
    mpi_dir       = /nasa/sgi/mpt/2.15r20
    mpicc         = mpicc
    mpicxx        = mpicxx
    include_dirs  = %(mpi_dir)s/include
    libraries     = mpi
    library_dirs  = %(mpi_dir)s/lib
    runtime_library_dirs = %(library_dirs)s

    ## mpi_dir              = /usr
    ## mpi_dir              = /usr/local
    ## mpi_dir              = /usr/local/mpi
    ## mpi_dir              = /opt
    ## mpi_dir              = /opt/mpi
    ## mpi_dir =            = $ProgramFiles\MPI

    ## mpicc                = %(mpi_dir)s/bin/mpicc
    ## mpicxx               = %(mpi_dir)s/bin/mpicxx

    ## define_macros        =
    ## undef_macros         =
    ## include_dirs         = %(mpi_dir)s/include
    ## libraries            = mpi
    ## library_dirs         = %(mpi_dir)s/lib
    ## runtime_library_dirs = %(mpi_dir)s/lib

    ## extra_compile_args   =
    ## extra_link_args      =
    ## extra_objects        =



    # MPICH2 example
    # --------------
    [mpich2]
    mpi_dir              = /home/devel/mpi/mpich2-1.4.1
    mpicc                = %(mpi_dir)s/bin/mpicc
    mpicxx               = %(mpi_dir)s/bin/mpicxx
    #include_dirs         = %(mpi_dir)s/include
    #libraries            = mpich opa mpl
    #library_dirs         = %(mpi_dir)s/lib
    #runtime_library_dirs = %(library_dirs)s


    # Open MPI example
    # ----------------
    [openmpi]
    mpi_dir              = /home/devel/mpi/openmpi-1.5.4
    mpicc                = %(mpi_dir)s/bin/mpicc
    mpicxx               = %(mpi_dir)s/bin/mpicxx
    #include_dirs         = %(mpi_dir)s/include
    #libraries            = mpi
    library_dirs         = %(mpi_dir)s/lib
    runtime_library_dirs = %(library_dirs)s


    # Sun MPI example
    # ---------------
    [sunmpi]
    #mpi_dir              = /opt/SUNWhpc/HPC8.2.1/gnu
    mpi_dir              = /opt/SUNWhpc/HPC8.1/sun
    mpicc                = %(mpi_dir)s/bin/mpicc
    mpicxx               = %(mpi_dir)s/bin/mpicxx
    #include_dirs         = %(mpi_dir)s/include
    #libraries            = mpi open-rte open-pal
    library_dirs         = %(mpi_dir)s/lib
    runtime_library_dirs = %(library_dirs)s


    # HP MPI example
    # --------------
    [hpmpi]
    mpi_dir              = /opt/hpmpi
    mpicc                = %(mpi_dir)s/bin/mpicc
    mpicxx               = %(mpi_dir)s/bin/mpiCC
    #include_dirs         = %(mpi_dir)s/include
    #libraries            = hpmpio hpmpi dl
    #library_dirs         = %(mpi_dir)s/lib
    #runtime_library_dirs = %(library_dirs)s


    # SGI MPI example
    # ---------------
    [sgimpi]
    define_macros = SGI_MPI=1
    mpi_dir       = /usr
    mpicc         = icc
    mpicxx        = icpc
    include_dirs  = %(mpi_dir)s/include
    libraries     = mpi
    library_dirs  = %(mpi_dir)s/lib
    runtime_library_dirs = %(library_dirs)s


    # IBM POE/MPI example
    # -------------------
    [poempi]
    mpicc  = mpcc_r
    mpicxx = mpCC_r


    # MPICH2 example (Windows)
    # ------------------------
    [mpich2-win32]
    mpi_dir = $ProgramFiles\MPICH2
    include_dirs = %(mpi_dir)s\include
    libraries = mpi
    library_dirs = %(mpi_dir)s\lib


    # Open MPI example (Windows)
    # -------------------------
    [openmpi-win32]
    mpi_dir = $ProgramFiles\OpenMPI_v1.5.4-win32
    define_macros = OMPI_IMPORTS
    include_dirs = %(mpi_dir)s\include
    libraries = libmpi
    library_dirs = %(mpi_dir)s\lib


    # DeinoMPI example
    # ----------------
    [deinompi]
    mpi_dir = $ProgramFiles\DeinoMPI
    include_dirs = %(mpi_dir)s\include
    libraries = mpi
    library_dirs = %(mpi_dir)s\lib


    # Microsoft MPI example
    # ---------------------
    [msmpi]
    mpi_dir = $ProgramFiles\Microsoft HPC Pack 2008 SDK
    include_dirs = %(mpi_dir)s\include
    libraries = msmpi
    library_dirs = %(mpi_dir)s\lib\i386
    #library_dirs = %(mpi_dir)s\lib\amd64


    # SiCortex MPI example
    # --------------------
    [sicortex]
    mpicc = mpicc --gnu
    mpicxx = mpicxx --gnu


    # LAM/MPI example
    # ---------------
    [lammpi]
    mpi_dir              = /home/devel/mpi/lam-7.1.4
    mpicc                = %(mpi_dir)s/bin/mpicc
    mpicxx               = %(mpi_dir)s/bin/mpic++
    include_dirs         = %(mpi_dir)s/include
    libraries            = lammpio mpi lam
    library_dirs         = %(mpi_dir)s/lib
    runtime_library_dirs = %(library_dirs)s

    # MPICH1 example
    # --------------
    [mpich1]
    mpi_dir              = /home/devel/mpi/mpich-1.2.7p1
    mpicc                = %(mpi_dir)s/bin/mpicc
    mpicxx               = %(mpi_dir)s/bin/mpicxx
    include_dirs         = %(mpi_dir)s/include
    libraries            = mpich
    library_dirs         = %(mpi_dir)s/lib/shared:%(mpi_dir)s/lib
    runtime_library_dirs = %(mpi_dir)s/lib/shared


    # Fake MPI, just for testing
    # --------------------------
    [fakempi]
    mpicc         = cc
    mpicxx        = c++
    include_dirs  = misc/fakempi


3rd party packages
------------------
A number of required packages are included in the modules loaded in the
example ``.bashrc`` above, including:

#. Python
#. Valgrind
#. cmake
#. Numpy
#. openmpi
#. BLAS & LAPACK

The :ref:`install_petsc`, :ref:`install_mpi4py`, :ref:`install_petsc4py`,
and :ref:`install_cgns` libraries will need to be installed by the user.
The petsc4py and cgns installations directly follow the general guidelines
provided in their install guides linked above. Some notes for the
installation of PETSc and mpi4py specifically on Pleiades are given below.

A number of configurations are available for the installation of
:ref:`install_petsc`. The user is advised to select relevant configuration
options, but a tested baseline to start from on Pleiades is:

::

    ./configure --with-shared-libraries --with-fortran-interfaces=1 -with-debugging=no
    --with-petsc-arch=real-opt-intel -download-fblaslapack=1 --with-ssl=0

There are a number of changes the user may need to make to this configuration
setup, including but not limited to:

- Add debugging for non-production runs
- Add superlu, parmetis, and metis if using pywarp (but these aren't needed for pywarpustruct)

There are many other configuration changes that may be needed depending
on the software you'll be using, but they will not be considered here.
We recommend PETSc version 3.7.3 since it has been confirmed to work with
the MDOlab codebase.

After installation of mpi4py, an adjustment is required in
``~/.local/lib/python2.7/site-packages/mpi4py/include/mpi4py/mpi4py.MPI_api.h``
to provide compatibility with TACS. In mpi4py 1.3.1, lines 135-145 of that
file should be commented out. Other versions of mpi4py have not been tested,
and the user is advised to use 1.3.1 at this point.


MDOlab packages
---------------

Most of the MDOlab packages can be installed using the basic instructions
given in the documentation.  A few packages have specific settings that
are required for Pleiades, as detailed below.

TACS Makefile.in
................

As usual, the user will copy the ``Makefile.in.info`` to ``Makefile.in``.
A few changes are required to compile TACS on Pleiades. The user should
remove the default ``LAPACK_LIBS`` definition from ``Makefile.in`` and
add the following:

::

	MKLPATH=${MKLROOT}/lib/intel64
	MKL_LIBS = -Wl,--start-group ${MKLPATH}/libmkl_intel_lp64.a ${MKLPATH}/libmkl_sequential.a ${MKLPATH}/libmkl_core.a -Wl,--end-group -lpthread

	LAPACK_LIBS = -limf ${MKL_LIBS}



EXAMPLE PBS Script
------------------

Below is an example PBS script for Pleiades.  This script requests 2 20 core
ivy bridge nodes (for 40 cores total) for 1 minute.  The example includes the
current group_list account for the MDOlab. Also note that this script submits a
job to the devel queue. For more information about the options for the PBS script,
consult man qsub or http://www.nas.nasa.gov/hecc/support/kb/commonly-used-qsub-options-in-pbs-scripts-or-in-the-qsub-command-line_175.html
for a partial list of common options.

::

        #PBS -S /bin/bash
	#PBS -N testCaseAS
	#PBS -l select=2:ncpus=20:model=ivy
	#PBS -l walltime=0:01:00
	#PBS -j oe
	#PBS -W group_list=a1556
	#PBS -m bae
	#PBS -q devel

	source ~/.bashrc

	cd repos/mdo_tutorial/as_opt/

	mpiexec python-mpi as_opt.py
