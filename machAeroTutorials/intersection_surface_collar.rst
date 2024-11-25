.. _intersection_surface_collar:

Surface Collar Meshing
======================

.. note::

    For this tutorial, we assume that you have completed the :ref:`MACH-Aero ICEM tutorial <mach-aero:aero_icem>` and that the component meshes are ready.

#. ``.tin`` files for the wing and fuselage geometries are located in ``meshing/surface``.
   Load both geometry files into a project.
#. Create a 3D bounding box around both geometries.
#. Convert the bounding box to 2D blocking.
#. Looking head on at the aircraft (in the positive x-direction), delete the left and right blocks.
#. Split the remaining blocks into 2 so that there are now 8 blocks.
#. Associate the 4 blocks closer the to symmetry plane to the fuselage and the other 4 blocks to the wing.
   Associate points to the surface for the fuselage block.
   The blocking for the wing is similar to a regular wing mesh but truncated such that there is no tip closure.
#. Create points in ICEM as a reference for the amount of overlap needed.
   For example, if you want to create a surface mesh that can be coarsened twice, aim for 20 cells of overlap on the component surface meshes.
#. Move the vertices on the blocks until you reach the desired overlap.
#. Set some initial spacings.
   At the intersection, use uniform spacing for the leading and trailing edges, and hyperbolic or bigeometric for the upper and lower surface edges.
   Make sure the spacing and growth ratio on either side of the intersection are roughly equal.
   In addition, the growth ratio should be close to one to avoid clustering nodes at concave corners.
   Use the component meshes as a reference for the cell sizes.
   Make sure the collar mesh cells are slightly finer than the component at the intersection and a similar size in the interpolation region.

    .. note::

        Do not consider off-wall spacing when creating the surface collar mesh.
        This will be handled by pyHyp when generating the volume mesh.

#. Link the upper and lower surface blocking with the leading and trailing edges to get a smooth transition.
#. Split the edges of the fuselage blocks to improve quality.
   Ideally, the outer edges of the fuselage blocks (away from the intersection) will be smooth.
   The angle of the fuselage blocks coming out of the trailing edge is also important for quality.

    .. note::

        It is challenging to get good surface quality where the trailing edge intersects with fuselage.
        Aim for a determinant quality of at least 0.3.

.. important::
    High surface cell quality does not guarantee high volume cell quality.
    This is true in general but especially so for collar meshes.
    In fact, you may find that lower surface quality results in higher volume quality.
    This is because the quality of the volume cells at the intersection depends more on the compatibility between the surface cells on either side of the intersection than the quality of individual surface cells.
    In Pointwise, this can be visualized using the Area Ratio.
