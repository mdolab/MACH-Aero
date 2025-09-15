.. _opt_overview:

########################
Aerodynamic Optimization
########################
In this part of the tutorial, we will demonstrate how to optimize the design of an aircraft with gradient-based optimization algorithms.
One of the singular attributes of the AeroOpt framework is that it was specifically designed for the purpose of conducting gradient-based optimization studies.
(For a simple demonstration of why we use gradient-based optimization, check out `this optimization game <http://mdolab.engin.umich.edu/assets/optimizationGame/>`_.)
Each module was developed from the beginning with gradient-based optimization in mind to ensure that accurate gradients could be obtained efficiently.
The naive approach to gradient-based optimization is generally to use finite difference approximations for derivatives of the functions of interest with respect to the design variables.
There are many problems with this approach, including prohibitive computational expense and rampant inaccuracy, so as a rule, we don't touch finite difference with a ten foot pole.
Instead, we use a combination of analytic gradients, automatic differentiation, and the complex-step method to compute accurate gradients for our optimizations.
We have spent a great deal of effort to make optimization a fairly straightforward and seamless process for the end user, so we hope you enjoy learning to use our tools!

Overview of framework
---------------------
An optimizer is used via `pyOptSparse` to select the design variables for a candidate design.
`pyGeo` warps the surface mesh according to the geometric design variables.
`idwarp` propagates the deformation of the surface mesh into the volume mesh.
ADflow then solves for the performance of the design using that volume mesh. The variables used to define the aerodynamic analysis can also be modified by the optimizer (e.g. Mach number, AoA, etc.).
Based on the outputs of the aerodynamic analysis and the setup of the optimization problem, the optimizer will continue to generate a new candidate designs until it converges.

Here are a few of the items we will cover in the following pages:

    - Set up an optimization script using pyOptSparse
    - Parametrize a 3D geometry using the Free-form Deformation method
    - Run single-point and multi-point aerodynamic shape optimizations

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   opt_pyopt
   opt_ffd
   opt_aero
