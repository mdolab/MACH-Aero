.. _aero_pyhyp:

**************
Volume Meshing
**************

Introduction
============
The objective of this section is to create a volume mesh using pyHyp.
The surface mesh serves as the seed for hyperbolically marching the mesh to the farfield.
Generating the volume mesh in this way is fast, repeatable, and results in a high-quality mesh.
More details on pyHyp can be found in the :doc:`pyHyp documentation <pyhyp:index>` or in the code itself.

Files
=====
Navigate to the directory ``aero/meshing/volume`` in your tutorial folder.
Copy the following file from the surface meshing directory:

.. prompt:: bash

    cp ../surface/wing.cgns .

Create the following empty runscript in the current directory:

- ``run_pyhyp.py``

Dissecting the pyHyp runscript
==============================
Open the file ``run_pyhyp.py`` with your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries
----------------
.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
   :language: py
   :start-after: # rst Imports
   :end-before: # rst general

This is the standard way of importing the pyHyp library.

Options
-------
For each module in MACH, we generally pass in options using a dictionary.
A complete list of definitions of the pyHyp options can be found in the :doc:`pyHyp documentation <pyhyp:options>`.
Here we will point a few of the more basic options.
For pyHyp, the options can be organized like so:

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :language: py
    :start-after: # rst general
    :end-before: # rst grid

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
    :language: py
    :start-after: # rst grid
    :end-before: # rst pseudo

Grid parameters:

    ``N``
        Number of nodes in off-wall direction.
        If multigrid will be used this number should be 2\ :sup:`m-1` (n+1), where m is the number of multigrid levels and n is the number of layers on the coarsest mesh.

    ``s0``
        Thickness of first off-wall cell layer.

    ``marchDist``
        Distance of the far-field.

The following options are related to the algorithms that are used to generate the mesh and usually these default values do not need to be modified.
More information can be found in the :doc:`pyHyp documentation <pyhyp:index>`.
For example, ``epsE`` may be of interest when dealing with concave corners.

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :language: py
    :start-after: # rst pseudo
    :end-before: # rst smoothing

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :language: py
    :start-after: # rst smoothing
    :end-before: # rst solution

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :language: py
    :start-after: # rst solution
    :end-before: # rst run pyHyp

Running pyHyp is quite simple, as shown below.
After the mesh extrusion is done, we can write the volume mesh with the ``writeCGNS`` function.

.. literalinclude:: ../tutorial/aero/meshing/volume/run_pyhyp.py
    :language: py
    :start-after: # rst run pyHyp

Run it yourself!
================
You can now run the python file with the command:

.. prompt:: bash

    python run_pyhyp.py

For larger meshes, you will want to run pyHyp as a parallel process.
This can be done with the command:

.. prompt:: bash

    mpirun -np 4 python run_pyhyp.py

where the number of processors is given after ``-np``.
You can open ``wing_vol.cgns`` in Tecplot to view the volume mesh.
The expected mesh output is shown below.

.. figure:: images/aero_wing_volume_mesh.png
    :scale: 20
    :align: center
    :alt: Wing volume mesh
    :figclass: align-center
