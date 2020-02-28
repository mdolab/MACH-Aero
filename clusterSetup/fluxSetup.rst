.. Documentation of a basic setup on the flux cluster.
   Note that the user is assumed to have already gotten an account
   setup, and has access to the login nodes on the cluster.

.. _flux:

Flux Cluster Setup
======================
This guide is intended to assist users with setting up the MDOlab software
on the UMich Flux Cluster.  The user will first need to create an account
and get access to the cluster. Flux requires an on-campus connection, which can be provided by UMVPN (see :ref:`settingUpUMVPN` for setup instructions). An alternative is to first ``ssh`` into ``login.itd.umich.edu``, which does not require an on-campus connection, then from there ``ssh`` on to ``flux-login.arc-ts.umich.edu``. It is recommended to save these commands as aliases or bash scripts for convenience. 

flux users manual is at:
http://arc-ts.umich.edu/flux-user-guide/

.. note::
    Pay attention to the version of anaconda2 version -- newer version like
    "anaconda2/latest" may not work approporiately. It is recommended to be specific
    about the version you use and stick with it. It is known: "python-anaconda2/201704" 
    will work.

Example .bashrc
---------------

Here is an example .bashrc file. You may need to create this in your
home directory on flux.

.. code-block:: bash

   # .bashrc                                                                

   # Source global definitions                       
   if [ -f /etc/bashrc ]; then
        . /etc/bashrc
   fi

   module load python-anaconda2
   module load intel/17.0.1
   module load openmpi/1.10.2/intel
   module load cmake

   # add the repos directory to your python path so that the mdolab modules will be available
   export PYTHONPATH=$PYTHONPATH:$HOME/repos/

   # CGNS
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/cgnslib_3.2.1/src

   # Petsc
   export PETSC_DIR=${HOME}/packages/<petsc-version>
   export PETSC_ARCH=real-opt
   export PATH=${PATH}:${HOME}/repos/tacs/extern/f5totec
   export PATH=$PATH:$HOME/repos/cgnsutilities/bin

   # User specific aliases and functions
   alias j4='qsub -I -V -A engin_flux -q flux -l procs=4,qos=flux,walltime=24:00:00,pmem=8000mb'
   alias j16='qsub -I -V -A engin_flux -q flux -l procs=16,qos=flux,walltime=24:00:00,pmem=4000mb'
   alias jj16='qsub -I -V -A jrram_flux -q flux -l procs=16,qos=flux,walltime=24:00:00,pmem=4000mb'
   alias jj24='qsub -I -V -A jrram_flux -q flux -l procs=24,qos=flux,walltime=24:00:00,pmem=4000mb'
   alias jj12='qsub -I -V -A jrram_flux -q flux -l nodes=1:ppn=12:x5650,qos=flux,walltime=4:00:00,pmem=4000mb'
   alias jj64='qsub -I -V -A jrram_flux -q flux -l procs=64,qos=flux,walltime=24:00:00,pmem=4000mb'
   alias jj60='qsub -I -V -A jrram_flux -q flux -l nodes=5:ppn=12:x5650,qos=flux,walltime=24:00:00,pmem=4000mb'
   alias jj180='qsub -I -V -A jrram_flux -q flux -l procs=180,qos=flux,walltime=24:00:00,pmem=4000mb'
   alias j='qstat -u uniqname'
   alias sjq='showq -w acct=jrram_flux'
   alias emn='emacs -nw'
   alias scr='cd /scratch/jrram_flux/uniqname/'
   PS1='${USER}@${HOSTNAME}:\w$ '

This file starts by specifying the preset modules you want to load.
This is followed by a section setting the environment variables to allow the use of the MDOlab software.
The last portion of the file specifies a series of aliases to make some standard operations easier.

Example PBS Script
------------------

Below is an example PBS script for Flux.

.. code-block:: bash

   #PBS -S /bin/bash
   #PBS -N testCaseAS
   #PBS -l nodes=4:ppn=16,pmem=4000mb
   #PBS -l walltime=0:01:00
   #PBS -j oe
   #PBS -V
   #PBS -m bae
   #PBS -M uniqname@umich.edu
   #PBS -q flux
   #PBS -A jrram_flux

   source ~/.bashrc

   cd repos/mdo_tutorial/as_opt/

   mpiexec python as_opt.py

Specifying Job Architecture
---------------------------

Flux currently has the following compute nodes:

.. list-table:: 
    :widths: 30 20 20 20 
    :header-rows: 1

    * - Architecture
      - ppn
      - RAM (GB)
      - Number

    * - Haswell
      - 24
      - 128
      - 109

    * - Ivybridge
      - 20
      - 96
      - 124

    * - Sandybridge
      - 16
      - 64
      - 139

    * - Nehalem
      - 12
      - 48
      - 88

Flux, unlike many other clusters, does not provide entire compute nodes for you by default. It is common to have to share nodes with other users, degrading the performance of your code. For example, if you request ``ppn=16``, you may end up on an Ivybridge node using 16 of the 20 available procs. Since memory is shared within a node, this may affect the performance of your code. Furthermore, you will likely receive a mix of different architectures among your nodes, which is again detrimental. To mitigate these issues, it is possible to request entire compute nodes by specifying an architecture which matches up to the requested ``ppn``. This is done with for example ``#PBS -l nodes=4:ppn=16:sandybridge,pmem=4000mb``. However, you may end up waiting a longer time before full compute nodes become available. 

Job Submission and Monitoring
-----------------------------

Jobs are submitted with ``qsub PBS_script``, and cancelled with ``canceljob jobid`, where ``jobid`` can be found with ``showq -u uniqname``. Interactive jobs may be useful for debugging purposes, and they can be requested with the ``-I`` flag. The ``.bashrc`` file above contains many aliases to interactive job requests.

To check the estimated starting time for your job, type
``showstart jobid``. If a job is eligible but not running, check that the allocation has enough free procs. A job may also not start due to the unavailability of the specific architecture requested. To check the available resources for a given architecture, use ``idlenodes jrram_flux sandybridge``.

Once the job is running, you can also ``ssh`` directly into any of your compute nodes to monitor the job. The names of the compute nodes are written in the email you receive when your flux job begins execution, and are of the form ``nyx`` followed by a string of numbers.