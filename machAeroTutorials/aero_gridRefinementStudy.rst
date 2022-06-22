.. Standard method of doing a grid refinement study.


.. _gridRefinementStudy:

Grid Refinement Study
==========================

Theory
------
Computational physics models generally use discretized physical domains (grids) to transform physical laws into systems of equations that can be solved by numerical methods.
The discretization of a physical domain introduces discretization error, which can be reduced in two ways:

- h-refinement: Increasing the resolution of the grid.
- p-refinement: Increasing the order of the numerical approximation at each cell.

In a grid refinement study, we demonstrate that iterative h-refinement converges to the exact solution.
For a given grid/mesh, the grid spacing is

.. math::
    h = N^{-1/d}

where :math:`N` is the number of cells and :math:`d` is the dimension of the domain.
For two grids, the grid refinement ratio is

.. math::
    r = \frac{h_{coarse}}{h_{fine}}

Generally, we use a grid refinement ratio of 2.
The convention is to name the grids with an `L` (for level) followed by an integer beginning at 0 for the finest grid (i.e. L0 for the finest, L1 for the next, etc).

If the grids are sufficiently fine, the error is roughly proportional to :math:`h^p`, where :math:`p` is the order of the solution method.
Grids that follow this relationship are in what is termed the "region of asymptotic convergence".
Although for a second-order finite volume solver, the theoretical order of convergence is :math:`p=2`, the achieved rate of convergence (:math:`\hat{p}`) may vary.
The achieved rate of convergence for a given h-refinement study can be computed as

.. math::
    \hat{p} = ln\left(\frac{f_{L2}-f_{L1}}{f_{L1}-f_{L0}}\right) / ln(r)

using the finest three grids.
When plotting the results of the grid convergence study, we generally plot the results of the grid convergence using :math:`h^p` on the x-axis.


The Richardson extrapolation is an estimation of the solution for a grid with a grid spacing on the order of zero.
It is computed using the solutions from the L0 and L1 grids with the equation

.. math::
    f_{h=0} = f_{L0} + \frac{f_{L0}-f_{L1}}{r^{\hat{p}} - 1}

Grid Refinement Study on Airfoils
======================================

There are two methods for performing grid refinement: 
1) coarsening the volume mesh and 
2) coarsening the surface mesh and extruding the family of surface meshes
We discuss the pros and cons of each method and underlying theory;
it is up to the user to choose the method.

.. _option-1:

Option 1: Coarsening volume meshes
----------------------------------

1. Generate fine grid (L0) with :math:`N=(2^n) (m) + 1` nodes along each edge.
2. Coarsen the L0 grid :math:`n-1` times using ``cgns_utils coarsen``.
3. Use ``solveCL`` or ``solveTrimCL`` in ADflow to obtain :math:`C_D` for a given :math:`C_L`.
4. Compute the Richardson extrapolation using the L0 and L1 grids.
5. Plot :math:`h^p` vs :math:`C_D`. For ADflow, use :math:`p=2` to indicate a second-order method.

This method is the original mesh refinement Richardson Extrapolation theory relies on since there is a uniform coarsening between meshes.
If the plotted dots are in a straight line, your mesh is in the asymptotic regime.
You want the Richardson Extrapolation to lie on the line or lead to a slight concave up shape, which indicates convergence to the exact numerical solution.
The slope of the line is the coefficient of the leading truncation error term.

An example of grid convergence plot for a family of RAE 2822 Airfoil meshes is illustrated below:

.. figure:: images/RAE2822_gridconvergence.png
    :scale: 60
    :align: center
    :alt: RAE 2822 Grid Convergence
    :figclass: align-center

    Figure 1: Grid convergence plot for RAE 2822 Transonic Airfoil.

Pros:
    - The grid is coarsened uniformly, giving the most mathematically rigorous convergence study, which is important for justifying solutions in your scholarly articles.

Cons:
    - To generate enough points to make a line (at least three), the finest mesh (L0) has to be extremely fine for 3D meshes to have a coarse mesh that is still in the asymptotic regime since for the ``n``th level, it needs to have :math:`(2^3)^n` fewer cells assuming a refinement ratio of 2.
    - Growth ratio is changing, so be wary of the off-wall cell resolution and boundary layer accuracy.

Option 2: Coarsening surface meshes and extruding a family of volume meshes
---------------------------------------------------------------------------

Instead of using the ``cgns_utils coarsen`` feature, we can easily make the finer or coarsen meshes with the help of ``prefoil`` package.
The main reason behind this idea is to generate the meshes without changing the ``growth rate`` of the off wall layers.
If you use ``cgns_utils coarsen`` feature (i.e. :ref:`option-1`), you will be able to increase the first off-wall spacing ``s0`` uniformly; 
however, the grow ratio is going to change and the off-wall layers will have too much distance between each other.

In order to avoid this, we can use the ``prefoil`` packages easily and still be able to coarsen or refine the meshes. 
The example code is given below. You can either upload a ``.dat`` file or create the NACA 4 digit airfoils. 
Then, you can manipulate the meshing parameters and get mesh grids with different levels.

.. code-block:: python

    from pyhyp import pyHyp
    from prefoil.preFoil import Airfoil, readCoordFile,generateNACA
    from prefoil import sampling


    # L2 layer mesh grid initilization
    # We will refine the mesh from this starting grid
    nTE_cells_L2 = 5
    nSurfPts_L2 = 200
    nLayers_L2 = 80
    s0_L2 = 4e-6

    # Increasing the mesh sizes 
    refinement=[1,2,4]
    level =['L2','L1','L0']

    for i in range(len(refinement)):

        # number of points on the airfoil surface
        nSurfPts = refinement[i]*nSurfPts_L2

        # number of points on the TE.
        nTEPts = refinement[i]*nTE_cells_L2 


        # number of extrusion layers
        nExtPts = refinement[i]*nLayers_L2 

        # first off wall spacing
        s0 = s0_L2/ refinement[i]

        #### We can either import our desired airfoil .dat file and continue the meshing proces ####
        #### Or we can generate the NACA airfoils if our baseline is a 4 series NACA airfoil    ####

        # Read the Coordinate file
        # filename = "n0012_old.dat"
        # coords = readCoordFile(filename, headerlines=1)

        # We can also  generate NACA 4 series airfoils
        code='0012'
        nPts=150
        coords=generateNACA(code, nPts, spacingFunc=sampling.polynomial, func_args={"order": 8})
        # print('yes',coords)
        airfoil = coords

        coords = airfoil.getSampledPts(
        nSurfPts,
        spacingFunc=sampling.polynomial, func_args={"order": 8},
 
        nTEPts=nTEPts,
        )
        # print(coords)
        # Write surface mesh
        airfoil.writeCoords("./input/naca0012_%s" % level[i], file_format="plot3d")



        options = {
            # ---------------------------
            #        Input Parameters
            # ---------------------------
            "inputFile": "./input/naca0012_%s.xyz" % level[i],
            "unattachedEdgesAreSymmetry": False,
            "outerFaceBC": "farfield",
            "autoConnect": True,
            "BC": {1: {"jLow": "zSymm", "jHigh": "zSymm"}},
            "families": "wall",
            # ---------------------------m
            #        Grid Parameters
            # ---------------------------
            "N": nExtPts,
            "s0": s0,
            "marchDist": 100.0,

        }
        hyp = pyHyp(options=options)
        hyp.run()
        hyp.writeCGNS("./input/naca0012_%s.cgns" % level[i])



As an example, the Tecplot of both cases are shown. As we can see, when we coarsen through ``cgns_utils``, the distance between each layers become higher and the growth ratio is not the same as ``prefoil`` mesh.

.. figure:: images/meshexample.png
    :scale: 40
    :align: center
    :alt: Mesh comparison
    :figclass: align-center

    Figure 2: Mesh comparison.

.. TODO: add mesh refinement plot using this method that's similar to the RAE one

Pros:
    - It is more practical for 3D meshes since the refinement ratio is not as aggressive as ``Option 1``. This places the points on the refinement plot closer to each other  on the :math:`x`-axis so it is more likely that your coarsest volume mesh is in the asymptotic regime, which you can then use for coarse optimizations.
    - It is easier to generate the 0.5 level family of meshes (e.g., L0.5, L1.5, L2.5) using the ``scaleBlkFile`` procedure in the postprocessing repository to scale the surface meshes by a factor of :math:`1/\sqrt{2}`.

Cons:
    - It is harder to be mathematically rigorous (and therefore justifiable in a scholarly article) using this method because all options from the surface mesh extrusion have to be scaled accordingly and even then, there may be variations in volume cell scaling from the procedure.
    - Your mesh refinement results might not follow a perfectly straight line compared to ``Option 1`` even if they are in the asymptotic regime since it is not a uniform refinement (but it should be close to linear)

External Links
--------------

- https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html
- https://turbmodels.larc.nasa.gov/uncertainty_summary.pdf
