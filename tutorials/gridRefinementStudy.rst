.. Standard method of doing a grid refinement study.


.. _gridRefinementStudy:

Grid Refinement Study
=====================

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

Grid refinement study with ADflow
---------------------------------

1. Generate fine grid (L0) with :math:`N=2^n m + 1` nodes along each edge.
2. Coarsen the L0 grid :math:`n-1` times using :code:`cgns_utils coarsen`.
3. Use :code:`solveCL` or :code:`solveTrimCL` in ADflow to obtain :math:`C_D` for a given :math:`C_L`.
4. Compute the Richardson extrapolation using the L0 and L1 grids.
5. Plot :math:`h^p` vs :math:`C_D`. For ADflow, use :math:`p=2` to indicate a second-order method.

Examples
--------
See examples of grid convergence figures at the following links.

- `RAE 2822 Airfoil <https://github.com/mdolab/RAE2822/tree/master/grid_convergence>`_

External Links
--------------

- https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html
- https://turbmodels.larc.nasa.gov/uncertainty_summary.pdf