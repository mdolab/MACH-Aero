.. _aero_overview:

####################
Aerodynamic Analysis
####################
High-fidelity aerodynamic analysis in the MDOlab is done using `ADflow <https://github.com/mdolab/adflow>`_.
ADflow is a finite-volume CFD solver for cell-centered multiblock and overset meshes.
ADflow solves the compressible Euler, laminar Navier--Stokes, and RANS equations with a second-order accurate spatial discretization.
More information on ADflow can be found somewhere (needs link).

In order to analyze a geometry with ADflow, we need to take the following steps:

- **Obtain a CAD representation of the geometry**
    In practice, we want an IGES file that contains the geometry description.
    This can be done with any commercial CAD package, but it can also be done by lofting airfoil sections using pyGeo.

- **Generate a valid multiblock or overset mesh**
    ADflow uses the CGNS mesh format. In practice, we create a surface mesh using ICEM and then extrude a volume mesh using pyHyp. However, the volume mesh could be created in ICEM or any other meshing software. Component volume meshes can be combined using cgnsUtilities.

- **Analyze the flow with ADflow**
    Since ADflow is a script-based software, it is important to understand the elements of an ADflow runscript.
    Additionally, there are many settings that can be adjusted to make ADflow perform better for a given case.

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   aero_pygeo
   aero_icem
   aero_pyhyp
   aero_cgnsutils
   aero_adflow
   aero_adflow_polar
   aero_gridRefinementStudy

