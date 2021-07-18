.. _overset_theory:

##############
Overset Theory
##############

Overset Mesh
============

ADflow uses structured meshes.
For simple geometries, a valid structured mesh can be obtained by the multiblock structured mesh approach.
However, it can be difficult or even impossible to generate a high quality multiblock mesh for complex geometries.

To mitigate this problem, the overset approach (also called chimera-patch) was implemented in ADflow.
Overset meshes can be viewed as an *unstructured* network of overlapping *structured* meshes.
Instead of having one big structured mesh, the fluid domain is split up into separate, overlapping meshes.
Information is interpolated among overlapping meshes at every solver iteration.

.. figure:: images/overset_guide_3.jpg
    :align: center
    :width: 450

    A simple 2-D overset mesh. The nearfield mesh of the airfoil is red, and the background mesh is black.

..
    src: overset_guide.pdf page 3

The boundary conditions for this example is set as follows:

.. figure:: images/overset_guide_4.jpg
    :align: center
    :width: 600

    The boundary-condition information for the simple overset example.

..
    src: overset_guide.pdf page 4

Cells assume different tasks in an overset mesh:

* Compute cells: Active cells that are relevant to the solution as they represent the volume. The PDEs are enforced on these cells.
* Blanked cells: Inactive cells that are inside bodies or overlapped by better quality cells.
* Interpolated cells (Receivers): Cells that inherit state variables from donor cells belonging to other overlapping meshes.

The *compute cells* in an overset mesh for a more complicated configuration look like this:

.. figure:: images/overset_Overview.jpg
    :align: center

    Example of a farfield mesh embedding multiple nearfield meshes for the CFD mesh of NASA's STARC-ABL concept.
..
    src: https://openmdao.org/wp-content/uploads/2018/06/bli_16_9_clean.jpg

More about the overset implementation in ADflow can be found in `this paper <http://www.umich.edu/~mdolaboratory/pdf/Kenway2017a.pdf>`__.

.. note::

    Because the solver has to interpolate in the overlapping region, the numerical solution will locally not be as accurate.
    It is recommended to avoid such overlapping near critical regions of the flowfield, like the wing tip.

Implicit Hole Cutting (IHC)
===========================

ADflow uses implicit hole cutting (IHC) to automatically assign overset connectivities.
IHC is based on the assumption that cells are finer near walls.
IHC preserves smaller cells and blanks or interpolates larger ones.
The general theory behind IHC can be found in `this paper <https://arc.aiaa.org/doi/10.2514/6.2003-4128>`__.
In this section, we focus on the IHC implementation in ADflow.

.. figure:: images/overset_IHC.png
    :align: center

    The original mesh (left) and only the compute cells after IHC (right).
..
    src: overset_guide.pdf page 7

The ``iBlank`` array indicates the function of each cell.
ADflow saves this array in the volume or surface CGNS files if you add ``blank`` to the ``surfaceVariables``
or ``volumeVariables`` respectively.
The complete list of ``iBlank`` values in ADflow is:

*  1: Compute
*  0: Blanked
* -1: Interpolated
* -2: Flooded
* -3: Flood seed
* -4: Explicitly blanked (using ``cutCallBack``)
* -5: Orphan (flagged for debugging purposes only)

.. figure:: images/overset_guide_8.jpg
    :align: center

    The resulting ``iBlank`` values after the IHC process for the background and nearfield meshes.
..
    src: overset_guide.pdf page 8

In the figure above, the red cells represent the compute cells in each mesh.
The green cells are the interpolated cells, which bring in information from the overlapping compute cells.
The yellow cells represent the blanked cells.
These have no function in the flow solution but play an important role in the flooding process.

Flooding
--------

Flooding is the process used to determine which side of a wall should not be included in the flow solution.
This is usually the interior of a body such as a wing or aircraft.
Flooding starts at the flood seeds, which are the dark blue cells in the figure above.
A cell must satisfy two requirements to be designated as a flood seed.
First, the cell must intersect a wall on an overlapping mesh.
Second, the cell must be farther than ``nearWallDist`` from any wall in its own mesh.
In the example, the flood seeds are cells in the background mesh that overlap with the walls of the circle in the nearfield mesh.
The light blue cells are the flooded cells.
Compute cells that are next to a flood seed or a flooded cell are converted to flooded cells until the flooding is stopped by at least two layers of blanked or interpolated cells.
In the example, the flooded region is limited to the inside of the circle.
If we did not have enough resolution in the blanked and interpolated cells, the flood seeds would flood the rest of the mesh and the IHC would fail.

Orphan cells
------------

In the figure below, the center cell is marked with red, and all of the other cubes represent an exploded view of the computational stencil used in ADflow for RANS simulations.
The stencil for all compute cells (excluding cells at physical boundaries) should include only other compute or interpolated cells.
If this is not satisfied, the center cell is tagged as an *orphan* cell.
A valid mesh has no orphan cells.

.. figure:: images/cubeplot.jpg
    :align: center
    :width: 300

    The computational stencil used in ADflow for a second-order accurate finite-volume formulation for RANS equations.
    The center compute cell (marked with red) needs to access the state in all of the cells included in the figure to compute the residuals.
..
    src: ank paper stencil plots


Zipper Mesh
===========

As seen in the STARC-ABL figure on this page, there can be multiple nearfield meshes that overlap on a surface.
This makes it difficult to correctly integrate the forces and moments acting there.
For that reason, ADflow uses zipper meshes to provide a watertight surface.
More about zipper meshes can be found `this paper <https://www.nas.nasa.gov/assets/pdf/staff/Chan_W_Enhancements_to_the_Hybrid_Mesh_Approach_to_Surface_Loads_Integration_on_Overset_Structured_Grids.pdf>`__.

.. figure:: images/overset_zipper.jpg
    :align: center

    Overlapped meshes (left), Removed overlaps (mid), Triangulated gaps (right)

..
    src: overset_guide.pdf page 20


Collar Mesh
===========

Collar meshes outline the intersection between two component meshes.
The collar mesh should be finer than the overlapping component meshes.
This ensures that the collar cells are selected during IHC and there are no gaps at the intersection.

.. figure:: images/overset_guide_10.jpg
    :align: center

    The collar mesh at the wing-strut intersection of a strut-braced wing configuration.
..
    src: overset_guide.pdf page 10

We can also use a half-collar to reduce the number of overset blocks.
In the following example, the half-collar on the fuselage belongs to the tail mesh.
The half-collar and the rest of the tail mesh share the intersection line.

.. figure:: images/overset_guide_11.jpg
    :align: center
    :width: 400

    An example of a half-collar at the fuselage-horizontal tail region.
..
    src: overset_guide.pdf page 11


Steps to Create an Overset Mesh
===============================

Here is a list of commonly used steps to create an overset mesh with the usual workflow in the MDO Lab:

#. Generate surface meshes for the main components in ICEM.
#. Extrude surface meshes into volume meshes using pyHyp.
#. Generate a background mesh using cgnsUtilities.
#. Merge blocks in a single file using cgnsUtilities.
#. Check connectivities using ADflow.

Tips for Getting a Valid Overset Mesh
=====================================

Tip #1
------
Make sure there is sufficient overlap between meshes.

.. figure:: images/overset_tip1.png
    :align: center

    Overlapping is needed between meshes.

Tip #2
------
Match cell sizes of the overlapped meshes, especially near boundaries.

.. figure:: images/overset_tip2.png
    :align: center

    Left: Not recommended. May give a valid hole cutting with additional effort. Right: Better transition. Easier to find interpolation stencils.

Tip #3
------
Match the growth ratios of the mesh extrusion.

* Use similar values of initial cell height for all meshes (``s0`` option in pyHyp)
* Make sure that all meshes have similar growth ratios during the pyHyp extrusion.
  Variations within 0.05 are acceptable.
* If you want to prioritize one mesh, such as a collar mesh, use a slightly smaller value for ``s0`` and aim for a slightly smaller growth ratio.

.. figure:: images/overset_guide_14.jpg
    :align: center

    Output from pyHypMulti showing how to find the grid ratio value.
..
    src: overset_guide.pdf page 14

Debugging an Overset Mesh
=========================

The ADflow output might help you to debug an overset mesh.
Here is what the output from a valid IHC process looks like:

.. figure:: images/overset_guide_15.jpg
    :align: center
    :width: 400

    ADflow output with a successful hole cutting. This results in a valid overset mesh.
..
    src: overset_guide.pdf page 15

The following points indicate a problem:

* Several flooding iterations
* Small number of compute cells
* Orphan cells are present

.. figure:: images/overset_bad_IHC.png
    :align: center
    :width: 400

    Bad IHC output.

Flood troubleshooting
---------------------

If the mesh is flooding (too many flooding iterations, a high number of flooded cells), we need to first prevent this to get a valid hole cutting.
For this, we need to check leaks in the flooding process:

#. Set the ADflow option: ``"nRefine": 1``.
   This stops the IHC algorithm after one iteration.
   You will get a warning, but this is fine.
   We just want to get an intermediate output for debugging.
   You can also modify the ``nFloodIter`` option to control how many *flooding* iterations are performed.
   For example, if ADflow segfaults in the first overset iteration because the whole mesh floods, then you can stop the flooding iterations early by setting ``nFloodIter`` to 1 or 2.
   A value of 1 will just determine the flood seeds, a value of 2 will do a first pass of the flooding process.
#. Set ADflow option: ``"useZipperMesh": False``.
   This skips the zipper mesh generation, which may crash if the hole cutting does not work.
#. Run the overset check file: ``ihc_check.py``.
   (This can be found under the tutorial/overset/mesh directory in this repo.)
#. Open the output volume file in Tecplot.
#. Use the blanking option to show only ``iBlank`` = -3 (flood seeds) and ``iBlank`` = -2 (flooded cells).
#. Check which CGNS blocks are fully flooded.
   Identify the flood cells that connect cells inside the body to cells outside the body.
   This is where the leak occurs.

The following points might help to fix your flooding issue.
Check them first.

Check if the meshes have similar growth ratios in the pyHyp extrusion.
    Flooding is usually caused by cells that grow too fast off a wall.
    A mesh with a high growth ratio may cause the flooding of the other overlapped meshes because the other meshes will not create a layer of interpolated cells to contain the flood.

Increase the ``nearWallDist`` option in ADflow.
    This option controls how compute cells are preserved near walls.
    We usually use 0.01 for a full-scale aircraft mesh defined in meters.
    Increasing ``nearWallDist`` will reduce the number of flood seeds.
    Once you have a valid hole cutting, decrease ``nearwalldist`` to the minimum possible value.

Check for sufficient overlap on the surface and in the volume.
    The overlap should have at least 5 cells from each mesh.
    Either extend the nearfield meshes or refine the background mesh until you have a 5 cell overlap in the off-wall direction.

.. warning::
    Even if the IHC is valid, the flooding may not behave as expected.
    Thin geometries at component intersections can cause problems with flooding and result in flow through solid surfaces.
    Increase the mesh density at the intersection to avoid this.

Troubleshooting orphan cells
----------------------------

ADflow outputs the CGNS block ID and the i, j, k position of the orphan cells.
The k values (4th column) represent the position in the off-wall direction and may point to the issue.

.. figure:: images/overset_orphan_debug.png
    :align: center
    :width: 450

    Output from a mesh with orphan cells.

Orphans with high k
    There is a lack of volume overlap and some interpolated cells cannot find donors.
    Possible solutions are increasing the mesh extrusion distance (``marchDist`` option in pyHyp) or adding more layers to the mesh extrusion process (``N`` option in pyHyp).
    You can also refine the background mesh.

Orphans with small k
    ``nearWallDist`` is too large and there are compute cells on the wrong side of the surface defined by overlapping meshes.
    Try reducing ``nearWallDist``.
