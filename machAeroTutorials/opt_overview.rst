.. _opt_overview:

########################
Wing Aerodynamic Optimization
########################
After completing the wing analysis tutorial, you'll be ready to start optimizing the wing.
This tutorial will heavily build on the previous one and it is highly recommended that you go through it first if you have not.
In fact, we will be reusing the same initial geometry, surface mesh, and volume mesh that we created in the previous tutorial in this one.
The wing optimization process is very similar to the airfoil optimziation processess except that the FFD parameterization will be a bit more complicated.

In order to optimize a wing geometry with MACH-Aero, we need to take the following steps:

**Parametrize the 3D wing using the Free-form Deformation method**
    To conduct wing optimization, the optimizer has to be able to control the wing's geometry.
    We use the Free-form Defomation method to do this which is provided by the pygeo package.
    In the airfoil example we only used local FFD design variables.
    In this example we will need to cover global FFD design variables to control typical wing parameters like twist, dihedral, and sweep.

**Run the aerodynamic shape optimzation on the wing**
    Here is where we put it all together to optimize our wing for a single flight condition.

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   opt_ffd
   opt_aero
