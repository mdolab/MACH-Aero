.. _airfoilopt_singlepoint:


*************************
Single Point Optimization
*************************

Introduction
============
We will now proceed to optimizing a NACA0012 airfoil for a given set of flow conditions. It is very similar to a wing optimization.
The optimization problem is defined as:

| *minimize*
|    :math:`C_D`
| *with respect to*
|    10 shape variables
| *subject to*
|    :math:`C_L = 0.5`
|    :math:`V \ge V_0`
|    :math:`t \ge 0.1t_0`
|    :math:`\Delta z_\text{LETE, upper} = -\Delta z_{LETE, lower}`

The shape variables are controlled by the FFD points specified in the FFD file.

Files
=====

Navigate to the directory ``airfoilopt/singlepoint`` in your tutorial folder.
Copy the FFD file, ``ffd.xyz``, and the CGNS mesh file, ``n0012.cgns``, generated previously, into the directory:

.. prompt:: bash

    cp ../mesh/n0012.cgns .
    cp ../ffd/ffd.xyz .

Create the following empty runscript in the current directory:

- ``airfoil_opt.py``


Dissecting the aerodynamic optimization script
==============================================
Open the file ``airfoil_opt.py`` in your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst Imports (beg)
    :end-before: # rst Imports (end)

Adding command line arguments
-----------------------------
This is a convenience feature that allows the user to pass in command line arguments to the script.
Four options are provided:

-  Output directory
-  Optimizer to be used
-  Grid file to be used
-  Optimizer options

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst args (beg)
    :end-before: # rst args (end)

Specifying parameters for the optimization
------------------------------------------
Several conditions for the optimization are specified at the beginning of the script.
These include the coefficient of lift constraint value, Mach number, and altitude to indicate flow conditions.

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst parameters (beg)
    :end-before: # rst parameters (end)

The angle of attack serves as the initial value for the optimization and should not affect the optimized result.

Creating processor sets
-----------------------

Allocating sets of processors for different analyses can be helpful for multiple design points, but this is a single-point optimization, so only one point is added.

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst multipoint (beg)
    :end-before: # rst multipoint (end)


ADflow set-up
-------------

The ADflow set-up looks similar to the aerodynamic analysis script.

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst adflow (beg)
    :end-before: # rst adflow (end)

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


We also use ``addSlices`` to write the airfoil coordinates and :math:`c_p` distribution to a text file.

Set the AeroProblem
-------------------

We add angle of attack as a design variable and set up the AeroProblem using given flow conditions.

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst aeroproblem (beg)
    :end-before: # rst aeroproblem (end)


Geometric parametrization
-------------------------

The set-up for DVGeometry is simpler for an airfoil since it doesn't involve span-wise variables such as twist, dihedral, or taper.
As a result, we also don't need to set up a reference axis.
The only DVs we have are local shape variables that control the vertical movements of each individual FFD node.
Note that since we have to work with a 3D problem, this in fact has twice as many DVs as we'd like---the shape of the two airfoil sections should remain the same.
This is addressed by adding linear constraints in the following section.

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst dvgeo (beg)
    :end-before: # rst dvgeo (end)

The local design variable ``shape`` is added.

Geometric constraints
---------------------
This section is very similar to the corresponding section for the wing optimization.
The only difference is that, we must add a set of linear constraints such that the shape deformations on one side of the airfoil mirrors that of the other.
This is accomplished with a call to ``addLinearConstraintsShape``.


.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst dvcon (beg)
    :end-before: # rst dvcon (end)


Mesh warping set-up
-------------------

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst warp (beg)
    :end-before: # rst warp (end)

Optimization callback functions
-------------------------------
This section is also the same as the corresponding section in aircraft optimization.

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst funcs (beg)
    :end-before: # rst funcs (end)

Optimization problem
--------------------
This section is also the same as the corresponding section in aircraft optimization.

.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst optprob (beg)
    :end-before: # rst optprob (end)


Run optimization
----------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst optimizer

Run it yourself!
================

To run the script, use the ``mpirun`` and place the total number of processors after the ``-np`` argument

.. prompt:: bash

    mpirun -np 4 python airfoil_opt.py | tee output.txt

The command ``tee`` saves the text outputs of the optimization to the specified text file.
You can follow the progress of the optimization using OptView, as explained in :ref:`pyOptSparse <opt_pyopt>`.

.. figure::
    images/airfoil_single_opt.png
    :width: 600
    :align: center
