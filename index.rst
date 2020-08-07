.. MDOLAB Code documentation

MACH-Aero Framework
===================
MACH-Aero is a framework for performing gradient-based aerodynamic shape optimization.
It consists of the following core modules:

- `baseClasses <https://mdolab-baseclasses.readthedocs-hosted.com>`_ defines Python classes used by the other packages
- `pySpline <https://mdolab-pyspline.readthedocs-hosted.com>`_ is a B-spline implementation used by the other packages
- `pyGeo <https://mdolab-pygeo.readthedocs-hosted.com>`_ is a module for geometry manipulation and constraint formulation
- `IDWarp <https://mdolab-idwarp.readthedocs-hosted.com>`_ performs mesh warping using an inverse distance method
- `ADflow <https://mdolab-adflow.readthedocs-hosted.com>`_ is a 2nd-order finite volume CFD solver with an efficient adjoint implementation
- `pyOptSparse <https://mdolab-pyoptsparse.readthedocs-hosted.com>`_ is an optimization framework which provides a unified interface to several popular optimizers

And the following optional modules:

- `pyHyp <https://mdolab-pyhyp.readthedocs-hosted.com>`_ is a hyperbolic mesh generation tool used as a preprocessing step
- `multiPoint <https://mdolab-multipoint.readthedocs-hosted.com>`_ facilitates distributed multipoint optimization and handles the parallel communication using MPI
- `DAFoam <https://dafoam.github.io/>`_ provides efficient adjoint implementations for OpenFOAM to be used for CFD instead of ADflow

More detail for the framework can be found in :ref:`mach-aero`.
If you use any of our codes, please :ref:`cite us <cite-us>`.

.. toctree::
   :caption: Overview
   :maxdepth: 1
   :hidden:

   machFramework/MACH-Aero.rst
   machFramework/citeUs.rst

.. toctree::
   :caption: Installation
   :maxdepth: 1

   installInstructions/installFromScratch
   installInstructions/install3rdPartyPackages

.. toctree::
   :caption: Tutorials
   :maxdepth: 2

   machAeroTutorials/index