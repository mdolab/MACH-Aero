.. _overset_surface_mesh:

########################
Surface mesh with Pointwise
########################

Now that we have a geometry, we can start meshing it. We are using Pointwise to generate the surface mesh. 
Once this is done, we hyperbolically extrude it into a 3D mesh on the next tutorial page. 

Meshing strategy
================
Before we start meshing, we have to know how many meshes we create and where they overlap. For this tutorial,
3 different meshes are proposed: `near_wing`, `near_tip` and `far`. The following picture should give an overview:

.. figure:: images/overset_m6_mesh_fields.png
    :width: 400
    :align: center 

    The three overset meshes.

Now we should estimate the cell count of the mesh. For the purpose of a grid convergence study (GCS) and debugging
it makes sense to have differently refined meshes. To limit the amount of work, we will create the finest mesh and
coarsen it multiple times. 

Usually, the finest mesh is called L0 (level 0) and should have approx 60M cells for this geometry. If every 2 cells 
are combined in each direction, we get a coarser mesh called L1. This usually goes to L2 for production and L3 for 
debugging purposes. Additionally, there could be an intermediate level starting at L0.5. It requires a different 
surface mesh that is sqrt(2) coarser than L0. In this tutorial, we will start at L1 (~8M cells) and end at L3 
(~0.125M cells).

Creating the `near_wing` surface mesh
=====================================