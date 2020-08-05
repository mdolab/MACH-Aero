.. _airfoilopt_overview:

####################
Airfoil Optimization
####################
In this part of the tutorial, we will go through an example of an airfoil optimization. The process is similar to that of the previous sections, but less complicated.

Here are a few of the items we will cover in the following pages:

    - Generate an airfoil mesh to be used for optimization

    - Parametrize the 2D airfoil using the Free-form Deformation method

    - Run a single-point aerodynamic shape optimization

    - Run a multi-point aerodynamic shape optimization

Table of Contents
=================

.. toctree::
   :maxdepth: 1

   airfoilopt_mesh
   airfoilopt_ffd
   airfoilopt_singlepoint
   airfoilopt_multipoint

Directory Structure
===================
::

    opt
    |-- meshing
    |   |-- genMesh.py
    |-- ffd
    |   |-- genFFD.py
    |-- single point opt
    |   |-- airfoil_opt.py
    |-- multipoint opt
    |   |-- airfoil_multiopt.py
