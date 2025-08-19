.. _airfoilopt_singlepoint:


*************************
Single Point Optimization
*************************

Introduction
============
We will now proceed to optimizing a NACA0012 airfoil for a given set of flow conditions.
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
Copy the FFD file, ``ffd.xyz``, and the CGNS mesh file, ``n0012.cgns``, generated in the previous tutorial, into the directory:

.. prompt:: bash

    cp ../../meshing/n0012.cgns . 
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
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst args (beg)
    :end-before: # rst args (end)

This is a convenience feature that allows the user to pass in command line arguments to the script.
Four options are provided:

-  Output directory
-  Optimizer to be used
-  Grid file to be used
-  Optimizer options

Specifying parameters for the optimization
------------------------------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst parameters (beg)
    :end-before: # rst parameters (end)

Several conditions for the optimization are specified at the beginning of the script. 
These include the coefficient of lift constraint value, Mach number, and altitude to indicate flow conditions. 
The angle of attack serves as the initial value for the optimization and should not affect the optimized result.

Creating processor sets
-----------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst multipoint (beg)
    :end-before: # rst multipoint (end)

Allocating sets of processors for different analyses can be helpful for multiple design points, but this is a single-point optimization, so only one point is added. 

ADflow options
------------- 
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst adflow (beg)
    :end-before: # rst adflow (end)

In this example, we have configured far more options for ADflow than we did in the previous example.
For optimziation problems, the solver needs to be tuned for high performance and robustness.
As it is, the options specified above allow for a good convergence of NACA0012 airfoil analysis, but may not converge for other airfoils. 
We won't go over all the options and why we selected them here but will refer you to the ADflow documentation.
However some useful options to adjust are:

``nCycles``
    If the analysis doesn't converge, this can be increased.

``NKSwitchTol``
    If the analysis stops converging during NK (Newton-Krylov), this might mean that it is still outside of the radius of convergence of the NK method. The parameter should then be lowered.

``NKSubSpaceSize``
    Decreasing this parameter will decrease memory usage when in the NK solver. Only change this if there are memory issues when dealing with larger meshes.

``writeSurfaceSolution`` and ``writeVolumeSolution``
    If you want to view the surface or volume solutions at the end of each analysis, these parameters can be set to True.

We then create the ADflow solver object while passing in the options dictionary and communicator object.
We also use ``addSlices`` to write the airfoil coordinates and :math:`c_p` distribution to a text file.

Set the AeroProblem
-------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst aeroproblem (beg)
    :end-before: # rst aeroproblem (end)

We add angle of attack as a design variable and set up the AeroProblem using given flow conditions.


Geometric parametrization
-------------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst dvgeo (beg)
    :end-before: # rst dvgeo (end)

The set-up for DVGeometry (FFD class) is simple for an airfoil since it doesn't involve span-wise variables such as twist, dihedral, or taper.
The only DVs we have are local shape variables that control the vertical movements of each individual FFD node.
The local design variable ``shape`` is added.

.. note:: Note that since we have to work with a 3D problem, this in fact has twice as many DVs as we'd like---the shape of the two airfoil sections should remain the same.
    This is addressed by adding linear constraints in the following section.

Geometric constraints
---------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst dvcon (beg)
    :end-before: # rst dvcon (end)

``DVConstraints`` is the class in pygeo responsible for handling geometric constriants.
In order to meet our coefficient of lift constraint, the optimizer will have to change the angle-of-attack.
Since we have given it :math:`\alpha` as a design variable, it should be able to do that.
However, optimizers have a strong tendancy to exploit any flaws in a problem formulation and there is a major one that we have to address with a constraint.
Instead of changing :math:`\alpha` to meet the :math:`C_l` constraint, the optimizer could instead twist the airfoil shape itself to achieve the same effect.
This effect is undesirable and we can prevent it by constraining the leading and trailing edge to only move in the same direction with a call to ``addLeTeConstraints``.
Additionally since we are treating the airfoil as a 3D problem we must add a set of linear constraints such that the shape deformations on one side of the airfoil mirrors that of the other.
This is accomplished with a call to ``addLinearConstraintsShape``.
Lastly, we can add the thickness and volume constraints defined in our optimization problem with calls to ``addThicknessConstraints2D`` and ``addVolumeConstraint``.


Mesh warping set-up
-------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst warp (beg)
    :end-before: # rst warp (end)

The FFD only warps the point set defining our airfoil.
The volume mesh itself must still conform to the airfoil surface for ADflow to compute an accurate flow solution.
Volume mesh warping is accomplished using IDwarp in MACH and is very straightforward to set up as shown here.

Optimization callback functions
-------------------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst funcs (beg)
    :end-before: # rst funcs (end)

We can now start setting up the optimization problem.
First we must set up a callback function and a sensitivity function for each processor set (well, the one processor set in this case).
In this case ``cruiseFuncs`` and ``cruiseFuncsSens`` belong to the ``cruise`` processor set.
Then we need to set up an objCon function, which is used to create abstract functions of other functions.

Now we will explain each of these callback functions.

cruiseFuncs
~~~~~~~~~~~
The input to ``cruiseFuncs`` is the dictionary of design variables.
First, we pass this dictionary to DVGeometry and AeroProblem to set their respective design variables.
Then we solve the flow solution given by the AeroProblem with ADflow.
Finally, we fill the ``funcs`` dictionary with the function values computed by DVConstraints and ADflow.
The call ``checkSolutionFailure`` checks ADflow to see if there was a failure in the solution (could be due to negative volumes or something more sinister).
If there was a failure it changes the ``fail`` flag in ``funcs`` to ``True``.
The ``funcs`` dictionary is the required return.

cruiseFuncsSens
~~~~~~~~~~~~~~~
The inputs to ``cruiseFuncsSens`` are the design variable and function dictionaries.
Inside ``cruiseFuncsSens`` we populate the ``funcsSens`` dictionary with the derivatives of each of the functions in ``cruiseFuncs`` with respect to all of its dependence variables.

objCon
~~~~~~
The main input to the ``objCon`` callback function is the dictionary of functions (which is a compilation of all the ``funcs`` dictionaries from each of the design points).
Inside ``objCon``, the user can define functionals (or functions of other functions).
For instance, to maximize L/D, you could define the objective function as::

    funcs['obj'] = funcs['cl'] / funcs['cd']

The ``objCon`` function is processed within the multipoint module and the partial derivatives of any functionals with respect to the input functions are automatically computed with the complex-step method.
This means that the user doesn't have to worry about computing analytic derivatives for the simple functionals defined in ``objCon``.
The ``printOK`` input is a boolean that is False when the complex-step is in process.

Optimization problem
--------------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst optprob (beg)
    :end-before: # rst optprob (end)

Setting up the optimization problem follows the same format as before, only now we incorporate multiPointSparse.
When creating the instance of the Optimization problem, ``MP.obj`` is given as the objective function.
multiPointSparse will take care of calling both ``cruiseFuncs`` and ``objCon`` to provide the full ``funcs`` dictionary to pyOptSparse.

Both AeroProblem and DVGeometry have built-in functions to add all of their respective design variables to the optimization problem.
DVConstraints also has a built-in function to add all constraints to the optimization problem.
The user must manually add any constraints that were defined in ``objCon``.

Finally, we need to tell multiPointSparse which callback functions belong to which processor set.
We also need to provide it with the objCon and the optProb.
The call ``optProb.printSparsity()`` prints out the constraint Jacobian at the beginning of the optimization.


Run optimization
----------------
.. literalinclude:: ../tutorial/airfoilopt/singlepoint/airfoil_opt.py
    :start-after: # rst optimizer

To finish up, we choose the optimizer and then run the optimization.

.. note::
    The complete set of options for ``SNOPT`` can be found in :ref:`the pyOptSparse documentation <pyoptsparse:snopt>`.
    It is useful to remember that you can include major iterations information in the history file by providing the proper options.
    It has been observed that the ``_print`` and ``_summary`` files occasionally fail to be updated, possibly due to unknown hardware issues on GreatLakes.
    The problem is not common, but if you want to avoid losing this information, you might back it up in the history file.
    This would allow you monitor the optimization even if the ``_print`` and ``_summary`` files are not being updated.
    Note that the size of the history file will increase due to this additional data.

Run it yourself!
================

To run the script, use the ``mpirun`` and place the total number of processors after the ``-np`` argument

.. prompt:: bash

    mpirun -np 4 python airfoil_opt.py | tee output.txt

The command ``tee`` saves the text outputs of the optimization to the specified text file.
You can follow the progress of the optimization using OptView, as explained in :ref:`pyOptSparse <opt_pyopt>`.
For postprocessing, refer to the corresponding section the previous tutorial.
Using the settings given in this example, ADflow should automatically output the surface, volume, and slice solutions at each optimizer iteration.
Be sure to use the most recent output files to view the optimum airfoil solution.

.. figure::
    images/airfoil_single_opt.png
    :width: 600
    :align: center
