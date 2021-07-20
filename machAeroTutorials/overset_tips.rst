.. _overset_tips:

########################
Tips and Troubleshooting
########################

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

Troubleshooting an Overset Mesh
===============================

The ADflow output might help you to troubleshoot an overset mesh.
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
   We just want to get an intermediate output for visualization.
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
