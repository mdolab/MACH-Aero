.. _aso:

MACH-Aero
==============

This page provides an overview of the aerodynamic shape optimization capability within MACH (framework for MDO of aircraft configurations with high fidelity).

MACH-Aero consists of six major modules:

- Pre-processing (`pyHyp <https://mdolab-pyhyp.readthedocs-hosted.com>`_, `ANSYS ICEM-CFD <https://ansys.com>`_)

- Geometry parameterization (`pyGeo <https://mdolab-pygeo.readthedocs-hosted.com>`_)

- Volume mesh deformation (`IDWarp <https://mdolab-idwarp.readthedocs-hosted.com>`_)

- Flow simulation (`ADflow <https://mdolab-adflow.readthedocs-hosted.com>`_, `DAFoam <https://dafoam.rtfd.io>`_)

- Adjoint computation (`ADflow <https://mdolab-adflow.readthedocs-hosted.com>`_, `DAFoam <https://dafoam.rtfd.io>`_)

- Optimization (`pyOptSparse <https://mdolab-pyoptsparse.readthedocs-hosted.com>`_)

See the following papers for technical background of the above modules. **If you use these modules for publications, please cite the corresponding papers**.

- Ruben E. Perez, Peter W. Jansen, Joaquim R.R.A. Martins, pyOpt: A Python-based object-oriented framework for nonlinear constrained optimization, Structural and Multidisciplinary Optimization 45, 101–118, 2012. https://doi.org/10.1007/s00158-011-0666-3 (**pyOptSparse**)

- Gaetan K.W. Kenway, Graeme J. Kennedy, Joaquim R.R.A. Martins, A CAD-free approach to high-fidelity aerostructural optimization, Proceedings of the 13th AIAA/ISSMO Multidisciplinary Analysis Optimization Conference, Fort Worth, TX, 2010. https://doi.org/10.2514/6.2010-9231 (**pyGeo**)

- Charles A. Mader, Gaetan K.W. Kenway, Anil Yildirim, Joaquim R.R.A. Martins, ADflow: An Open-Source Computational Fluid Dynamics Solver for Aerodynamic and Multidisciplinary Optimization, Journal of Aerospace Information Systems, 2020. https://doi.org/10.2514/1.I010796 (**ADflow**)

- Gaetan K.W. Kenway, Charles A. Mader, Ping He, Joaquim R.R.A. Martins, Effective adjoint approaches for computational fluid dynamics, Progress in Aerospace Sciences, 2019. https://doi.org/10.1016/j.paerosci.2019.05.002 (**ADflow**)

- Anil Yildirim, Gaetan K.W. Kenway, Charles A. Mader, Joaquim R.R.A. Martins, A Jacobian-free approximate Newton–Krylov startup strategy for RANS simulations, Journal of Computational Physics, 2019. https://doi.org/10.1016/j.jcp.2019.06.018 (**ADflow**)

- Ping He, Charles A. Mader, Joaquim R.R.A. Martins, Kevin J. Maki, An aerodynamic design optimization framework using a discrete adjoint approach with OpenFOAM, Computers \& Fluids 168, 285-303, 2018. https://doi.org/10.1016/j.compfluid.2018.04.012 (**DAFoam**)

.. image:: images/AeroOpt.png

Generally, MACH-Aero starts with a baseline design and uses the gradient to find the most promising direction in the design space for improvement.
This process is repeated until the optimality and feasibility conditions are satisfied.
More specifically, the process is as follows, using the above figure as a reference.
Here we use the extended design structure matrix (XDSM) representation developed by Lambe and Martins (2012).
The diagonal nodes represent the modules and the off-diagonal nodes represent the data.
The black lines represent the process flow for the adjoint solver, whereas the thick gray lines represent the data flow.
The number in each node represents the execution order:

- First, we generate a volume mesh for the baseline geometry (pre-processing in process 1). Several mesh generation tools are available including `pyHyp <https://mdolab-pyhyp.readthedocs-hosted.com>`_ and ICEM. Refer to `Surface Meshing <https://mdolab-mach-aero-tutorial.readthedocs-hosted.com/en/latest/aero_icem.html>`_, `Volume Meshing <https://mdolab-mach-aero-tutorial.readthedocs-hosted.com/en/latest/aero_pyhyp.html>`_, and `Mesh Manipulation <https://mdolab-mach-aero-tutorial.readthedocs-hosted.com/en/latest/aero_cgnsutils.html>`_ for more details. The generated mesh will be used later in process 4. In the pre-processing step, we also generate free-form deformation (FFD) points (process 3) that will be used later to morph the design surface. Refer to `Geometric Parameterization <https://mdolab-mach-aero-tutorial.readthedocs-hosted.com/en/latest/opt_ffd.html>`_.

- Then, we give a set of baseline design variables to the optimizer (process 2). We usually use SNOPT as the optimizer, which uses the SQP algorithm. We use `pyOptSparse <https://mdolab-pyoptsparse.readthedocs-hosted.com>`_ to facilitate the optimization problem setup. The optimizer will update the design variables and give them to the geometry parameterization module (`pyGeo <https://mdolab-pygeo.readthedocs-hosted.com>`_; process 3). pyGeo receives the updated design variables and the FFD points generated in the pre-processing step, performs the deformation for the design surface, and outputs the deformed design surface to the mesh deformation module (`IDWarp <https://mdolab-idwarp.readthedocs-hosted.com>`_) in process 4. pyGeo also computes the values of geometric constraints and their derivatives with respect to the design variables (process 7).

- Next, `IDWarp <https://mdolab-idwarp.readthedocs-hosted.com>`_ deforms the volume mesh based on the updated design surface and outputs the updated volume mesh to the flow simulation module in process 5.

- The flow simulation module receives the updated volume mesh and uses high-fidelity CFD tools (i.e., `ADflow <https://mdolab-adflow.readthedocs-hosted.com>`_ or `DAFoam <https://dafoam.rtfd.io>`_) to compute the state variables (process 6) or physical fields (pressure, density, velocity, etc.). The flow simulation module also computes the objective and constraint functions (e.g., drag and lift; see process 7) and outputs the state variables to the adjoint computation module.

- Then, the adjoint computation module (process 6) computes the total derivatives of the objective and constraint functions with respect to the design variables (process 7) and gives them back to the optimizer in process 7. The benefit of using the adjoint method to compute derivatives is that its computational cost is independent of the number of design variables, which makes it attractive for handling large-scale, complex design problems such as aircraft design. There are two available adjoint solvers: `ADflow <https://mdolab-adflow.readthedocs-hosted.com>`_, `DAFoam <https://dafoam.rtfd.io>`_.

- Finally, the optimizer receives the values and derivatives of the objective and constraint functions in process 7, performs the SQP computation, and outputs a set of updated design variables to pyGeo.

The above process is repeated until the optimization converges.
Refer to the `MACH-Aero tutorials <https://mdolab-mach-aero-tutorial.readthedocs-hosted.com/>`_ for tutorials.
