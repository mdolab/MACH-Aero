.. _airfoilanalysis_overview:

####################
Airfoil Analysis
####################
This tutorial explains how to analyze an airfoil using high-fidelity aerodynamic analysis.
High-fidelity aerodynamic analysis in MACH is done using :doc:`ADflow <adflow:index>`.
ADflow is a finite-volume CFD solver for cell-centered multi-block and overset meshes.
ADflow solves the compressible Euler, laminar Navier--Stokes, and RANS equations with a second-order accurate spatial discretization.
More information on ADflow can be found `here <https://github.com/mdolab/adflow>`_.

To start, we will go through an example of how to perform an aerodynamic analysis on a NACA 0012 airfoil with ADflow.

In order to analyze an airfoil geometry with ADflow, we need to take the following steps:

**Obtain a set of airfoil coordinates and preprocess them for meshing**
    The MACH-Aero framework provides the necessary tools to process and manipulate airfoil coordinates. 
    However, the coordinates themselves will need to be sourced, provided, or generated.

**Generate a valid structured mesh**
    ADflow uses the CGNS mesh format. 
    For airfoils, we can simply extrude airfoil coodinates using **pyHyp** to obtain a structured volume mesh.

**Analyze the flow with ADflow**
    Since ADflow is a script-based software, it is important to understand the elements of an ADflow runscript.
    Additionally, there are many settings that can be adjusted to make ADflow perform better for a given case.

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   airfoilanalysis_prefoil
   airfoilanalysis_mesh
   airfoilanalysis_adflow
