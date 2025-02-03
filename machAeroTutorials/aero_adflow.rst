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
Copy the following file from the volume meshing directory:

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
   :language: py
   :start-after: # rst Imports
   :end-before: # rst ADflow options

First we import ADflow.
We also need to import ``baseclasses``, which is a library of problem and solver classes used to encourage a common API within the MACH suite.
In this case we will be using the AeroProblem, which is a container for the flow conditions that we want to analyze.
Finally, it is convenient to import the mpi4py library to prevent printing multiple times if we are running on multiple processors.
Importing mpi4py is not entirely necessary in the runscript because ADflow does it internally if necessary.

We also set up some command line arguments to easily specify certain parameters without having to modify the script.
These include options for specifying the output directory, the grid file used, and a ``task`` option that will be used to switch between several pre-defined tasks.
The ``analysis`` option here will simply run a single ADflow analysis, and the ``polar`` option will sweep through a range of angles of attack, and produce a table of :math:`C_L` and :math:`C_D` values.


ADflow options
--------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
   :language: py
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
   :language: py
   :start-after: # rst Start ADflow
   :end-before: # rst Create AeroProblem

When ADflow is instantiated, it reads in the mesh and then waits for the user to dictate further operations.
Before running the case, we can choose to set up some additional output options.
First, ADflow can write a file containing distribution data over the extent of the wing (e.g. lift, drag, twist) using ``addLiftDistribution``.
Also, ADflow can write airfoil data for a given set of slices along the wing using `addSlices`.

Set flow conditions
-------------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :language: py
    :start-after: # rst Create AeroProblem
    :end-before: # rst Run ADflow

The flow conditions and any auxiliary information about the geometry (such as reference dimensions) are provided to ADflow by way of an AeroProblem.
The AeroProblem automatically generates complete flow state information from the Mach number and altitude based on the 1976 U.S. Standard Atmosphere.
The ``alpha`` parameter is used to rotate the flow in the far-field to simulate angle-of-attack.
The ``evalFuncs`` parameter stipulates which functions the user would like to compute from the converged flow solution.
Some available functions include ``'cl'``, ``'cd'``, ``'cmz'``, ``'lift'``, and ``'drag'``.

Single analysis
---------------
.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :language: py
    :start-after: # rst Run ADflow
    :end-before: # rst Create polar arrays

Running the solver is very simple, it only requires an AeroProblem to run.
The function evaluation is done separately from the solution.
We pass a dictionary to ADflow and it will populate it with the prescribed functions.
We can request additional functions with the ``evalFuncs`` parameter.
Finally we print out the requested functions on the root proc.

Generating Drag Polars
----------------------
The other task is to generate a drag polar, which shares the same ADflow setup as the previous task.
The only difference is that the analysis is now done within a loop.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :language: py
    :start-after: # rst Create polar arrays
    :end-before: # rst Start loop

We start by creating a list of the angle of attack values that we wish to analyze.
In this case we use the ``numpy.linspace`` function to create a uniformly-spaced array with six whole number entries from 0 -- 5.
We also create the empty lists for storing the lift and drag coefficients.
The lift and drag data will be appended to these lists as the flow solutions are completed.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :language: py
    :start-after: # rst Start loop
    :end-before: # rst Print polar

Having created the input array and data storage lists, we can now loop over the desired angles of attack to evaluate the polar.
We accomplish this by using the builtin ``for`` loop structure in python.

Now for each angle of attack, we update two attributes of the aero problem.
We update the name to include the current angle of attack.
This allow the filenames of the lift distribution, slices, volume solution and surface solution to be updated with the current angle of attack, making it easier to keep track of the output files.
We also update the alpha parameter, which is the attribute of the AeroProblem that represents the angle of attack.

Running the solver is identical to the simple single point example.
We simply call the ``CFDSolver`` instance with the current AeroProblem.
This causes the CFD solver to be updated with the values of that AeroProblem prior to solving the flow.
We then use the same ``EvalFunctions`` call to integrate the surface forces to get the lift and drag coefficients.
The difference is that here, we append the coefficients from ``funcs`` into the ``CLList`` and ``CDList`` variables, so that they can be used later.


.. literalinclude:: ../tutorial/aero/analysis/aero_run.py
    :language: py
    :start-after: # rst Print polar

Once we complete the loop and evaluate all of the desired flow conditions, we can print the completed data set to the screen.



Run it yourself!
================
First we run the analysis task, which is the default ``task``:

.. prompt:: bash

    mpirun -np 4 python aero_run.py


ADflow will print to the terminal various information during the initialization stages before starting the solution process.
Once the solution process starts the terminal should show information about the convergence history of the variables specified in ``monitorvariables``, in addition to the total residual.
The solver terminates either by reaching the maximum number of iterations or a reduction in the total residual is specified by the ``L2Convergence`` option::

    #
    # Grid 1: Performing 1000 iterations, unless converged earlier. Minimum required iteration before NK switch:      5. Switch to NK at totalR of:   0.87E+03
    #
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
    #  Grid  | Iter | Iter |  Iter  |   CFL   | Step | Lin  |        Res rho         |         C_lift         |        C_drag          |        totalRes        |
    #  level |      | Tot  |  Type  |         |      | Res  |                        |                        |                        |                        |
    #------------------------------------------------------------------------------------------------------------------------------------------------------------
        1       0      0     None     ----    ----   ----   0.4736542591862984E+04   0.9538373121334282E-03   0.1223509652576924E+00   0.8731635332356837E+07
        1       1      3     *ANK   0.50E+01  0.15  0.002   0.4157522032946461E+04   0.1784855561878665E-01   0.1439322296931146E+00   0.7696003130201009E+07
        1       2      8      ANK   0.50E+01  0.26  0.006   0.3337803689264238E+04   0.4368200811732226E-01   0.1742644820652672E+00   0.6165342727351038E+07
        1       3     13      ANK   0.50E+01  0.32  0.027   0.2582456998758441E+04   0.6799469001914685E-01   0.2013532433207174E+00   0.4742386626241744E+07
        1       4     19      ANK   0.50E+01  0.34  0.028   0.1988458840993347E+04   0.8617757940165757E-01   0.2203844182873343E+00   0.3625314700328018E+07
                .
                .
        1      47    320      ANK   0.29E+04  1.00  0.049   0.4020045549734340E+00   0.4225411072341632E+00   0.1686171937462218E-01   0.8628072659973345E+03
        1      48    325      *NK     ----    1.00  0.265   0.1122839602373398E+00   0.4214424715301505E+00   0.1693782497607938E-01   0.2281856331464926E+03
        1      49    357       NK     ----    1.00  0.139   0.3590927801948642E-01   0.4188700783401403E+00   0.1675878885812413E-01   0.9602093569663219E+02
        1      50    370       NK     ----    1.00  0.233   0.1234849430743969E-01   0.4183997561758928E+00   0.1672837063506830E-01   0.2236421105321589E+02
        1      51    416       NK     ----    1.00  0.100   0.2859429789094894E-02   0.4177585676352084E+00   0.1680250566621767E-01   0.3480878888188400E+01


A the end of the terminal output the functions defined in ``evalFuncs``  are printed to the screen::

    {'wing_cd': 0.016801751358107225, 'wing_cl': 0.4177636397905002}

Next, run the ``polar`` task:

.. prompt:: bash

    mpirun -np 4 python aero_run.py --task polar --output polar


The final table should look something like::

     Alpha       CL       CD
    ========================
       0.0   0.2272   0.0111
       1.0   0.3550   0.0143
       2.0   0.4760   0.0201
       3.0   0.5695   0.0284
       4.0   0.6330   0.0385
       5.0   0.6805   0.0509


Postprocessing the solution output
==================================
All output is found in the ``output`` directory.
The solutions file (``.dat``, ``.cgns`` or ``.plt``) can be viewed in the Tecplot.
A contour plot of the pressure coefficient using the surface ``.plt`` is shown below.

.. figure:: images/aero_wing_analysis_cp_contour.png
    :scale: 20
    :align: center
    :alt: Pressure coefficient
    :figclass: align-center

The lift and slice files (``.dat``) can also be viewed in tecplot or parsed directly and plotted e.g. matplotlib.
From the lift file we show the spanwise normalized lift, compared to elliptical lift, as well as the twist distribution and t/c.

.. figure:: images/aero_wing_analysis_lift.png
    :scale: 50
    :align: center
    :alt: Lift file
    :figclass: align-center

For the slice file, here the normalized airfoil shape and pressure coefficient are shown.

.. figure:: images/aero_wing_analysis_slices.png
    :scale: 50
    :align: center
    :alt: Slice file
    :figclass: align-center
