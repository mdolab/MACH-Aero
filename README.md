# MACH-Aero
[![Documentation Status](https://readthedocs.com/projects/mdolab-mach-aero/badge/?version=latest)](https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/?badge=latest)
[![Build Status](https://dev.azure.com/mdolab/Public/_apis/build/status/mdolab.MACH-Aero?repoName=mdolab%2FMACH-Aero&branchName=master)](https://dev.azure.com/mdolab/Public/_build/latest?definitionId=35&repoName=mdolab%2FMACH-Aero&branchName=master)

MACH-Aero is a framework for performing aerodynamic shape optimization.
It contains the following core modules:

| Code repository | Functionality | Documentation | CI Status |
| --------------- | ------------- | ------------- | --------- |
| [`baseClasses`](https://github.com/mdolab/baseclasses) | Shared class definitions | [![Documentation Status](https://readthedocs.com/projects/mdolab-baseclasses/badge/?version=latest)](https://mdolab-baseclasses.readthedocs-hosted.com/?badge=latest) | [![Build Status](https://travis-ci.com/mdolab/baseclasses.svg?branch=master)](https://travis-ci.com/mdolab/baseclasses) |
| [`pySpline`](https://github.com/mdolab/pyspline) | B-spline implementation | [![Documentation Status](https://readthedocs.com/projects/mdolab-pyspline/badge/?version=latest)](https://mdolab-pyspline.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://travis-ci.com/mdolab/pyspline.svg?branch=master)](https://travis-ci.com/mdolab/pyspline) |
| [`pyGeo`](https://github.com/mdolab/pygeo) | Geometry definition | [![Documentation Status](https://readthedocs.com/projects/mdolab-pygeo/badge/?version=latest)](https://mdolab-pygeo.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://travis-ci.com/mdolab/pygeo.svg?branch=pyGeo)](https://travis-ci.com/mdolab/pygeo) |
| [`IDWarp`](https://github.com/mdolab/idwarp) | Volume mesh warping | [![Documentation Status](https://readthedocs.com/projects/mdolab-idwarp/badge/?version=latest)](https://mdolab-idwarp.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://travis-ci.com/mdolab/idwarp.svg?branch=master)](https://travis-ci.com/mdolab/idwarp) |
| [`ADflow`](https://github.com/mdolab/adflow) | CFD and adjoint solver | [![Documentation Status](https://readthedocs.com/projects/mdolab-adflow/badge/?version=latest)](https://mdolab-adflow.readthedocs-hosted.com/?badge=latest) | [![Build Status](https://travis-ci.com/mdolab/adflow.svg?branch=master)](https://travis-ci.com/mdolab/adflow)  |
| [`pyOptSparse`](https://github.com/mdolab/pyoptsparse) | Optimizer wrapper | [![Documentation Status](https://readthedocs.com/projects/mdolab-pyoptsparse/badge/?version=latest)](https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://travis-ci.com/mdolab/pyoptsparse.svg?branch=master)](https://travis-ci.com/mdolab/pyoptsparse) |
| And optional modules: |  |  |  |
| [`pyHyp`](https://github.com/mdolab/pyhyp) | Volume mesh generation | [![Documentation Status](https://readthedocs.com/projects/mdolab-pyhyp/badge/?version=latest)](https://mdolab-pyhyp.readthedocs-hosted.com/en/latest) | [![Build Status](https://dev.azure.com/mdolab/Public/_apis/build/status/mdolab.pyhyp?branchName=master)](https://dev.azure.com/mdolab/Public/_build/latest?definitionId=13&branchName=master) |
| [`multiPoint`](https://github.com/mdolab/multipoint) | Utilities for multipoint optimization | [![Documentation Status](https://readthedocs.com/projects/mdolab-multipoint/badge/?version=latest)](https://mdolab-multipoint.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Public/_apis/build/status/mdolab.multipoint?branchName=master)](https://dev.azure.com/mdolab/Public/_build/latest?definitionId=24&branchName=master) |
| [`DAFoam`](https://github.com/mdolab/dafoam) | Alternate adjoint solver using OpenFOAM | [![Documentation](https://img.shields.io/badge/docs-passing-brightgreen)](https://dafoam.github.io/) | ![Build Status](https://github.com/mdolab/dafoam/workflows/DAFoam/badge.svg?branch=master) |
| [`cgnsUtilities`](https://github.com/mdolab/cgnsutilities) | Utilities for CGNS mesh files |  | [![Build Status](https://dev.azure.com/mdolab/Public/_apis/build/status/mdolab.cgnsutilities?repoName=mdolab%2Fcgnsutilities&branchName=master)](https://dev.azure.com/mdolab/Public/_build/latest?definitionId=16&repoName=mdolab%2Fcgnsutilities&branchName=master) |

## Where is the code?
All the code for MACH-Aero are contained within the individual repositories, which you can go to by clicking on the names in the table above.
To go to the documentation site for each repository, click on the badge in the documentation column of the table above.

## What's in this repo then?
This repository contains the following:
- A description of the overall framework
- Installation instructions which are shared across the various repositories
- Tutorials for using MACH-Aero to perform aerodynamic shape optimization

These documentation can be accessed online at https://mdolab-mach-aero.readthedocs-hosted.com/.
To run the tutorials yourself, you need to follow the installation instructions to install all the modules, then clone this repository to access the tutorial scripts.
To compile the doc locally, first install dependencies via ``pip install -r requirements.txt``, then build locally with ``make html``.
