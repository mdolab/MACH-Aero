# rst Imports
import numpy as np
from adflow import ADFLOW
from baseclasses import AeroProblem
from mpi4py import MPI

# rst ADflow options
aeroOptions = {
    # I/O Parameters
    "gridFile": "wing_vol.cgns",
    "outputDirectory": ".",
    "monitorvariables": ["resrho", "cl", "cd"],
    "writeTecplotSurfaceSolution": True,
    # Physics Parameters
    "equationType": "RANS",
    # Solver Parameters
    "smoother": "dadi",
    "MGCycle": "sg",
    # ANK Solver Parameters
    "useANKSolver": True,
    # NK Solver Parameters
    "useNKSolver": True,
    "nkswitchtol": 1e-4,
    # Termination Criteria
    "L2Convergence": 1e-6,
    "L2ConvergenceCoarse": 1e-2,
    "nCycles": 1000,
}
# rst Start ADflow
# Create solver
CFDSolver = ADFLOW(options=aeroOptions)

# Add features
CFDSolver.addLiftDistribution(150, "z")
CFDSolver.addSlices("z", np.linspace(0.1, 14, 10))

# rst Create AeroProblem
ap = AeroProblem(name="wing", mach=0.8, altitude=10000, alpha=1.5, areaRef=45.5, chordRef=3.25, evalFuncs=["cl", "cd"])
# rst Run ADflow
# Solve
CFDSolver(ap)
# rst Evaluate and print
funcs = {}
CFDSolver.evalFunctions(ap, funcs)
# Print the evaluated functions
if MPI.COMM_WORLD.rank == 0:
    print(funcs)
