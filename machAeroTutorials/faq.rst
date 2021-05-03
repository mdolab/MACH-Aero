.. _faq:


Frequently Asked Questions
==========================

In this section, we have a list of frequently asked questions and answers.

How do I obtain the cell count in a mesh?
-----------------------------------------

There are several ways to get the cell count information from a mesh file.

The simplest way is to use the ``info`` command in CGNS Utilities, which will print this information to the terminal.

.. prompt:: bash

    cgns_utils info wing_vol.cgns

The output should look like::

    Total Zones: 9
    Total Cells: 193536
    Total Nodes: 217413
    Wall Boundary Cells: 4032
    Wall Boundary Nodes: 4437


Running ADflow with a mesh will also print the number of cells to the terminal.
For example, after printing the full options dictionary, ADflow will print::

    #
    # Grid level: 1, Total number of cells: 193536
    #


Finally, users should note that for overset meshes, the number of "compute" cells will be different than number of total cells.
In both methods above, the code will print the total number of cells present in the CGNS file.
However, with overset grids, a portion of the cells will be "blanked".
During the overset hole cutting, ADflow will print some detailed information about this process.
For example::

    Flood Iteration:           1 Blanked         3357 Interior Cells.
    Flood Iteration:           2 Blanked            0 Interior Cells.
    +--------------------------------+
    | Compute Cells           :      548237
    | Fringe Cells            :       61968
    | Blanked Cells           :         852
    | Explicitly Blanked Cells:           0
    | Flooded   Cells         :        1650
    | FloodSeed Cells         :        5161
    +--------------------------------+
    Total number of orphans:        8860
    Flood Iteration:           1 Blanked         7619 Interior Cells.
    Flood Iteration:           2 Blanked            0 Interior Cells.
    +--------------------------------+
    | Compute Cells           :      548540
    | Fringe Cells            :       61665
    | Blanked Cells           :          44
    | Explicitly Blanked Cells:           0
    | Flooded   Cells         :        2458
    | FloodSeed Cells         :        5161
    +--------------------------------+
    Total number of orphans:         424
    Flood Iteration:           1 Blanked         7619 Interior Cells.
    Flood Iteration:           2 Blanked            0 Interior Cells.
    +--------------------------------+
    | Compute Cells           :      548540
    | Fringe Cells            :       61709
    | Blanked Cells           :           0
    | Explicitly Blanked Cells:           0
    | Flooded   Cells         :        2458
    | FloodSeed Cells         :        5161
    +--------------------------------+
    Total number of orphans:           0
    Flood Iteration:           1 Blanked         7619 Interior Cells.
    Flood Iteration:           2 Blanked            0 Interior Cells.
    +--------------------------------+
    | Compute Cells           :      548540
    | Fringe Cells            :       61709
    | Blanked Cells           :           0
    | Explicitly Blanked Cells:           0
    | Flooded   Cells         :        2458
    | FloodSeed Cells         :        5161
    +--------------------------------+
    Total number of orphans:           0
    +--------------------------------+
    | Compute Cells           :      548540
    | Fringe Cells            :       46574
    | Blanked Cells           :       15135
    | Explicitly Blanked Cells:           0
    | Flooded   Cells         :        2458
    | FloodSeed Cells         :        5161
    +--------------------------------+
    Total number of orphans:           0

The last iteration of the hole cutting algorithm will print the number of ``Compute Cells``.
With simulations using overset meshes, the code will still loop over all of the cells during residual computations; however, the blanked cells do not add directly to the cost of linear solutions with implicit solvers or the adjoint solver.
As a result, the residual evaluations' cost will still be proportional to the total number of cells, while the cost of linear solutions will roughly be proportional to the number of compute cells.
See the :ref:`overset theory guide <overset_theory>` for more details.