.. _overset_overview:

*******************************************************
Aerodynamic Analysis with Overset Meshes
*******************************************************

In this part of the tutorial we will mainly generate an overset mesh for ADflow.
Here is a list of commonly used steps to create an overset mesh with the usual workflow in the MDO Lab:

#. Create the geometry using pyGeo, if necessary.
#. Generate surface meshes for the main components in ICEM.
#. Extrude surface meshes into volume meshes using pyHyp.
#. Generate a background mesh using cgnsUtilities.
#. Merge blocks in a single file using cgnsUtilities.
#. Check connectivities using ADflow.

We will take a slightly different approach in this tutorial by using `OpenVSP <http://openvsp.org/>`_ to create the geometry and `Pointwise <http://www.pointwise.com>`_ to generate the surface meshes.
The :ref:`Aerodynamic Analysis <aero_overview>` tutorial covers how to use pyGeo and ICEM.

.. OpenVSP does not only provide the geometry, it can also be hooked up with pygeo. This means, the mesh can be warped based on OpenVSP variables thus allowing optimization without the hassle of generating an FFD control box. This capability will also be showed.

We will do this process on the `ONERA M6 Wing <https://www.grc.nasa.gov/WWW/wind/valid/m6wing/m6wing.html>`_, which is a common example to validate flow solvers in the transonic regime.
Note that an overset mesh might not be needed for a simple geometry like this; however, we will use this geometry as an example to demonstrate the overset mesh surface overlap.

Here are a few of the items we will cover in the following pages:

* Some theory on overset meshes
* General tips and troubleshooting for overset meshes
* Create a wing geometry using OpenVSP
* Surface mesh generation with Pointwise
* Volume mesh extrusion with pyHyp
* ADflow analysis for overset meshes

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   overset_theory
   overset_tips
   overset_vsp
   overset_surface_mesh
   overset_volume_mesh
   overset_analysis


About this tutorial
===================
This tutorial was written by David Anderegg and Anil Yildirim.
David Anderegg is employed by `ZHAW <https://www.zhaw.ch/en/university/>`_ in Switzerland at the time this tutorial was published.
Most of the 'Overset Theory' and 'Tips and Troubleshooting' sections is based on material from Ney Secco.


References
==========

.. bibliography:: overset.bib
   :style: unsrt
   :labelprefix: O
