.. Documentation of a basic setup on the flux cluster.
   Note that the user is assumed to have already gotten an account
   setup, and has access to the login nodes on the cluster.

.. _Great Lakes:

GreatLakes Cluster Setup
========================
This guide is intended to assist users with setting up the MDOlab software
on the UMich GreatLakes Cluster.  The user will first need to create an account
and get access to the cluster. GreatLakes requires an on-campus connection, which can be provided by UMVPN (see :ref:`settingUpUMVPN` for setup instructions). An alternative is to first ``ssh`` into ``login.itd.umich.edu``, which does not require an on-campus connection, then from there ``ssh`` on to ``greatlakes.arc-ts.umich.edu``. It is recommended to save these commands as aliases or bash scripts for convenience.

Great Lakes users manual is at:
https://arc-ts.umich.edu/greatlakes/

A ``gcc``-based installation is recommended. The compiler/MPI versions can be found in the ``.bashrc`` below.
Intel-based installs are possible, with ``intel/18.0.5`` and ``impi/2018.4.274``. However, the setup is significantly more complicated.

Example .bashrc
---------------

Here is an example .bashrc file. You may need to create this in your
home directory on Great Lakes.

.. code-block:: bash

   # .bashrc

   # Source global definitions
   if [ -f /etc/bashrc ]; then
        . /etc/bashrc
   fi

   module load python2.7-anaconda/2019.03
   module load gcc/4.8.5
   module load openmpi/3.1.4
   module load cmake/3.13.2


   # add the repos directory to your python path so that the mdolab modules will be available
   export PYTHONPATH=$PYTHONPATH:$HOME/repos/

   # CGNS
   # Follow the 3rd party package installation tutorial to add the correct PATH
   export CGNS_HOME=$HOME/packages/CGNS-3.3.0
   export PATH=$PATH:$CGNS_HOME/bin
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib


   # PETSc
   export PETSC_DIR=${HOME}/packages/<petsc-version>
   export PETSC_ARCH=real-opt
   export PATH=${PATH}:${HOME}/repos/tacs_orig/extern/f5totec
   export PATH=$PATH:$HOME/repos/cgnsutilities/bin

   # Convenient env variables
   export SCRATCH=/scratch/jrram_root/jrram1/$USER

   # User specific aliases and functions
   alias squ='squeue -u $USER'
   alias sqj='squeue -A jrram1'
   alias scr="cd $SCRATCH"
   alias billing='sreport -T billing cluster AccountUtilizationByUser Accounts=jrram1 Start=$(date '+%Y-%m-01') End=now'
   alias utilization='sreport cluster Utilization -t percent End=$(date +%H:%M) Start=$(date +%H:%M -d "2 hours ago")'

   alias debug8='srun --account=jrram1 --nodes=1 --ntasks-per-node=8 --mem-per-cpu=5GB --time=4:00:00 --partition=standard --cpus-per-task=1 --pty /bin/bash'
   alias debug36='srun --account=jrram1 --nodes=1 --ntasks-per-node=36 --mem-per-cpu=5GB --time=4:00:00 --partition=standard --cpus-per-task=1 --pty /bin/bash'
   alias debug72='srun --account=jrram1 --nodes=2 --ntasks-per-node=36 --mem-per-cpu=5GB --time=4:00:00 --partition=standard --cpus-per-task=1 --pty /bin/bash'   
   alias debug108='srun --account=jrram1 --nodes=3 --ntasks-per-node=36 --mem-per-cpu=5GB --time=4:00:00 --partition=standard --cpus-per-task=1 --pty /bin/bash'

   
This file starts by specifying the preset modules you want to load.
This is followed by a section setting the environment variables to allow the use of the MDOlab software.
The last portion of the file specifies a series of aliases to make some standard operations easier.

Example Batch Script
--------------------

Below is an example Batch script for Great Lakes.

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=<job-name>        # unique identifier for the job
   #SBATCH --mail-user=<email>          # email address to send notification
   #SBATCH --mail-type=BEGIN,END,FAIL   # when to notify, pick from NONE, BEGIN, END, FAIL, REQUEUE, ALL
   #SBATCH --nodes=1                    # number of nodes
   #SBATCH --ntasks-per-node=36         # number of CPU-cores per node, max is 36 for GL
   #SBATCH --mem-per-cpu=5GB            # memory per CPU core
   #SBATCH --time=100:00:00             # recommended formats: MM:SS, HH:MM:SS, DD-HH:MM
   #SBATCH --account=jrram1             # the billing account
   #SBATCH --partition=standard         # typically either standard or debug

   source ~/.bashrc
   # The application(s) to execute along with its input arguments and options:
   mpirun -np 36 python opt.py

.. note::
   #. By default Slurm does not source the files ``~./bashrc`` or ``~/.profile``.

   #. You can use any of ``srun``, ``mpirun`` or ``mpiexec`` commands to start your MPI job. In most cases, ``mpirun`` will work correctly with OpenMPI. With some old version of OpenMPI, ``srun`` will fail.

   #. ``srun`` seems to be much faster than ``mpirun`` using an Intel-based installation.

Partitions
----------

Great Lakes currently has the following partitions: standard, large memory, GPU, and visuallization.
Typically, we will only have access to standard partition.
There is no need to specify the architecture the same way as in flux.

.. list-table::
    :widths: 30 20 20 20
    :header-rows: 1

    * - Node type
      - ppn
      - RAM (GB)
      - Number

    * - Standard
      - 36
      - 192
      - 380

A separate debug queue is also available, which can be requested via ``--partition=debug``.
It's exactly the same as the standard queue, but with a limit of 8 processors and 4 hours wall time, as well
as only one job per user at any given time.
The debug queue itself has higher priority, so it can be useful when the standard queue is packed.

Interactive Jobs
----------------
Interactive jobs are jobs where you get access to the terminal, such that you can run tasks interactively.
It would be exactly the same as if you were running jobs on your local computer, except you get access to more cores and more memory.

For example, an interactive job with 16 processors for one hour can be requested using::

   srun --nodes=1 --ntasks-per-node=16 --mem-per-cpu=5GB --time=1:00:00 --partition standard --pty /bin/bash

If the cluster is busy, using the debug queue (while staying under its resource limits) may be faster.
Once successful, you'll be logged in to a compute node (the hostname would look something like ``gl3057``), and you can then run your code normally.

Job Submission and Monitoring
-----------------------------

Jobs are submitted with ``sbatch batch_script``, and cancelled with ``scancel jobid``, where ``jobid`` can be found with ``squeue -u $USER``.
To check the estimated starting time for your job, type ``squeue -j <job ID> --start``.
To estimate the cost of your job, ``my_job_estimate <script name>``.
To check how much money used on an account, ``sreport -T billing cluster AccountUtilizationByUser Accounts=<account name> Start=<date> End=<date>``. 
A ``billing`` alias is shown in the above sample bashrc. The number needs to be divided by 100,000 to get the actual dollar amount used.
