.. Documentation of a basic setup on the flux cluster.
   Note that the user is assumed to have already gotten an account
   setup, and has access to the login nodes on the cluster.
   Author: C.A.(Sandy) Mader (cmader@umich.edu)
   Edited by: 

.. _Great Lakes:

GreatLakes Cluster Setup
========================
This guide is intended to assist users with setting up the MDOlab software
on the UMich GreatLakes Cluster.  The user will first need to create an account
and get access to the cluster. GreatLakes requires an on-campus connection, which can be provided by UMVPN (see :ref:`settingUpUMVPN` for setup instructions). An alternative is to first ``ssh`` into ``login.itd.umich.edu``, which does not require an on-campus connection, then from there ``ssh`` on to ``greatlakes.arc-ts.umich.edu``. It is recommended to save these commands as aliases or bash scripts for convenience. 

Great Lakes users manual is at:
https://arc-ts.umich.edu/greatlakes/

.. note::
    It is known: "python-anaconda2/" works.

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

   module load python-anaconda2/                                                                                                       
   module load gcc/4.8.5                                                                                                           
   module load openmpi/1.10.7
   module load cmake


   # add the repos directory to your python path so that the mdolab modules will be available
   export PYTHONPATH=$PYTHONPATH:$HOME/repos/

   # CGNS
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/cgnslib_3.2.1/src
   # CGNS 3.3.0
   # export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/CGNS-3.3.0/src


   # Petsc
   export PETSC_DIR=${HOME}/packages/<petsc-version>
   export PETSC_ARCH=real-opt
   export PATH=${PATH}:${HOME}/repos/tacs_orig/extern/f5totec
   export PATH=$PATH:$HOME/repos/cgnsutilities/bin

   # User specific aliases and functions
   alias j='squeue -u uniqname'
   alias emn='emacs -nw'
   alias scr='cd /scratch/jrram_root/jrram/uniqname'
   PS1='${USER}@${HOSTNAME}:\w$ '

This file starts by specifying the preset modules you want to load.
On GreatLakes, if you want to use openmpi/1.10.7, you have to use gcc.
This is followed by a section setting the environment variables to allow the use of the MDOlab software.
The last portion of the file specifies a series of aliases to make some standard operations easier.

Example Batch Script
--------------------

Below is an example Batch script for Great Lakes.

.. code-block:: bash

   #!/bin/bash                                                                                                                       
   # The interpreter used to execute the script:                                                                                     
   # "SBATCH" directives that convey submission options:                                                                             
   ##### The name of the job                                                                                                         
   #SBATCH --job-name=Jobname
   ##### Email address
   #SBATCH --mail-user=uniqname@umich.edu                                                                                               
   ##### When to send e-mail: pick from NONE, BEGIN, END, FAIL, REQUEUE, ALL                                                         
   #SBATCH --mail-type=BEGIN,END,FAIL                                                                                                
   ##### Resources for your job                                                                                                      
   # number of physical nodes                                                                                                        
   #SBATCH --nodes=1                                                                                                                 
   # number of task per nodes (number of CPU-cores per node)                                                                         
   #SBATCH --ntasks-per-node=36                                                                                                      
   # memory per CPU core                                                                                                             
   #SBATCH --mem-per-cpu=5GB                                                                                                        
   ##### Maximum amount of time the job will be allowed to run                                                                       
   ##### Recommended formats: MM:SS, HH:MM:SS, DD-HH:MM                                                                              
   #SBATCH --time=100:00:00                                                                                                          
   ##### The resource account; who pays                                                                                              
   #SBATCH --account=jrram    
   #SBATCH --partition=standard
   ##### Output path
   #SBATCH --output=/home/%u/%x-%j.log                                                                                                       
   ########## End of preamble! #########################################                                                             
   # No need to “cd”. Slurm starts the job in the submission directory.                                                              
   #####################################################################  
   source ~/.bashrc                                                           
   # The application(s) to execute along with its input arguments and options:                                                       
   mpirun -np 36 python opt.py 

.. note::
    By default Slurm does not source the files ``~./bashrc`` or ``~/.profile``.

Specifying Partition
---------------------

Great Lakse currently has the following partitions:

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

    * - Large Momory
      - 36
      - 1,539
      - 3

    * - GPU
      - 40
      - 192
      - 20

    * - Visualization
      - 40
      - 192
      - 4


Job Submission and Monitoring
-----------------------------

Jobs are submitted with ``sbatch batch_script``, and cancelled with ``scancel jobid`, where ``jobid`` can be found with ``squeue -u uniqname``. 
Interactive jobs may be useful for debugging purposes, and they can be requested with the ``srun --nodes=2 --ntasks-per-node=4 --mem-per-cpu=1GB --cpus-per-task=1 --time=1:00:00 --pty /bin/bash``. 
