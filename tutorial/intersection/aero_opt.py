# ======================================================================
# Import modules
# ======================================================================

import os
import argparse
from itertools import permutations
from mpi4py import MPI
from pyoptsparse import Optimization, OPT
from multipoint import multiPointSparse
from pprint import pprint
from SETUP import (
    setup_aeroproblem,
    setup_adflow,
    setup_dvgeo,
    setup_dvcon,
    setup_idwarp,
)

# ======================================================================
# Set up I/O
# ======================================================================

parser = argparse.ArgumentParser()
parser.add_argument("--inputdir", type=str, default="./INPUT")
parser.add_argument("--outputdir", type=str, default="./OUTPUT")

# rst dvs (start)
# Get all possible permutations of the DV string
all_DVs = "ftshv"
all_DV_permutations = []

for i in range(1, len(all_DVs) + 1):
    for perm in permutations(all_DVs, i):
        all_DV_permutations.append("".join(perm))

parser.add_argument("--dvs", default="fts", choices=all_DV_permutations)

# rst dvs (end)

args = parser.parse_args()
gcomm = MPI.COMM_WORLD

# Print the arguments
if gcomm.rank == 0:
    print("Arguments are:")
    pprint(vars(args))

# Set the CFD mesh file
gridFile = os.path.join(args.inputdir, "cfd", "dlr-f6_vol.cgns")

# Set full output path
outDir = os.path.join(args.outputdir, args.dvs)

# Create output directory if it does not exist
if gcomm.rank == 0:
    if not os.path.exists(outDir):
        os.makedirs(outDir)

gcomm.Barrier()

# ======================================================================
# Create multipoint communication object
# ======================================================================

MP = multiPointSparse(gcomm)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=gcomm.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

# rst MACH (start)
# ======================================================================
# Set up MACH modules
# ======================================================================

# Set up AeroProblem
ap = setup_aeroproblem.setup()

# Set up ADflow
CFDSolver, CFDPointSetKwargs = setup_adflow.setup(comm, gridFile, outDir)

# Set up IDWarp
mesh = setup_idwarp.setup(comm, gridFile)
CFDSolver.setMesh(mesh)

# Set up DVGeometry
DVGeo = setup_dvgeo.setup(args.inputdir, args.dvs)

# Add DVGeometry object to CFD solver
CFDSolver.setDVGeo(DVGeo, CFDPointSetKwargs)

# Set up DVConstraints
DVCon = setup_dvcon.setup(comm, outDir, DVGeo, CFDSolver, args.dvs)

# rst MACH (end)

# ======================================================================
# Define callback functions
# ======================================================================


def cruiseFuncs(x):
    # Print design variables
    CFDSolver.pp(x)

    # Set design variables
    DVGeo.setDesignVars(x)
    ap.setDesignVars(x)

    # Run CFD
    CFDSolver(ap)

    # Evaluate functions
    funcs = {}
    DVCon.evalFunctions(funcs)
    CFDSolver.evalFunctions(ap, funcs)
    CFDSolver.checkSolutionFailure(ap, funcs)

    # Print funcs
    CFDSolver.pp(funcs)

    return funcs


def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    CFDSolver.evalFunctionsSens(ap, funcsSens)

    return funcsSens


def objCon(funcs, printOK):
    # Set drag as the objective
    funcs["obj"] = funcs[ap["cd"]]

    # Set the lift constraint
    funcs["cl_con_" + ap.name] = funcs[ap["cl"]] - 0.5

    if printOK:
        pprint(funcs)

    return funcs


# ======================================================================
# Set up optimization
# ======================================================================

# Create optimization problem
optProb = Optimization("dlr-f6", MP.obj, comm=comm)

# Add objective
optProb.addObj("obj", scale=1e2)

# Add variables from the AeroProblem
ap.addVariablesPyOpt(optProb)

# Add DVGeo variables
DVGeo.addVariablesPyOpt(optProb)

# Add constraints
DVCon.addConstraintsPyOpt(optProb)
optProb.addCon("cl_con_" + ap.name, lower=0.0, upper=0.0, scale=1.0)

# Add callback functions and optProb to MP
MP.setProcSetObjFunc("cruise", cruiseFuncs)
MP.setProcSetSensFunc("cruise", cruiseFuncsSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)

# Print optimization problem
if gcomm.rank == 0:
    print(optProb)
optProb.printSparsity()

# Set up optimizer
optOptions = {
    "Major feasibility tolerance": 1e-5,
    "Major optimality tolerance": 1e-5,
    "Difference interval": 1e-4,
    "Hessian full memory": None,
    "Function precision": 1e-8,
    "Nonderivative linesearch": None,
    "Print file": os.path.join(outDir, "SNOPT_print.out"),
    "Summary file": os.path.join(outDir, "SNOPT_summary.out"),
}
opt = OPT("SNOPT", options=optOptions)

# Run optimization
sol = opt(optProb, MP.sens, storeHistory=os.path.join(outDir, "opt.hst"))
if comm.rank == 0:
    print(sol)
