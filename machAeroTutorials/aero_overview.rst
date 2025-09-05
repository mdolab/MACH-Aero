.. _aero_overview:

####################
Wing Aerodynamic Analysis
####################
Once you have mastered analysing and optimizing airfoils with MACH-Aero, you can try performing these operations on finite wings.
We will start with the aerodynamic analysis of a Boeing 717 wing.

.. note:: This process builds on the skills learned in the previous tutorials but is overall more complicated.
    Make sure you've completed the airfoil tutorials first before attempting this one.

In order to analyze a wing geometry with ADflow, we need to take the following steps:

**Obtain a CAD representation of the geometry**
    With complex 3D geometries like wings we can't just easily obtain our geometry as a set of points like we did for the airfoil.
    As a result, we will need to define our wing's geometry using CAD.
    In practice, we want an IGES file that contains the geometry description.
    This can be done with any commercial CAD package, but it can also be done by lofting airfoil sections using the geometry surfacing engine built into *pygeo*, called **pyGeo**.

**Generate a family of valid multiblock meshes**
    Like the airfoil, the wing will also need a valid structured volume mesh.
    However, since our geometry is composed of surfaces generated in CAD and not a set of points we will need to do this in two steps.
    We create a surface mesh using the Pointwise or ICEM meshing utilities and then extrude the volume mesh using pyHyp.
    However, the volume mesh could also be created in Pointwise, ICEM, or any other meshing software.
    Additionally, we won't just generate one mesh in this step.
    Instead we generate a family of meshes with varying degrees of grid refinement.

**Analyze the flow with ADflow**
    Since ADflow is a script-based software, it is important to understand the elements of an ADflow runscript.
    Additionally, there are many settings that can be adjusted to make ADflow perform better for a given case.

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   aero_pygeo
   aero_pointwise
   aero_icem
   aero_pyhyp
   aero_adflow
