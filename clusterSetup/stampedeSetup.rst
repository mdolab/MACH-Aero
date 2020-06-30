.. Documentation of a basic setup on the stampede2 cluster.
   Note that the user is assumed to have already gotten an account
   setup, and has access to the login nodes on the cluster.

.. _stampede2:

Stampede2 Cluster Setup
=======================

This guide is intended to help users get setup with the MDO Lab software on the Stampede 2 HPC system hosted at TACC. The first step is to create an XSEDE account on the XSEDE user portal:
https://portal.xsede.org

Once you have your XSEDE username setup, ask Prof. Martins to add you to the relevant allocation on XSEDE and confirm that you can log into the resource.

.. NOTE ::

   It is strongly recommended to go through the `Stampede 2 user guide <https://portal.tacc.utexas.edu/user-guides/stampede2>`_ before you start operating on your account

Connecting to the TACC servers
------------------------------
You can directly ``ssh`` into stampede2 using::

   ssh username@stampede2.tacc.utexas.edu

Make sure to set up the multifactor authentication first (more info `here <https://portal.tacc.utexas.edu/tutorials/multifactor-authentication>`_).

Alternatively, read `this article <https://portal.xsede.org/documentation-overview#access>`_ for instructions on accessing XSEDE resources for the single sign on hub.
Using the XSEDE login allows you to use DUO two-factor authentication instead of using a dedicated app for TACC.

Home, Work and Scratch directories
----------------------------------

Similarly to Great Lakes and other HPCs, you can access different file systems from your Stampede account. To learn more about the different directory, read `this section <https://portal.tacc.utexas.edu/user-guides/stampede2#overview-filesystems>`_ of the user guide.

Use ``$HOME`` for ``packages`` and ``repos`` folders.
For our typical production jobs, with relatively limited storage and file I/O usage, it is fine to use the ``$WORK`` directory. It has a 1TB limit but it is never purged, while ``$SCRATCH`` has no storage limit but any file that is not executed or modified for more than 10 days will be deleted.

.. WARNING ::

   ``$SCRATCH`` purge might occur after more than 10 days but you will not be warned in advance, so be extra careful.

.. TIP ::

   It is good practice to always download or backup your output files as soon as the job is completed.

Data transfer
~~~~~~~~~~~~~

You can use `Globus <https://portal.xsede.org/data-management>`_ for data management and transfer. 
Conversely, you can use ` scp <https://portal.tacc.utexas.edu/user-guides/stampede2#transferring-scp>`_ from the terminal window.
For ``PuTTY`` users, this `PSFTP tutorial <https://www.ssh.com/ssh/putty/putty-manuals/0.68/Chapter6.html>`_ can be useful.

.. TODO : add file backup tips
.. TODO : using transfer nodes

Setting up MDO Lab software
---------------------------
For most cluster setups, you need to follow the basic steps outlined in :ref:`installFromScratch`.

Again, it is advised to install all the MDO Lab code under ``$HOME/repos``. A few differences to note:

- :ref:`PETSc/MPI <install_petsc>` have already been compiled, so it is strongly recommended to use the system MPI, and optionally the system PETSc. Load the required modules with, say, ``module load impi/18.0.2`` and ``module load petsc/3.11`` respectively.

- :ref:`mpi4py <install_mpi4py>` is installed by default, but :ref:`petsc4py <install_petsc4py>` still needs to be installed. Do a user install for all required python packages.

- When compiling TACS, make the following modification in Makefile.in before compiling: ``LAPACK_LIBS = -mkl``.

.. WARNING ::

   In case you encounter ``mkl`` errors like ``Intel MKL FATAL ERROR: Cannot load libmkl_avx512.so or libmkl_def.so.`` when running any of our runscripts, there is most likely some issue with PETSc and ``petsc4py``. It is recomended to install ``petsc4py`` locally using `these instructions <https://petsc4py.readthedocs.io/en/stable/install.html>`_ (files downloadable from the `Bitbucket repo <https://bitbucket.org/petsc/petsc4py/downloads/>`_), so you can test ``petsc4py`` locally. Try different PETSc versions in case the error persists.

Install CGNS
~~~~~~~~~~~~

The CGNS Library cannot be imported as a module in Stampede. You can refer to `this section of the docs <http://mdolab.engin.umich.edu/docs/installInstructions/install3rdPartyPackages.html#install-cgns>`_ for the installation procedure.

Be careful to set ``-DCGNS_BUILD_CGNSTOOLS = 0`` to skip the installation of cgnstools.
As you will use Intel compilers, you **must** set the compilers path by using these commands before configuring the build:

.. code-block :: bash

   export CC=$(which icc)
   export FC=$(which ifort)

CGNS will by default compile using the default ``/usr/bin/gcc``, which is not part of a specific module. This hard-coded path will most likely generate issues, as the rest of the code will be compiled by a different compiler. Setting the path as done above ensures that the compiler choice is consistent between CGNS and our codes, avoiding disruptive incompatibilities.


Example .bashrc
------------------
Load the correct modules in section 1, `within the if statement`, following the instructions on the default file in your ``$HOME`` directory.

.. code-block:: bash

   module load git/2.24.1
   module load intel/18.0.2
   module load impi/18.0.2
   module load petsc/3.11              # If you want to use pre-compiled PETSc

.. WARNING :: 

   Load a specific Python module only if you intend to use it. Having multiple python versions loaded (even if one is Python 2.x and the other is Python 3.x) can lead to ``$PYTHONPATH`` and packages conflicts.

Environmental variables are placed in the if block under section 2:

.. code-block:: bash

   # PETSc ARCH and DIR (only needed if you are compiling PETSc)
   export PETSC_DIR=$HOME/packages/<PETSC LOCATION>
   export PETSC_ARCH=real-opt-intel

   # -- CGNS
   export CGNS_HOME=$HOME/packages/CGNS-3.3.0/opt-gfortran
   export PATH=$PATH:$CGNS_HOME/bin
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

   # Path for repos directories - uncomment if not using pip to install MDO Lab codes
   # export PYTHONPATH=$PYTHONPATH:$HOME/repos/

   # Path for cgns utilities
   export PATH=:$HOME/repos/cgnsutilities/bin/:$PATH
   export PATH=:${HOME}/.local/bin:${PATH}

Lastly, the aliases are placed under section 3.

.. code-block:: bash

   # Aliases
   alias ls='ls --color=auto'
   alias myq='squeue -u <username>'
   alias labq='squeue -A TG-DDM140001'
   alias emn='emacs -nw'
   alias jstat='scontrol show job'
   alias iknl='idev -n 68 -N 1 -m 120 -A TG-DDM140001'
   alias iskx='idev -p skx-dev -n 48 -N 1 -m 120 -A TG-DDM140001'
   alias iskx2='idev -p skx-dev -n 96 -N 2 -m 120 -A TG-DDM140001'
   alias iskx4='idev -p skx-dev -n 192 -N 4 -m 120 -A TG-DDM140001'
   alias myqq='showq -u'
   alias strtime='squeue --start -j'  # <jobID>, check estimated startime of your job

Adjust directory names as needed. If you want to use the PETSc already compiled on stampede2, then you need to have ``module load petsc/3.11`` as mentioned above, and you no longer need the first three export statements.

.. NOTE ::

   ``TG-DDM140001`` refers to the MDO Lab allocation, it is not related to your specific user. You should not modify it unless you are accessing to another specific allocation.

Running Jobs
------------
Stampede2 uses Slurm as job scheduler. 
It is generally advised to use SKX nodes rather than KNL for running MDO Lab code, as they are more optimized for those architectures and can save substantial run time. 
SKX nodes have fewer (48) cores per node, but each core runs at a higher clock speed. KNL has more cores per node (68), but they all run at a lower speed.
Check the user guide for more `details <https://portal.tacc.utexas.edu/user-guides/stampede2#system-overview>`_

Example run script:

.. code-block:: bash
    
    #!/bin/bash
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

.. TIP ::

   Run an interactive job to test your scripts before you submit a regular job via ``sbatch``, especially since the queuing time can be substantially longer than Great Lakes or other HPCs. Note that the queue for SKX nodes is longer than KNL.

.. Queue and Prioritization system
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. Your jobs will most likely stay in the queue from several hours up to a day, depending on the resources you are requesting. 
.. Your priority in the queue depends on your usage.
.. It will go up if you are not a frequent user, reducing your queue time. If you try to use a lot of resources in a burst, then your priority will be significantly reduced and you might end up waiting unnecessarily long queues. 
.. The best approach is to keep your utilization of the system as constant as possible.

.. We do not have more specific tips for queuing and job requests, except for what already reported in the User guide. 
.. Don't ask for more resources than you actually need! You can get a glimpse of Stampede 2 current usage on this `system monitor <https://portal.tacc.utexas.edu/system-monitor>`_. 
.. Also note that the queue for SKX nodes is longer than KNL.

.. .. TIP ::

..    Interactive jobs are a useful resource. There is only a time limit (120 minutes) and you can request a high number of nodes. The queue time varies from few seconds to few minutes. Although it is not recommended to use these jobs for production (unless, for example, you have to run a set of quick ADflow runs), it is **strongly** recommended to test your run scripts here before you submit a regular job. You don't want to wait a day for your job to start and then have it crashing after a few seconds for some trivial coding mistake.
