.. _aero_adflow_polar:

*******************************
Drag Polar Analysis with ADflow
*******************************

Introduction
============
This example is an extension of the previous example "Analysis with ADflow".
Much of the code used for the two cases is the same, however, we include the full 
script for completeness. 
We extend the basic single point run script to run a simple variable sweep, in this
case angle of attack, to demonstrate the power of scripting the analysis.
As we go through the code, we will highlight the differences between the this example and the
previous case.

Files
=====
Navigate to the directory ``aero/analysis`` in your tutorial folder.
If you haven't already done so, copy the following files from the volume meshing directory:

.. prompt:: bash

    cp ../meshing/volume/wing_vol.cgns .

Create the following empty runscript in the current directory:

- ``aero_run_drag_polar.py``


Dissecting the ADflow runscript
===============================
Open the file ``aero_run_drag_polar.py`` with your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
   :start-after: # rst Imports
   :end-before: # rst ADflow options

As in the previous example, we first import ADflow.
We also need to import :doc:`baseclasses <baseclasses:index>`, which is a library of problem and solver classes used to encourage a common API within the MACH suite.
We will again be using the AeroProblem, which is a container for the flow conditions that we want to analyze.
However, in this case we will sequentially update the alpha parameter to produce the desired drag polar.
Again, it is convenient to import the mpi4py library to prevent printing multiple times if we are running on multiple processors.
Importing mpi4py is not entirely necessary in the runscript because ADflow does it internally if necessary.

ADflow options
--------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
   :start-after: # rst ADflow options
   :end-before: # rst Start ADflow

An exhaustive list of the ADflow options and their descriptions can be found in :doc:`ADflow options<adflow:options>`.
We will not go over every option here, as they are outlined in the previous example.
However, we will highlight the option that has been changed for this case.
This option is the "infchangecorrection" option.
This option causes the change in the freestream velocity to be added to every cell in the mesh whenever alpha is updated.
This produces a significant improvement in the convergence of the implicit solver algorithms in the code, in particular the full Newton-Krylov algorithm.

Create solver
-------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
   :start-after: # rst Start ADflow
   :end-before: # rst Create AeroProblem

When ADflow is instantiated, it reads in the mesh and then waits for the user to dictate further operations.
As in the previous example, we tell ADflow to create lift distribution and section slice files for the test case.
ADflow appends a numeric counter to the file name, which is incremented for each solution call, so that the files will not be overwritten in scripted cases like this drag polar calculation.

Create AeroProblem Object
-------------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
    :start-after: # rst Create AeroProblem
    :end-before: # rst Create polar arrays

As in the previous case, we create a single AeroProblem instance which describes the flight condition and reference quantities for the flow simulation.
At this stage, the setup of the AeroProblem is the same as the single point analysis. 
However, as we will show later, we will update this AeroProblem with different values of alpha to produce the desired drag polar. 

Create Drag Polar Arrays
------------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
    :start-after: # rst Create polar arrays
    :end-before: # rst Start loop

This is where the major differences between a single point run and the drag polar become evident.
We start by creating an array of the angle of attack values that we wish to simulate.
In this case we use the numpy.linspace function to create a uniformly space array with six whole number entries from 0 - 5.
We also create the empty lists for storing the lift and drag coefficients. 
The lift and drag data will be appended to these lists as the flow solutions are completed.

Loop over the Angle of Attack Input Arrays
------------------------------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
    :start-after: # rst Start loop
    :end-before: # rst update AP

Having created the input array and data storage lists, we can now loop over the desired angles of attack to evaluate the polar.
We accomplish this by using the builtin "for" loop structure in python.

Update the AeroProblem
----------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
    :start-after: # rst update AP
    :end-before: # rst Run ADflow

Now for each angle of attack, we update two attributes of the aero problem.
We update the name to include the current angle of attack.
This allow the filenames of the lift distribution, slices, volume solution and surface solution to be updated with the current angle of attack, making it easier to keep track of the output files.
We also update the alpha parameter, which is the attribute of the AeroProblem that represents the angle of attack.

Run solver and Accumulate Drag Polar
------------------------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
    :start-after: # rst Run ADflow
    :end-before: # rst Print polar

Running the solver is identical to the simple single point example. 
We simply call the CFDSolver instance with the current AeroProblem. 
This causes the CFD solver to be updated with the values of that AeroProblem prior to solving the flow.
We then use the same EvalFunctions call to integrate the surface forces to get the lift and drag coefficients.
The difference is that here, we append the coefficients from "funcs" into the "CL" and "CD" list, so that they can be used later.

Print Drag Polar
----------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run_drag_polar.py
    :start-after: # rst Print polar

Once we complete the loop and evaluate all of the desired flow conditions, we can print the completed data set to the screen.


Run it yourself!
================
First make the output directory and then run the script

.. prompt:: bash

    mkdir output
    mpirun -np 4 python aero_run_drag_polar.py
