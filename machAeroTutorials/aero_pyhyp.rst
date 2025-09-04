.. _aero_pyhyp:

**************
Volume Meshing
**************

Introduction
============
The objective of this section is to create a family of volume meshes using pyHyp.
We previously used pyHyp to extrude our airfoil coordinates into a volume mesh.
However, this time we will use it to extrude our surface mesh coordinates into a volume mesh.
The surface mesh serves as the seed for hyperbolically marching the mesh to the farfield.
Generating the volume mesh in this way is fast, repeatable, and results in a high-quality mesh.
We will take advantage of the surface mesh coarsening features to generate a family of volume meshes.
Additionally, we will demonstrate a few additional settings in pyHyp compared to what was shown in the airfoil tutorial.

Files
=====
Navigate to the directory ``aero/meshing/volume`` in your tutorial folder.
Copy the following file from the surface meshing directory:

.. prompt:: bash

    cp ../surface/wing_surf_L1.cgns .

Create the following empty runscript in the current directory:

- ``run_pyhyp.py``

Dissecting the pyHyp runscript
==============================
Open the file ``run_pyhyp.py`` with your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
   :start-after: # rst Imports
   :end-before: # rst SetLevels

This is the standard way of importing the pyHyp library.
We also import the argument parser and setup it up to allow us to specify which level of mesh we want to extrude.

Setup parameters for each member of the mesh family
----------------
.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
   :start-after: # rst SetLevels
   :end-before: # rst general

We want to create a family of meshes with the L3 mesh being the coarseset and the L0.5 mesh being the finest.
In between we want an L2, L1.5, and L1 mesh.
Here we are goint to parse our input argument to determine which level of refinment we will generate on this run.
We default to L1 if the argument is invalid or no argument is provided.
Using the specified level of refinement we select the amount of surface mesh coarsening we will use, the number of off wall layers to extrude too, and the initial off wall spacing from a list.


Options
-------
.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :start-after: # rst general
    :end-before: # rst grid

Just like before we need to pass a dictionary of options to pyHyp for mesh extrusion.
Note that this time the options we use are a little different and that we need to take advantage for a few more options for a family of wing meshes.
A complete list of definitions of the pyHyp options can be found in the :doc:`pyHyp documentation <pyhyp:options>`.
Here we will point a few more of the options.

General options:

    ``inputFile``
        Name of the surface mesh file.

    ``fileType``
        Filetype of the surface mesh file.
        Either ``cgns`` or ``plot3d``.

    ``unattachedEdgesAreSymmetry``
        Tells pyHyp to automatically apply symmetry boundary conditions to any unattached edges (those that do not interface with another block).

    ``outerFaceBC``
        Tells pyHyp to which boundary condition to apply to the outermost face of the extruded mesh.
        Either ``farfield`` or ``overset``.

    ``families``
        Name given to wall surfaces. If a dictionary is submitted, each wall patch can have a different name. This can help the user to apply certain operations to specific wall patches in ADflow.

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :start-after: # rst grid
    :end-before: # rst pseudo

Grid parameters:
    ``coarsen``
        Automatically coarsen the surface mesh before starting extrusion. 
        ``1`` gives the same surface mesh. 
        ``2`` coarsens by a factor of 2 in each direction. 
        ``3`` coarsens by a factor of 4 in each direction, and so on. 
        Here will will pass in the value we selected from the list above for our specific mesh refinement level.

    ``N``
        Number of nodes in off-wall direction.
        Here will will pass in the value we selected from the list above for our specific mesh refinement level.
        If multigrid will be used this number should be 2\ :sup:`m-1` (n+1), where m is the number of multigrid levels and n is the number of layers on the coarsest mesh.

    ``s0``
        Thickness of first off-wall cell layer.
        Here will will pass in the value we selected from the list above for our specific mesh refinement level.

    ``marchDist``
        Distance of the far-field.

The following options are related to the algorithms that are used to generate the mesh and usually these default values do not need to be modified.
More information can be found in the :doc:`pyHyp documentation <pyhyp:index>`.
For example, ``epsE`` may be of interest when dealing with concave corners.
One thing to note there is that we have applied something called scheduleing to some of these parameters.
This is when we don't just pass a single value but a list of value pairs where the second term is the value of the parameter and the first is the point (as a fraction) in the mesh extrusion process it should be applied.

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :start-after: # rst pseudo
    :end-before: # rst smoothing

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :start-after: # rst smoothing
    :end-before: # rst solution

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :start-after: # rst solution
    :end-before: # rst run pyHyp

Running pyHyp is quite simple, as shown below.
After the mesh extrusion is done, we can write the volume mesh with the ``writeCGNS`` function.

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :start-after: # rst run pyHyp

Run it yourself!
================
When running you will need to specify which refinement level you want to generate.
For this tutorial having a L3, L2, and L1 mesh is sufficient but feel free to generate others.
You can now run the python file with the command:

.. prompt:: bash

    python run_pyhyp.py --level {insert refinement level here}

For larger meshes, you will want to run pyHyp as a parallel process.
This can be done with the command:

.. prompt:: bash

    mpirun -np 4 python run_pyhyp.py --level {insert refinement level here}

where the number of processors is given after ``-np``.
You can open ``wing_vol_{refine level}.cgns`` in Tecplot to view the volume mesh.
The output should look similar to the image below.

.. figure:: images/aero_wing_volume_mesh.png
    :scale: 20
    :align: center
    :alt: Wing volume mesh
    :figclass: align-center
