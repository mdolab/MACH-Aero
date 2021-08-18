.. _overset_surface_mesh:

*********************************
Surface Mesh
*********************************

Introduction
============
Now that we have a geometry, we can start meshing it.
We are using Pointwise to generate the surface mesh.
This is not a full blown tutorial, more a walk through.
If you want to learn more about it, their `Youtube channel <https://www.youtube.com/user/CFDMeshing>`_ is highly recommended.
You do not have to use Pointwise to generate an overset mesh.
ICEM or an other meshing software would work as well.

Files
=====
Navigate to the directory ``overset/mesh`` in your tutorial folder. Either use the previously generated ``.igs`` file or copy it from the tutorial folder.

.. prompt:: bash

    cp ../../../tutorial/overset/geo/onera_m6.igs .

It is possible to script Pointwise. In order to use it, we have to download the script first. You can either
`download <https://raw.githubusercontent.com/pointwise/Semicircle/master/Semicircle.glf>`_ it here or copy it
from the tutorial folder.

.. prompt:: bash

    cp ../../../tutorial/overset/mesh/Semicircle.glf .

Meshing strategy
================
Before we start meshing, we have to know how many meshes we create and where they overlap. For this tutorial,
3 different meshes are proposed: ``near_wing``, ``near_tip`` and ``far``. The following picture should give an overview:

.. figure:: images/overset_m6_mesh_fields.png
    :width: 500
    :align: center

    The three overset meshes.

Now we should estimate the cell count of the mesh. For the purpose of a grid convergence study (GCS) and debugging
it makes sense to have differently refined meshes. To limit the amount of work, we will create the finest mesh and
coarsen it multiple times.

Usually, the finest mesh is called ``L0`` (level 0) and should have approx 60M cells for this geometry. If every 2 cells
are combined in each direction, we get a coarser mesh called ``L1``. This usually goes to ``L2`` for production and ``L3`` for
debugging purposes. Additionally, there could be an intermediate level starting at ``L0.5``. It requires a different
surface mesh that is sqrt(2) coarser than ``L0``. In this tutorial, we will start at ``L1`` (~8M cells) and end at ``L3``
(~0.125M cells).

Mesh Generation
===============

Pointwise overview
------------------
If you start Pointwise, it should look something like in the next picture.

1. Object, Layer and Default control
2. Solver information
3. Selection control
4. View control
5. Fast meshing controls

.. figure:: images/overset_pointwise_overview.png
    :width: 600
    :align: center

    Pointwise Overview.

You can control the main view with the following key- and mouse combinations:

zoom
  Rotate your ``mouse wheel``. The zoom centers around your ``mouse pointer``.

rotate
  Press ``ctrl`` and your ``right mouse button`` while moving your mouse.

move
  Press ``shift`` and your ``right mouse button`` while moving your mouse.


Setup Pointwise
---------------
Before we actually begin meshing, we have to set some standard values and import our geometry. At first, we set some
tolerances for Pointwise

1. Click on ``File`` -> ``Properties``
2. Set ``Model Size`` to ``1``. (It is enough, if the order of magnitude is similar)
3. Set ``Node`` to ``1e-6``. The value of ``Connector`` should automatically jump to ``1e-6`` as well
4. ``OK``

Now we have to choose the proper solver. In my case it is ``CGNS`` with ``adf`` support. If you have compiled the
MACH-Framework with ``hdf5`` support, you can skip the last step.

1. Click ``CAE`` -> ``Select Solver``
2. Make Sure ``CGNS`` is selected.
3. Click ``OK``.
4. Click ``CAE`` -> ``Set Dimension`` -> ``2D`` (That's how surface meshes are called here)
5. Click ``CAE`` -> ``Set Solver Attributes`` (If you have ``hdf5`` support, you can stop here)
6. Select ``adf`` for ``CGNS File Type``
7. Click ``Close``

Now we can import the ``.iges`` file we created in the previous tutorial.

1. Click ``File`` -> ``Import`` -> ``Database``
2. Select your ``.iges`` File -> ``open``
3. Make sure nothing but ``Units`` and ``From File`` is selected
4. Click ``OK``
5. You will receive a warning that some entities could not be converted. Just ignore it and click ``YES``

After those steps, the window should look like this (you should probably save at this point):

.. figure:: images/overset_pointwise_after_import.png
    :width: 600
    :align: center

    Pointwise after setup.

Few important Pointwise labels:

Block
    This is a 3 dimensional Mesh
Domain
    This is a 2 dimensional Mesh
Connector
    A line constraining the extend of a ``Block`` or ``Domain``
Database
    An imported geometry
Spacing Constraint
    This controls how the ``nodes`` lay on a ``Connector``. Further down the line, the ``Connector`` controls
    how the ``nodes`` lay in a ``Domain`` or ``Block``


Prepare the Database
--------------------

To make our live a bit easier in the coming mesh work, we first prepare the database a bit (take a look at the next
picture to help guide you).

1. Select the whole ``database``. Just draw a rectangle around it while your ``left mouse button`` is pressed
2. Click ``Wireframe`` -> ``Shaded``
3. Click on ``Layers``
4. Double click on ``Description`` and enter ``Geo``

.. figure:: images/overset_pointwise_dat1.png
    :width: 600
    :align: center

    Prepare the database #1.


Because we have two overlapping meshes (``near_wing`` and ``near_tip``), we have to cut the database at an appropriate place.
This will indicate where the ``near_tip`` mesh will start. The ``near_wing`` mesh will go right to the tip of the wing. But
because ADflow uses an ``Implicit Hole Cutting Scheme`` we only have to make sure, that the ``near_tip`` mesh is slightly smaller
than the ``near_wing`` mesh. This will ensure, that the overlapping region is approximately where we cut the database. In this
way we are certain, the solver does not have to interpolate in a critical region (like the wing tip).

1. Click on ``Create`` -> ``Planes``
2. Choose ``Constant X, Y or Z``
3. Select ``Y`` and enter a value of ``0.9``
4. Click ``OK`` (Your view should now look like detail ``A`` in the following picture)
5. Select only the ``upper``, ``lower`` and ``trailing edge`` surface by drawing a rectangle with your ``left mouse button``
6. Click ``Edit`` -> ``Trim by Surfaces``
7. Select your freshly created plane (detail ``A``)
8. Make sure ``Tolerance`` and ``Advanced`` is unselected
9. Click ``Imprint`` (Your geometry should now have a different color towards the tip)
10. Click ``OK``

.. figure:: images/overset_pointwise_cut_database.png
    :width: 600
    :align: center

    Cut the database.


Now we are doing some cleaning up and delete some unneeded surfaces.

1. Rotate your view with pressing ``ctrl`` and your ``right mouse button`` while moving your mouse until you have a good view on the root surfaces.
2. Select the first ``root surface``
3. Press ``ctrl`` while selecting the second ``root surface``
4. Press ``del`` on your keyboard to delete them

.. figure:: images/overset_pointwise_del_root.png
    :width: 600
    :align: center

    Delete the root surfaces.



Create the ``near_wing`` surface mesh
-------------------------------------
We create the mesh ``near_wing`` in a new layer to keep everything orderly.

1. Click ``Layers``
2. Select ``Show Empty Layers``
3. Click with your ``right mouse button`` on layer ``10`` -> ``Set Current``
4. Double click with your ``left mouse button`` on the ``Description`` of layer ``10`` and enter ``near_wing``
5. Unselect ``Show Empty Layers``

.. figure:: images/overset_pointwise_near_layer.png
    :width: 600
    :align: center

    Create a new layer for ``near_wing``.


Because we want to coarsen our mesh multiple times, it is important to think about how many nodes we should have on a
connector (Apart from that, it is always good to be multi-grid-friendly). To calculate the number of nodes (:math:`N`) per connector, we
use this formula:

.. math::

    N=2^n m + 1

Where :math:`n` is the ``number of refinements + 1`` and :math:`m` is an ``integer``. For our chord-wise direction, we will
use ''145'' Nodes. To save some work, we will set it as default.

1. Click ``Defaults``
2. Make sure ``Connector`` is checked
3. Select ``Dimension`` and enter ``145``
4. Select the ``upper`` and ``lower`` surface of the wing
5. Click ``Connectors on Database Entities``
6. Click on ``Layers`` and uncheck the ``Geo`` layer
7. Select the ``two connectors`` in the middle of the wing (Detail A) and delete them. They showed up because we split the database
8. Select the ``6 spanwise connectors`` (Detail B)
9. Click ``Edit`` -> ``Join``

.. figure:: images/overset_pointwise_near_wing1.png
    :width: 600
    :align: center

    Create the connectors for the ``near_wing`` mesh.

When creating the connectors, we left out the TE. We did this because there were 2 surfaces from OpenVSP. It is less work for us,
if we manually create two connectors.

1. Click ``Defaults``
2. Select ``Dimension`` and enter ``17``
3. Click ``2 Point Curves``
4. Close the ``root trailing edge`` (make sure your pointer becomes a cross-hair before you click. This way you are sure the new connector lies on the closest point)
5. Close the ``tip trailing edge``
6. Press ``OK``

.. figure:: images/overset_pointwise_near_close_TE.png
    :width: 600
    :align: center

    Close the trailing edge.

Now we initialize the surface mesh.

1. Select ``everything``
2. Click ``Assemble Domains``
3. Select ``everything``
4. Click on the ``small arrow pointing down`` next to ``Wireframe``
5. Click on ``Hidden Line``

.. figure:: images/overset_pointwise_near_init.png
    :width: 600
    :align: center

    Initialize the ``near_wing`` mesh.

Now we ``size`` the LE (Leading Edge) and TE (Trailing Edge) connectors.

1. Click on ``All Masks On/Off``
2. Click on ```Connectors``
3. Select the ``LE`` and ``TE`` ``Connectors`` by drawing a rectangle like it is shown
4. Click on the input field next to ``Dimension``, enter ``73`` and hit ``enter``

.. figure:: images/overset_pointwise_near_dimension_LETE.png
    :width: 600
    :align: center

    Dimension the LE & TE connectors.

The surface mesh is now almost complete. We only have to distribute the nodes on it properly by changing the ``spacing``.
Usually all Points are distributed according to ``Tanh``. But because we split up the database in the previous steps,
we have to remove so called ``break point`` at that location.

.. note:: ``Break Points`` give you even more control to distribute your nodes on a connector.

1. Select the ``LE`` and ``TE`` connectors again.
2. Click on ``Grid`` -> ``Distribute``
3. Click on ``Break Points``
4. Click on ``Delete all Break Points``
5. Click on ``OK``

.. figure:: images/overset_pointwise_near_del_break_points.png
    :width: 600
    :align: center

    Delete unneeded Break Points.

1. Click on ``All Masks On/Off``
2. Click on ``Spacing Constraints``
3. Select the 2 spacing constraints at the ``LE`` of the ``root`` (A)
4. Click the field next to ``Spacing`` and enter ``0.0003``. Then hit ``enter``
5. Select the 2 spacing constraints at the ``TE root`` (B)
6. Apply ``7.15e-5`` for spacing
7. Select the 2 spacing constraints at the ``LE tip`` (C)
8. Apply ``0.00016`` for spacing
9. Select the 2 spacing constraints at the ``TE tip`` (D)
10. Apply ``4e-5`` for spacing
11. Select the 3 spacing constraints at the ``tip`` (E)
12. Apply ``0.0025`` for spacing
13. Select the 3 spacing constraints at the ``root`` (F)
14. Apply ``0.04`` as spacing

.. figure:: images/overset_pointwise_near_spacing.png
    :width: 600
    :align: center

    Apply the proper spacing.

The mesh ``near_wing`` is now complete. We will export it later.



Create the ``near_tip`` surface mesh
------------------------------------

Now we will create the ``near_tip`` mesh. Let's start with creating a new layer and hide everything unnecessary.

1. Click on ``Layers``
2. Check ``Show Empty Layers``
3. Right click on Layer ``20`` -> ``Set Current``
4. Double click the ``Description`` Field and enter ``near_tip``
5. Uncheck ``Show Empty Layers``
6. Check Layer ``0`` to make the database visible
7. Hide the mesh ``near_wing`` by un-checking layer ``10``

Now we will create the connectors.

1. Click on ``Defaults`` -> enter ``201`` for ``Dimension``
2. Select everything from the tip to the cut we made earlier
3. Click ``Connectors on Database Entities``
4. Click on ``Layers`` -> uncheck layer ``0``. Now, you should only see the connectors we created

Let's clean up the generated connectors at the tip TE.

1. Zoom into the ``tip TE``
2. Select the ``5`` shown ``connectors`` (A)
3. Delete them
4. Select and delete the remaining ``pole`` (the point with a circle around) (B)
5. Select the ``2`` ``connectors`` that define the outer tip (C)
6. Click ``Edit`` -> ``Join``
7. Select the ``newly joined`` connector (C)
8. Enter ``65`` For ``Dimension`` and hit ``enter``
9. Click on ``Defaults`` and enter ``65`` for ``Dimension``
10. Click on ``2 Point Curves``
11. Close the ``TE`` again (D)

.. figure:: images/overset_pointwise_tip_clean_tip.png
    :width: 600
    :align: center

    Clean up the ``tip TE``.

Next we clean up the root TE.

1. Select the ``2`` ``connectors`` that define the TE (A)
2. Delete them
3. Click on ``2 Point Curves``
4. Close the Tip again (B)

.. figure:: images/overset_pointwise_tip_clean_root.png
    :width: 600
    :align: center

    Clean up the ``root TE``.

The last thing to clean up is the ``tip LE``.

1. Select the ``3`` shown ``connectors`` (A)
2. Click on the ``arrow pointing down`` next to ``show``
3. Click ``Hide``
4. Select and delete the remaining ``pole`` (B)
5. Click on ``View`` -> ``Show Hidden``
6. Select the ``3`` ``connectors`` (A)
7. Click on the ``arrow pointing down`` next to ``Hide``
8. Click on ``Show``

.. figure:: images/overset_pointwise_tip_clean_LE_tip.png
    :width: 600
    :align: center

    Clean up the ``tip LE``.

Now we will dimension the remaining connectors and space the nodes properly.

1. Select the ``3`` shown connectors (A)
2. Enter ``97`` for ``Dimension`` and hit ``enter``
3. Click ``All Masks On/Off``
4. Click ``Spacing Constraints``
5. Select the ``2`` spacing constraints at the ``root LE`` (B)
6. Apply ``0.0008`` for spacing
7. Select the ``2`` spacing constraints at the ``tip LE`` (C)
8. Apply ``0.0008`` for spacing
9. Select the ``2`` spacing constraints at the ``root TE`` (D)
10. Apply ``1.3e-5`` as spacing
11. Select the ``2`` spacing constraints at the ``tip TE`` (E)
12. Apply ``1.3e-5`` as spacing
13. Select the ``3`` spacing constraints at the ``root`` (F)
14. Apply ``0.01`` as spacing
15. Select the ``1`` spacing constraint at the ``tip LE`` (G)
16. Apply ``0.0005`` as spacing
17. Select the ``2`` spacing constraints at the ``tip TE`` (H)
18. Apply ``1.56e-5`` as spacing

.. figure:: images/overset_pointwise_tip_spacing.png
    :width: 600
    :align: center

    Apply spacing constraints for the ``near_tip`` mesh.

Next, we split the connectors at the tip to allow a topology where we can achieve a decent quality mesh.

1. Select the ``tip top`` connector (A)
2. Click ``Edit`` -> ``Split``
3. Make sure ``Advanced`` is checked
4. Enter ``17`` for ``IJK`` and hit ``enter``
5. Click ``OK``
6. Select the ``tip bottom`` connector (B)
7. Click ``Edit`` -> ``Split```
8. Enter ``185`` for ``IJK`` and hit ``enter``
9. Click ``OK``
10. Click on ``2 Point Curves``
11. Connect the ``2`` new ``points`` (A) to (B)

.. figure:: images/overset_pointwise_tip_split_le_con.png
    :width: 600
    :align: center

    Split the ``tip`` connectors.

Since our tip is rounded, we have to ``project`` the newly created connector on to our database.

1. Select the ``newly`` created ``connector`` (A)
2. Click on ``Edit`` -> ``Project``
3. Click on ``Layers``
4. Check layer ``0`` (``Geo``)
5. Click on ``Project``
6. Make sure ``Target Database Selection`` is checked
7. Click ``Begin``
8. Select the ``upper`` and ``lower`` tip surface (hold down ``ctrl``) (B)
9. Click ``End``
10. Click ``Project``
11. Click ``OK``

.. figure:: images/overset_pointwise_tip_project.png
    :width: 600
    :align: center

    Project the connector on to the database.

Now we actually start meshing.

1. Click on ``Layers``
2. Uncheck layer ``0`` (``Geo``)
3. Select the ``newly`` created ``connector`` (A)
4. Click on the ``arrow pointing down`` next to ``Tanh Distribution``
5. Click on ``Equal``
6. Click ``Edit`` -> ``Split``
7. Enter ``17`` for ``IJK`` and hit ``enter``
8. Enter ``49`` for ``IJK`` and hit ``enter``
9. Click ``OK``
10. Click on ``Create`` -> ``Assemble Special`` -> ``Domain``
11. Select ``1`` ``connector`` (B)
12. Click ``Next Edge``
13. Select ``2`` ``connectors`` (C)
14. Click ``Next Edge``
15. Click ``OK``

.. figure:: images/overset_pointwise_tip_mesh_LE_tip.png
    :width: 600
    :align: center

    Assemble the mesh at the ``LE tip``.

Next, we mesh the rest.

.. 1. Download `this Script <https://raw.githubusercontent.com/pointwise/Semicircle/master/Semicircle.glf>`_ and save it somewhere

1. Select the ``2`` connectors that form the semi-circle (A)
2. Click ``Script`` -> ``Execute``
3. Look for the ``script`` you just downloaded and ``open`` it.
4. Select ``all`` connectors
5. Click ``Assemble Domains``

.. figure:: images/overset_pointwise_tip_semi-circle.png
    :width: 600
    :align: center

    Mesh the ``semi-circle``  at the TE.

The last step is to make sure, that the skewed elements at the tip are smoothed. As ``Assemble Domains`` didn't work
for the most outer mesh, we will delete this domain first, and create it manually again.

1. Select ``all`` domains
2. Click ``Hidden Line``
3. Select the ``outer most`` domain and delete it (A)
4. Select all ``9`` connectors, that define the last remaining domain
5. Click ``Assemble Domain``
6. Select the ``newly`` created ``domain`` and click ``Hidden Line``
7. Select the ``2`` domains that define the ``tip`` (A & B)
8. Click ``Grid`` -> ``Solve``
9. Click on ``Edge Attributes``
10. Make sure ``Boundary Conditions`` is checked and set the ``Type`` to ``Floating``
11. Click on ``Attributes``
12. Make sure ``Surface Shape`` is checked and set ``Shape`` to ``Database``
13. Click on ``Begin`` and make sure, the tip is selected (it should be)
14. Click on ``End``
15. Make sure ``Solution Algorithm`` is checked and set ``Solver Engine`` to ``Successive Over Relaxation``
16. Set ``Relaxation Factor`` to ``Nominal``
17. Click on ``Solve``
18. Enter ``50`` for ``Iterations`` and hit ``Run``
19. Click ``OK``

.. figure:: images/overset_pointwise_tip_solve.png
    :width: 600
    :align: center

    Finish the ``near_tip`` mesh.

Lets check the quality of the created mesh. The most important metrics are ``Area Ratio`` and ``Equiangle Skewness``.

1. Select ``all`` domains
2. Click ``Examine`` -> ``Area Ratio``
3. Click on the ``Magnification Glass`` next to ``max``
4. You see, the biggest ``Area Ratio`` is ``~2.24``
5. Click on ``Advanced``
6. Make sure ``Histogram`` and ``Show Histogram`` are checked
7. As you see, the vast majority of cells has an ``Area Ratio`` of less than ``1.25``. This should be fine
8. Click on ``Examine``
9. Choose ``Skewness Equiangle`` for ``Type``
10. As you can see, the most skewed cell has a ``Skewness Equiangle`` of ``~0.4``. This is also fine
11. Click ``Close``

.. note::
    The lower max ``Area Ratio`` is, the easier it is to extrude a mesh with pyHyp. If it is more than ``2``,
    it can get tricky. ``Skewness Equiangle`` describes how skewed a cell is. It should be below ``0.8``

.. figure:: images/overset_pointwise_tip_examine.png
    :width: 600
    :align: center

    Check the mesh quality.


Export all meshes for use in pyhyp
==================================

The last step is to export the mesh. For pyHyp it is important, that the ``normals`` look in the outwards direction.
We will set the boundaries manually in pyHyp.

.. note::
    As there has not been found an easy way to figure out which domain in Pointwise
    corresponds to which domain in pyHyp, it is recommended to orient them all the same way. Then apply the BC for all domains and run the pyHyp script.
    If an error pops up for one domain, the corresponding BC can be removed. This gets repeated until there are no errors left (This information is repeated
    on the next page where it probably makes more sense).


Lets start with orienting the ``near_tip`` mesh first.

1. Make sure only the layer ``near_tip`` is visible
2. Select ``all`` domains
3. Click ``Edit`` -> ``Orient``
4. Select ``one`` domain (It does not matter which one)
5. Click ``I-J`` a few times until you are sure, the ``orange arrow`` is pointing outwards
6. Click ``Set Master``
7. Select ``all`` domains
8. Click ``Align``
9. Click ``OK``

.. figure:: images/overset_pointwise_orient_near_tip.png
    :width: 600
    :align: center

    Orient the ``near_tip`` mesh so all normals point outwards.

Now we can export it.

1. Select ``all`` domains
2. Click ``File`` -> ``Export`` -> ``CAE``
3. Set ``near_tip`` as Filename and save it somewhere
4. Make sure ``Data Precision`` and ``double`` is checked
5. You can uncheck ``the rest`` (It doesn't really matter. But the files will be bigger if you leave it on)
6. Press ``OK``

.. figure:: images/overset_pointwise_export_near_tip.png
    :width: 600
    :align: center

    Export the ``near_tip`` mesh.

Now lets do the same for the ``near_wing`` mesh. As we have a symmetry boundary condition, the orientation
procedure is slightly more complicated.

1. Make sure only the layer ``near_wing`` is visible
2. Select ``all`` domains
3. Click ``Edit`` -> ``Orient``
4. Select ``one`` domain (It doesn't matter which one)
5. Click ``I-J`` until the ``orange arrow`` is pointing outwards
6. If the ``red arrow`` is not pointing towards the tip, click ``I`` and ``I-J`` until both conditions are satisfied
7. Click ``Set Master``
8. Select ``all`` domains
9. Click ``Align``
10. Make sure all ``red arrows`` point towards the tip (if this is not the case, select this domain and repeat step 6)
11. Click ``OK``

Now you can export the mesh ``near_wing`` like you did in the previous step.

Congratulations, you managed to create the surface mesh. On the next page, we will extrude it into a volume mesh.