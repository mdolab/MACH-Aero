.. _overset_theory:

########################
Overset Theory
########################

The figures and the tips below are based off of the overset_guide document by Ney Secco.

Overset Mesh
=============

ADflow uses structured meshes.
For simple geometries, a valid structured mesh can be obtained by the multiblock structured mesh approach.
But it can be really hard to generate a single structured mesh for a complex geometry.
It might even be impossible to achieve the required mesh quality.

To mitigate this problem, the overset approach (also called chimera-patch) was implemented in ADflow.
Instead of having one big structured mesh, the fluid domain is split up in different, overlapping meshes.
The fluid solver then interpolates between these patches.
Typically, there are one farfield and multiple nearfield meshes:

.. figure:: images/overset_Overview.jpg
    :align: center

    Example of a farfield mesh embedding multiple nearfield meshes for the CFD mesh of NASA's STARC-ABL concept.
..
    src: https://openmdao.org/wp-content/uploads/2018/06/bli_16_9_clean.jpg

More about the overset implementation in ADflow can be found here: `An Efficient Parallel Overset
Method for Aerodynamic Shape Optimization
<https://www.researchgate.net/publication/313459613_An_Efficient_Parallel_Overset_Method_for_Aerodynamic_Shape_Optimization>`_\.

.. note:: As the solver has to interpolate in the overlapping region, the numerical solution will locally not be as accurate. It is recommended to avoid such overlapping near critical regions of the flowfield, like the wing tip.

Implicit Hole Cutting (IHC)
===========================
When there are overlapping meshes, one must decide which cells of one grid should exchange information with cells from an other grid.
Additionally, there will be some cells that should be ignored at all.
This process is called hole cutting.
For some solvers, the user must set it up in advance.
ADflow does this implicitly without any additional input.
It works on the assumption, that the cells closer to a wall, have a smaller volume.
If there are overlapping meshes, it basically uses the smaller cells, and the code blanks or interpolates the bigger ones.

.. figure:: images/overset_IHC.png
    :align: center

    Before (left) and after IHC (right).
..
    src: overset_guide.pdf page 7

More about IHC can be found here: `Implicit Hole Cutting - A New Approach to Overset Grid Connectivity
<https://arc.aiaa.org/doi/10.2514/6.2003-4128>`_\.


Zipper Mesh
===========
As seen in the first figure on this page, there can be multiple nearfield meshes that overlap on a surface.
This makes it hard to correctly integrate the forces and moments acting there.
For that reason, ADflow uses zipper meshes to provide a watertight surface.

.. figure:: images/overset_zipper.png
    :align: center

    Overlapped meshes (left), Removed overlaps (mid), Triangulated gaps (right)

..
    src: overset_guide.pdf page 20

More about zipper meshes can be found here: `Enhancements to the Hybrid Mesh Approach to
Surface Loads Integration on Overset Structured Grids
<https://www.nas.nasa.gov/assets/pdf/staff/Chan_W_Enhancements_to_the_Hybrid_Mesh_Approach_to_Surface_Loads_Integration_on_Overset_Structured_Grids.pdf>`_\.


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
Match cell sizes of the overlapped meshes, especially near boundaries

.. figure:: images/overset_tip2.png
    :align: center

    Left: Not recommended. May give a valid hole cutting with additional effort. Right: Better transition. Easier to find interpolation stencils.

Tip #3
------
Match the growth ratios of the mesh extrusion.

* Use similar values of initial cell height for all meshes (``s0`` option in pyHyp)
* Make sure that all meshes have similar growth ratios during the pyHyp extrusion. A variation of +- 0.05 is okay
* If you want to prioritize one mesh, use slightly smaller values for ``s0`` and growth ratio.

Debugging an Overset Mesh
=========================

The ADflow output might help you to debug an overset mesh.
The following points indicate a problem.

* Several flooding iterations
* Small number of compute cells
* Orphan cells are present

.. figure:: images/overset_bad_IHC.png
    :align: center
    :width: 400

    Bad IHC terminal output.

During the IHC, each cell gets an logical attribute, that defines if it should be calculated as usual, deactivated/blanked or used for interpolation between meshes.
The basic principle of IHC is to always use the smaller cell and blank the bigger one.
If you look at the cells of a farfield mesh that lie behind a body, there are no smaller cells to pick.
This means, they must be blanked by a different condition.
This condition is something like: "If a patch of cells is completely surrounded by interpolation cells, the whole patch can be blanked".
This is process is called ``flooding``.

An ``orphan cell`` is a cell, that could not find a corresponding cell on a different mesh for interpolation purposes.

More about this and the implementation of IHC in ADflow can be found `here <http://mdolab.engin.umich.edu/bibliography/Kenway2017a.html>`_



Flood troubleshooting
---------------------

The following points might help to fix your flooding issue.
Check them first.

Flooding is usually caused by cells that grow too fast off a wall.
    The mesh with a high growth ratio may cause the flooding of the other overlapped meshes, since the other meshes will not create a layer of interpolate cells to contain the flood.
    Check if meshes have similar growth ratios for the pyHyp extrusion.

Change the ``nearwalldist`` option in ADflow.
    This option controls how compute cells are preserved near walls.
    Changing this value may prevent flooding.
    We usually use 0.01 for a full-scale aircraft mesh defined in metric units.
    If a collar mesh is flooding, try increasing ``nearwalldist`` to reduce the number of flood seeds.

Check for sufficient overlap on the surface and in the volume.
    The overlap should have at least 5 cells from each mesh.

The background mesh may be too coarse.
    Either extend the near-field meshes or refine the background mesh until you have a 5 cell
    overlap along the off-wall direction.


Orphans troubleshooting
-----------------------
ADflow outputs the CGNS block id, and the i ,j ,k position of the orphan cells.
The k values (4th column) may point to the issue.

.. figure:: images/overset_orphan_debug.png
    :align: center
    :width: 450

    Output from a mesh with an orphan issue.

Orphans with high k: Lack of volume overlap.
    Some interpolate cells cannot find donors.
    So they become blanked cells within the stencil of a compute cell.
    Possible solutions are increasing the mesh extrusion distance (``marchDist`` option in pyHyp) or adding more layers to the mesh extrusion process (``N`` option in pyHyp).
    You may also refine the background mesh.

Orphans with small k: Reduce ``nearwalldist`` option in ADflow.
    You have compute cells beneath the surface defined by overlapping meshes.
    The smaller ``nearwalldist`` may flood these unnecessary cells.


More Overset Tips from Ney
==========================

Below is a text file containing several important tips about overset meshes from Ney Secco.

.. include:: ney_overset_tips.txt
   :literal: