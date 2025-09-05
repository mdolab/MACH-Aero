.. _airfoilopt_overview:

####################
Airfoil Optimization
####################
In this tutorial we will introduce the aerodynamic shape optimization capabilities in MACH-Aero by optimizing the NACA 0012 airfoil examined in the previous tutorial.
This tutorial will heavily build on the previous one and it is highly recommended that you go through it first if you have not.
In fact, we will be reusing the same initial processed geometry and mesh that we created in the previous tutorial in this one.
This tutorial will be a high-fidelity RANS optimization of a NACA 0012 so we will be using ADflow again.
However, this time we will introducing a few more tools including pygeo, IDwarp, and pyOptSparse.

One of the singular attributes of the MACH-Aero framework is that it was specifically designed for the purpose of conducting gradient-based optimization studies.
(For a simple demonstration of why we use gradient-based optimization, check out `this optimization game <http://mdolab.engin.umich.edu/assets/optimizationGame/>`_.)
Each module was developed from the beginning with gradient-based optimization in mind to ensure that accurate gradients could be obtained efficiently.
The naive approach to gradient-based optimization is generally to use finite difference approximations for derivatives of the functions of interest with respect to the design variables.
There are many problems with this approach, including prohibitive computational expense and rampant inaccuracy, so as a rule, we don't touch finite difference with a ten foot pole.
Instead, we use a combination of analytic gradients, automatic differentiation, and the complex-step method to compute accurate gradients for our optimizations.
We have spent a great deal of effort to make optimization a fairly straightforward and seamless process for the end user, so we hope you enjoy learning to use our tools!

In order to optimize an airfoil geometry with MACH-Aero, we need to take the following steps:

**Learn how to use pyOptSparse to solve an optimziation problem with a gradient-based algorithm**
    The primary optimiation package/wrapper of choice for MACH-Aero is pyOptSparse.
    However, before you start optimizing airfoils with it you should understand how to use it to solve basic optimization problems.
    This part of the tutorial will explain how to use pyOptSparse to optimize the Rosenbrock functions.
    For a detailed theoretical background in numerical optimization please see our book `here <https://flowlab.groups.et.byu.net/mdobook.pdf>`_.

**Parametrize the 2D airfoil using the Free-form Deformation method**
    To conduct airfoil optimization, the optimizer has to be able to control the airfoil's geometry.
    We use the Free-form Defomation method to do this which is provided by the pygeo package.

**Run single and multi-point aerodynamic shape optimzation on the airfoil**
    Here is where we put it all together to optimize our NACA 0012 airfoil for a single flight condition.
    However, that by itself will get us an airfoil that performs really well at a certain flight condition and really bad anytime else.
    As a result, we also cover multi-point optimization to make sure our airfoil performs optimally accross many flight conditions.

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   airfoilopt_pyopt
   airfoilopt_ffd
   airfoilopt_singlepoint
   airfoilopt_multipoint
