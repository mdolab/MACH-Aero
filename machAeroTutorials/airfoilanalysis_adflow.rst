.. _airfoilanalysis_adflow:


*************************
Analysis with ADflow
*************************

Introduction
============
Now that we have a valid structured volume mesh, we can start our aerodynamics analysis with ADflow.
There is no graphical user interface for ADflow.
The cases are prepared with python scripts and run from the command line.
In this section of the tutorial, we will explain the nuts and bolts of a basic ADflow runscript.
You will find a complete introduction to ADflow in the :doc:`docs <adflow:introduction>`.

Files
=====

Navigate to the directory ``airfoil/analysis`` in your tutorial folder. 
Copy the CGNS mesh file, ``n0012.cgns``, generated previously, into the directory:

.. prompt:: bash

    cp ../mesh/n0012.cgns . 

Create the following empty runscript in the current directory:

- ``airfoil_run.py``


Dissecting the airfoil analysis script
==============================================
Open the file ``airfoil_run.py`` in your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Imports
    :end-before: # rst Args

First we import ADflow.
We also need to import ``baseclasses``, which is a library of problem and solver classes used to encourage a common API within the MACH suite.
In this case we will be using the AeroProblem, which is a container for the flow conditions that we want to analyze.
Finally, it is convenient to import the mpi4py library to prevent printing multiple times if we are running on multiple processors.
Importing mpi4py is not entirely necessary in the runscript because ADflow does it internally if necessary.

Adding command line arguments
-----------------------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst Args
    :end-before: # rst ADflow options

This is a convenience feature that allows the user to pass in command line arguments to the script.
Four options are provided:

-  Output directory
-  Grid file to be used
-  Task to execute

ADflow set-up
-------------
.. literalinclude:: ../tutorial/airfoil/analysis/airfoil_run.py
    :start-after: # rst ADflow options
    :end-before: # rst Start ADflow

As it is, the options specified above allow for a good convergence of NACA0012 airfoil analysis, but may not converge for other airfoils. 
Some useful options to adjust are:

``nCycles``
    If the analysis doesn't converge, this can be increased.

``nkswitchtol``
    If the analysis stops converging during NK (Newton-Krylov), this might mean that it is still outside of the radius of convergence of the NK method. The parameter should then be lowered.

``NKSubSpaceSize``
    Decreasing this parameter will decrease memory usage when in the NK range. Only change this if there are memory issues when dealing with larger meshes.

``writeSurfaceSolution`` and ``writeVolumeSolution``
    If you want to view the surface or volume solutions at the end of each analysis, these parameters can be set to True.

An exhaustive list of the ADflow options and their descriptions can be found in the docs.
We strongly recommend going over the descriptions and tips on solvers and solver options in the ADflow :doc:`solvers docs <adflow:solvers>`.


