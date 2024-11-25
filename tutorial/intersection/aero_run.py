import os
from mpi4py import MPI
from SETUP import setup_aeroproblem, setup_adflow

# Setup I/O
comm = MPI.COMM_WORLD
gridFile = "INPUT/cfd/dlr-f6_vol.cgns"
outDir = "OUTPUT/analysis"

# Create output directory if it does not exist
if comm.rank == 0:
    if not os.path.exists(outDir):
        os.makedirs(outDir)

# Set up ADflow
CFDSolver = setup_adflow.setup(comm, gridFile, outDir)[0]

# Set up AeroProblem
ap = setup_aeroproblem.setup()

# Run ADflow
CFDSolver(ap)

# Evaluate functions
funcs = {}
CFDSolver.evalFunctions(ap, funcs)

# Print the evaluated functions
CFDSolver.pp(funcs)
