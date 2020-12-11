.. _overset_overview:

*******************************************************
Overset Mesh
*******************************************************

In this part of the tutorial we will mainly generate an overset mesh for ADFlow. We will use 
`OpenVSP <http://openvsp.org/>`_ to create the geometry, generate a surface mesh with 
`Pointwise <http://www.pointwise.com>`_ (subject to charge) and extrude the volume mesh with pyHyp.

.. OpenVSP does not only provide the geometry, it can also be hooked up with pygeo. This means, the mesh can be warped based on OpenVSP variables thus allowing optimization without the hassle of generating an FFD control box. This capability will also be showed.

We will do this process on the `ONERA M6 Wing <https://www.grc.nasa.gov/WWW/wind/valid/m6wing/m6wing.html>`_. It is 
a common example to validate flow solvers in the transonic regime. Note that an overset mesh might not be needed
for a simple geometry like this.

Here are a few of the items we will cover in the following pages:

* Some theory on overset meshes
* Create a wing geometry using OpenVSP
* Surface mesh generationg with Pointwise
* Volume mesh extrusion with pyGeo
* ADflow analysis for overset meshes



.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   overset_theory
   overset_vsp
   overset_surface_mesh
   overset_volume_mesh
   overset_analysis


References
==========

.. bibliography:: overset.bib
    :style: unsrt