.. _aero_overview:

####################
Wing Aerodynamic Analysis
####################
Once you have mastered analysing and optimizing airfoils with MACH-Aero, you can try performing these operations on finite wings.
We will start with the aerodynamic analysis of a Boeing 717 wing.

.. note:: This process builds on the skills learned in the previous tutorials but is overall more complicated to make sure you've completed the airfoil tutorials first before attempting this one.

In order to analyze a wing geometry with ADflow, we need to take the following steps:

- **Obtain a CAD representation of the geometry**
    In practice, we want an IGES file that contains the geometry description.
    This can be done with any commercial CAD package, but it can also be done by lofting airfoil sections using the geometry surfacing engine built into *pygeo*, called **pyGeo**.

- **Generate a valid multiblock or overset mesh**
    ADflow uses the CGNS mesh format. In practice, we create a surface mesh using Pointwise or ICEM and then extrude a volume mesh using pyHyp. 
    However, the volume mesh could also be created in Pointwise, ICEM, or any other meshing software. 
    Component volume meshes can be combined using cgnsUtilities.

- **Analyze the flow with ADflow**
    Since ADflow is a script-based software, it is important to understand the elements of an ADflow runscript.
    Additionally, there are many settings that can be adjusted to make ADflow perform better for a given case.

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   aero_pygeo
   aero_pointwise
   aero_icem
   aero_pyhyp
   aero_cgnsutils
   aero_adflow
   aero_gridRefinementStudy
