.. Documentation of a basic setup on the stampede2 cluster.
   Note that the user is assumed to have already gotten an account
   setup, and has access to the login nodes on the cluster.

.. _stampede2:

Stampede2 Cluster Setup
=======================

This guide is intended to help users get setup with the MDO Lab software on the Stampede 2 HPC system hosted at TACC. The first step is to create an XSEDE account on the XSEDE user portal:
https://portal.xsede.org

Once you have your XSEDE username setup, ask Prof. Martins to add you to the relevant allocation on XSEDE and confirm that you can log into the resource.

Connecting to the TACC servers
------------------------------

Read this article for instructions on accessing XSEDE resources for the single sign on hub.
https://portal.xsede.org/documentation-overview#access

Alternatively, you can directly ``ssh`` into stampede2 using

::

   ssh username@stampede2.tacc.utexas.edu

Setting up MDO Lab software
---------------------------
For most cluster setups, you need to follow the basic steps outlined in :ref:`installFromScratch`.

It is advised to install all the MDOlab code under ``$HOME/repos``. A few differences to note:

- :ref:`PETSc/MPI <install_petsc>` has already been compiled, so it's possible to omit them during the installation process, and load the required modules with, say, ``module load petsc/3.7``

- :ref:`mpi4py <install_mpi4py>` is installed by default, but :ref:`petsc4py <install_petsc4py>` still needs to be installed. Do a user install for all required python packages.

- When compiling TACS, make the following modification in Makefile.in before compiling: ``LAPACK_LIBS = -mkl``.

Example .bashrc
------------------
Load the correct modules in section 1, `within the if statement`

.. code-block:: bash

   module load git
   module load intel/17.0.4
   module load python/2.7.13
   module load petsc/3.7              # If you want to use pre-compiled PETSc

Environmental variables are placed in the if block under section 2:

.. code-block:: bash

   # PETSc ARCH and DIR (only needed if you are compiling PETSc)
   export PETSC_DIR=$HOME/packages/<PETSC LOCATION>
   export PETSC_ARCH=real-opt-intel

   # Library Path for MPI (only needed if you are compiling PETSc)
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib

   # Library Path for CGNSlib
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/cgnslib_3.2.1/src

   # Path for repos directories
   export PYTHONPATH=$PYTHONPATH:$HOME/repos/

   # Path for cgns utilities
   export PATH=:$HOME/repos/cgnsutilities/bin/:$PATH
   export PATH=:${HOME}/.local/bin:${PATH}

Lastly, the aliases are placed under section 3.

.. code-block:: bash

   # Aliases
   alias ls='ls --color=auto'
   alias myq='squeue -u <username>'
   alias emn='emacs -nw'
   alias jstat='scontrol show job'
   alias iknl='idev -n 68 -N 1 -m 120 -A TG-DDM140001'
   alias iskx='idev -p skx-dev -n 196 -N 4 -m 120 -A TG-DDM140001'
   alias myqq='showq -u'

Adjust directory names as needed. If you want to use the PETSc already compiled on stampede2, then you need to have ``module load petsc/3.7`` as mentioned above, and you no longer need the first three export statements.

Running Jobs
------------
Stampede2 uses Slurm rather than PBS (Moab or Torque). Also note that, it is generally advised to use SKX nodes rather than KNL for running MDOlab code, as they are more optimized for those architectures.

Example run script:

.. code-block:: bash

    #SBATCH -J job_name        # Job name
    #SBATCH -o myjob.o%j       # Name of stdout output file
    #SBATCH -e myjob.e%j       # Name of stderr error file
    #SBATCH -p skx-normal      # Queue (partition) name
    #SBATCH -N 5               # Total # of nodes
    #SBATCH -n 240             # Total # of mpi tasks
    #SBATCH -t 24:00:00        # Run time (hh:mm:ss)
    #SBATCH --mail-user=uniqname@umich.edu
    #SBATCH --mail-type=all    # Send email at begin and end of job
    #SBATCH -A TG-DDM140001    # Allocation name (req'd if you have more than 1)

    module list                # Lists the modules loaded
    pwd                        # Lists current working directory
    date                       # Lists date/time when file began running

    # Launch MPI code...

    ibrun python myscript.py   # ibrun is used instead of mpirun/mpiexec on stampede
