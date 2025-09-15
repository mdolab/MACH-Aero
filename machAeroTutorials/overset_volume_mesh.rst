.. _overset_volume_mesh:

*******************************************************
Volume Mesh
*******************************************************

Introduction
============
In this part, we will extrude the previously generated surface mesh into a volume mesh using pyHyp. As this is an
overset mesh, it consists of multiple sub-meshes (``near_wing``, ``near_tip`` and ``far``). After extruding all of them,
we will combine them into one single grid, that ADflow can read.

As we said in the previous tutorial, we want differently sized meshes. To accomplish this, we generated the finest and
will use this script to coarsen it multiple times. We will implement a basic command line parsing to tell the script
wich grid to generate. For example, a ``L1`` mesh would be generated like this:

.. prompt:: bash

    python run_pyhyp.py --level L1


Files
=====

Navigate to the directory ``overset/mesh`` in your tutorial folder and create an empty file called ``run_pyhyp.py``.
You will also need to copy the surface meshes from the tutorial folder if you did not generate it in the previous part:

.. prompt:: bash

    cp ../../../tutorial/overset/mesh/near_tip.cgns .
    cp ../../../tutorial/overset/mesh/near_wing.cgns .


pyHyp Script
============

Setup
-----
First we have to import some stuff:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst Imports (beg)
   :end-before: # rst Imports (end)

Then we need to setup up some libraries:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst Init (beg)
   :end-before: # rst Init (end)

The first line makes the processor number, on which this script is running, availabe. (Only used if it is parallelized
via MPI).

After that, we setup up the command line parsing with three arguments
(``--input_dir``, ``--output_dir`` and ``--level``)

Level Dependent Options
-----------------------
Next, we define some basic mesh parameters that depend on the level used:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst parameters (beg)
   :end-before: # rst parameters (end)

As you can see, for most options, we generate a ``dict`` with the three levels we want to create. Right after the dict,
an indexing happens (``[args.level]``). This way, we dont actually save the dict in the variables. We actually load the
value, that corresponds to the current level, to that variable.

Common pyHyp options
---------------------
We extrude multiple nearfield meshes with pyHyp. As there are a lot of options used for all meshes, we first define some
common `options <https://mdolab-pyhyp.readthedocs-hosted.com/en/latest/options.html>`_\:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst common_options (beg)
   :end-before: # rst common_options (end)

This options are quite basic and you should recognize most of them. Some overset specific ones are pointed out:

outerFaceBC
    This has to be set to ``overset``. This way ADflow knows it has to interpolate the outer faces and doesn't apply
    any boundary conditions.

marchDist
    Usually, the farfield should be located about 100 root chords away from the wing. Since we are only generating
    the nearfield, we use 2.5 root chords.

Individual pyHyp options
------------------------
Lets define some individual `options <https://mdolab-pyhyp.readthedocs-hosted.com/en/latest/options.html>`_\:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst individual_options (beg)
   :end-before: # rst individual_options (end)

The options in the ``wing_dict`` dictionary are applied to the ``near_wing`` mesh. The ``tip_dict`` is used for the
``near_tip`` mesh. This individual options overwrite the common options if the same key exists in both of them.

inputFile
    Since we have different surface meshes, we have to supply the inputfile name individually
outputFile
    We also want different output names. This way we can inspect the generated mesh separately
BC
    Here we apply the boundary conditions (BC). The integer defines the Domain (starting at 1). The dict key defines
    which side of the domain the BC applies to. The dict value defines the type of the BC.

    As it has been mentioned in the previous tutorial, there is not a reliable way to get this integer, which defines
    the domain, out of Pointwise. So it is recommended to rotate all domains in such a way, that the BC can be applied on
    the same side of all domains. Then they are deleted one by one until no
    more error messages pop up in pyHyp.
families
    Here we give a unique name to a surface. This lets ADflow calculate the forces seperately and would allow you, for example,
    to get the lift and drag forces for your wing and tail individually


Extrude the nearfield
---------------------

Now we extrude the nearfield:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst near_field (beg)
   :end-before: # rst near_field (end)

We start the extrusion by calling ``pyHypMulti``\. As arguments we give the previously defined common and individual options.
After the extrusion, we wait for all procs to finish before we continue.


Combine the nearfield
---------------------
The farfield consist of a cartesian part in the middle and a simple Ogrid around it. This cartesian part will
enclose all the nearfields. Because of that, we have to combine all the nearfields first:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst combine_near_field (beg)
   :end-before: # rst combine_near_field (end)

First, the script reads the files, then it combines them. In the end everything gets moved to ``y=0``.


Generate the farfield
---------------------
Now we can generate the farfield:

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst far_field (beg)
   :end-before: # rst far_field (end)

The arguments are explained in the pyHyp docs for :func:`~pyhyp:pyhyp.utils.simpleOCart`.


Combine everything
------------------
Here we combine all the meshes into one. We do this only on the root processor if we run it in parallel.

.. literalinclude:: ../tutorial/overset/mesh/run_pyhyp.py
   :start-after: # rst combine (beg)
   :end-before: # rst combine (end)


Run the Script
==============

To run the script, simply type this in your console:

.. prompt:: bash

    python run_pyhyp.py --level L1

If you have MPI installed and enough processors available, you can also run it in parallel:

.. prompt:: bash

    mpirun -np 4 python run_pyhyp.py --level L1

Since we want 3 meshes of different size, you will have to run this script 3 times with the appropriate
``--level`` argument.

Check the Final Mesh
====================

Finally, we can use the ``ihc_check.py`` script to check the result of the implicit hole cutting process in ADflow:

.. literalinclude:: ../tutorial/overset/mesh/ihc_check.py
   :start-after: # rst start
   :end-before: # rst end
