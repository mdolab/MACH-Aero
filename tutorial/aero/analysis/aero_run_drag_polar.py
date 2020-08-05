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
    "infchangecorrection": True,
    # Solver Parameters
    "smoother": "dadi",
    "MGCycle": "sg",
    "MGStartLevel": -1,
    "nCyclesCoarse": 250,
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

# rst Create polar arrays

# Create an array of alpha values.
# In this case we create 6 evenly spaced values from 0 - 5.
alphaList = np.linspace(0, 5, 6)

# Create storage for the evaluated lift and drag coefficients
CL = []
CD = []
# rst Start loop
# Loop over the alpha values and evaluate the polar
for alpha in alphaList:

    # rst update AP
    # Update the name in the AeroProblem. This allows us to modify the
    # output file names with the current alpha.
    ap.name = "wing_%4.2f" % alpha

    # Update the alpha in aero problem and print it to the screen.
    ap.alpha = alpha
    if MPI.COMM_WORLD.rank == 0:
        print("current alpha: %f" % ap.alpha)

    # rst Run ADflow
    # Solve the flow
    CFDSolver(ap)

    # Evaluate functions
    funcs = {}
    CFDSolver.evalFunctions(ap, funcs)

    # Store the function values in the output list
    CL.append(funcs["%s_cl" % ap.name])
    CD.append(funcs["%s_cd" % ap.name])

# rst Print polar
# Print the evaluated functions
if MPI.COMM_WORLD.rank == 0:
    print("Alpha:", alphaList)
    print("CL:", CL)
    print("CD:", CD)
