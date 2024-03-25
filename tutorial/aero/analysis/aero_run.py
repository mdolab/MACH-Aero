# rst Imports
import numpy as np
import argparse
import os
from adflow import ADFLOW
from baseclasses import AeroProblem
from mpi4py import MPI

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output")
parser.add_argument("--gridFile", type=str, default="wing_vol.cgns")
parser.add_argument("--task", choices=["analysis", "polar"], default="analysis")
args = parser.parse_args()

comm = MPI.COMM_WORLD
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

# rst ADflow options
aeroOptions = {
    # I/O Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
    "monitorvariables": ["resrho", "cl", "cd"],
    "writeTecplotSurfaceSolution": True,
    # Physics Parameters
    "equationType": "RANS",
    # Solver Parameters
    "MGCycle": "sg",
    # ANK Solver Parameters
    "useANKSolver": True,
    # NK Solver Parameters
    "useNKSolver": True,
    "NKSwitchTol": 1e-4,
    # Termination Criteria
    "L2Convergence": 1e-6,
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
if args.task == "analysis":
    # Solve
    CFDSolver(ap)
    # rst Evaluate and print
    funcs = {}
    CFDSolver.evalFunctions(ap, funcs)
    # Print the evaluated functions
    if comm.rank == 0:
        print(funcs)
# rst Create polar arrays
elif args.task == "polar":
    # Create an array of alpha values.
    # In this case we create 6 evenly spaced values from 0 - 5.
    alphaList = np.linspace(0, 5, 6)

    # Create storage for the evaluated lift and drag coefficients
    CLList = []
    CDList = []
    # rst Start loop
    # Loop over the alpha values and evaluate the polar
    for alpha in alphaList:
        # rst update AP
        # Update the name in the AeroProblem. This allows us to modify the
        # output file names with the current alpha.
        ap.name = f"wing_{alpha:4.2f}"

        # Update the alpha in aero problem and print it to the screen.
        ap.alpha = alpha
        if comm.rank == 0:
            print(f"current alpha: {ap.alpha}")

        # rst Run ADflow polar
        # Solve the flow
        CFDSolver(ap)

        # Evaluate functions
        funcs = {}
        CFDSolver.evalFunctions(ap, funcs)

        # Store the function values in the output list
        CLList.append(funcs[f"{ap.name}_cl"])
        CDList.append(funcs[f"{ap.name}_cd"])

    # rst Print polar
    # Print the evaluated functions in a table
    if comm.rank == 0:
        print("{:>6} {:>8} {:>8}".format("Alpha", "CL", "CD"))
        print("=" * 24)
        for alpha, cl, cd in zip(alphaList, CLList, CDList):
            print(f"{alpha:6.1f} {cl:8.4f} {cd:8.4f}")
