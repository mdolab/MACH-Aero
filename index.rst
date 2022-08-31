.. MDOLAB Code documentation

MACH-Aero Framework
===================
MACH-Aero is a framework for performing gradient-based aerodynamic shape optimization.
It consists of the following core modules:

- :doc:`baseClasses <baseclasses:index>` defines Python classes used by the other packages
- :doc:`pySpline <pyspline:index>` is a B-spline implementation used by the other packages
- :doc:`pyGeo <pygeo:index>` is a module for geometry manipulation and constraint formulation
- :doc:`IDWarp <idwarp:index>` performs mesh warping using an inverse distance method
- :doc:`ADflow <adflow:index>` is a 2nd-order finite volume CFD solver with an efficient adjoint implementation
- :doc:`pyOptSparse <pyoptsparse:index>` is an optimization framework which provides a unified interface to several popular optimizers

And the following optional modules:

- :doc:`pyHyp <pyhyp:index>` is a hyperbolic mesh generation tool used as a preprocessing step
- :doc:`multiPoint <multipoint:index>` facilitates distributed multipoint optimization and handles the parallel communication using MPI
- `cgnsUtilities <https://github.com/mdolab/cgnsutilities>`_ is a command-line tool that allows carrying out several simple mesh manipulation operations on CGNS grids
- `DAFoam <https://dafoam.github.io/>`_ provides efficient adjoint implementations for OpenFOAM to be used for CFD instead of ADflow

More detail for the framework can be found in :ref:`mach-aero`.
If you use any of our codes, please :ref:`cite us <cite-us>`.

.. toctree::
   :caption: Overview
   :maxdepth: 1
   :hidden:

   machFramework/MACH-Aero.rst
   machFramework/citeUs.rst
   machFramework/contribute.rst

.. toctree::
   :caption: Installation
   :maxdepth: 1

   installInstructions/dockerInstructions
   installInstructions/installFromScratch
   installInstructions/install3rdPartyPackages

.. toctree::
   :caption: Tutorials
   :maxdepth: 2

   machAeroTutorials/intro
   machAeroTutorials/aero_overview
   machAeroTutorials/opt_overview
   machAeroTutorials/airfoilopt_overview
   machAeroTutorials/overset_overview
   machAeroTutorials/faq