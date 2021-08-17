.. _aero_adflow:

********************
Analysis with ADflow
********************

Introduction
============
There is no graphical user interface for ADflow.
The cases are prepared with python scripts and run from the command line.
In this section of the tutorial, we will explain the nuts and bolts of a basic ADflow runscript.
You will find a complete introduction to ADflow in the :doc:`docs <adflow:introduction>`.

Files
=====
Navigate to the directory ``aero/analysis`` in your tutorial folder.
Copy the following files from the volume meshing directory:

.. prompt:: bash

    cp ../meshing/volume/wing_vol.cgns .

Create the following empty runscript in the current directory:

- ``aero_run.py``


Dissecting the ADflow runscript
===============================
Open the file ``aero_run.py`` with your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
   :start-after: # rst Imports
   :end-before: # rst ADflow options

First we import ADflow.
We also need to import ``baseclasses``, which is a library of problem and solver classes used to encourage a common API within the MACH suite.
In this case we will be using the AeroProblem, which is a container for the flow conditions that we want to analyze.
Finally, it is convenient to import the mpi4py library to prevent printing multiple times if we are running on multiple processors.
Importing mpi4py is not entirely necessary in the runscript because ADflow does it internally if necessary.

ADflow options
--------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
   :start-after: # rst ADflow options
   :end-before: # rst Start ADflow

An exhaustive list of the ADflow options and their descriptions can be found in the docs.
For our purposes here, I will go over them briefly.
The `I/O Parameters` include the mesh file, the output directory, and the variables that will be printed as the solver runs.
Under `Solver Parameters`, you can choose a basic solver (DADI or Runge Kutta) and set the CFL and multigrid parameters.
Additionally, the Approximate Newton-Krylov (ANK) and Newton-Krylov (NK) solvers can be used to speed up convergence of the solver.
Finally, we can terminate the solver based on relative convergence of the norm of the residuals or maximum number of iterations.
We strongly recommend going over the descriptions and tips on solvers and solver options in the ADflow :doc:`solvers docs <adflow:solvers>`.

Create solver
-------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
   :start-after: # rst Start ADflow
   :end-before: # rst Create AeroProblem

When ADflow is instantiated, it reads in the mesh and then waits for the user to dictate further operations.
Before running the case, we can choose to set up some additional output options.
First, ADflow can write a file containing distribution data over the extent of the wing (e.g. lift, drag, twist) using ``addLiftDistribution``.
Also, ADflow can write airfoil data for a given set of slices along the wing using `addSlices`.

Set flow conditions
-------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Create AeroProblem
    :end-before: # rst Run ADflow

The flow conditions and any auxiliary information about the geometry (such as reference dimensions) are provided to ADflow by way of an AeroProblem.
The AeroProblem automatically generates complete flow state information from the Mach number and altitude based on the 1976 U.S. Standard Atmosphere.
The ``alpha`` parameter is used to rotate the flow in the far-field to simulate angle-of-attack.
The ``evalFuncs`` parameter stipulates which functions the user would like to compute from the converged flow solution.
Some available functions include ``'cl'``, ``'cd'``, ``'cmz'``, ``'lift'``, and ``'drag'``.

Run solver
----------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Run ADflow
    :end-before: # rst Evaluate and print

Running the solver is very simple.
It only requires an AeroProblem to run.

Evaluate functions
------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :start-after: # rst Evaluate and print

The function evaluation is done separately from the solution.
We pass a dictionary to ADflow and it will populate it with the prescribed functions.
We can request additional functions with the `evalFuncs` parameter.
Finally we print out the requested functions on the root proc.

Run it yourself!
================
First make the output directory and then run the script (you may have to change your outputDirectory in aeroOptions)

.. prompt:: bash

    mkdir output
    mpirun -np 4 python aero_run.py

