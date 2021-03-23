.. _overset_overview:

*******************************************************
Overset Mesh
*******************************************************

In this part of the tutorial we will mainly generate an overset mesh for ADflow.
We will use `OpenVSP <http://openvsp.org/>`_ to create the geometry, generate a surface mesh with `Pointwise <http://www.pointwise.com>`_ (requires a license), and extrude the volume mesh with `pyHyp <https://github.com/mdolab/pyhyp>`_.

.. OpenVSP does not only provide the geometry, it can also be hooked up with pygeo. This means, the mesh can be warped based on OpenVSP variables thus allowing optimization without the hassle of generating an FFD control box. This capability will also be showed.

We will do this process on the `ONERA M6 Wing <https://www.grc.nasa.gov/WWW/wind/valid/m6wing/m6wing.html>`_.
It is a common example to validate flow solvers in the transonic regime.
Note that an overset mesh might not be needed for a simple geometry like this; however, we will use this geometry as an example to demonstrate the overset mesh surface overlap.

Here are a few of the items we will cover in the following pages:

* Some theory on overset meshes
* Create a wing geometry using OpenVSP
* Surface mesh generation with Pointwise
* Volume mesh extrusion with pyHyp
* ADflow analysis for overset meshes

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   overset_theory
   overset_vsp
   overset_surface_mesh
   overset_volume_mesh
   overset_analysis


About this tutorial
===================
This tutorial was written by David Anderegg and Anil Yildirim.
David Anderegg is employed by `ZHAW <https://www.zhaw.ch/en/university/>`_ in Switzerland at the time this tutorial was published.
Most of the material in the overset theory section is based on the materials from Ney Secco.


References
==========

.. bibliography:: overset.bib
   :style: unsrt
   :labelprefix: O
