# ======================================================================
#         Import modules
# ======================================================================
# rst Imports (beg)
import os
import argparse
import ast
import numpy as np
from mpi4py import MPI
from baseclasses import AeroProblem
from adflow import ADFLOW
from pygeo import DVGeometry, DVConstraints
from pyoptsparse import Optimization, OPT
from idwarp import USMesh
from multipoint import multiPointSparse

# rst Imports (end)
# rst args (beg)
# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output")
parser.add_argument("--opt", type=str, default="SLSQP", choices=["IPOPT", "SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="wing_vol.cgns")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()
# rst args (end)
# ======================================================================
#         Create multipoint communication object
# ======================================================================
# rst multipoint (beg)
MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=MPI.COMM_WORLD.size)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

# rst multipoint (end)
# ======================================================================
#         ADflow Set-up
# ======================================================================
# rst adflow (beg)
aeroOptions = {
    # I/O Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
    "monitorvariables": ["resrho", "cl", "cd"],
    "writeTecplotSurfaceSolution": True,
    # Physics Parameters
    "equationType": "RANS",
    # Solver Parameters
    "smoother": "DADI",
    "MGCycle": "sg",
    "infchangecorrection": True,
    # ANK Solver Parameters
    "useANKSolver": True,
    # NK Solver Parameters
    "useNKSolver": True,
    "nkswitchtol": 1e-6,
    # Termination Criteria
    "L2Convergence": 1e-10,
    "L2ConvergenceCoarse": 1e-2,
    "nCycles": 10000,
    # Adjoint Parameters
    "adjointL2Convergence": 1e-10,
}

# Create solver
CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
CFDSolver.addLiftDistribution(150, "z")
CFDSolver.addSlices("z", np.linspace(0.1, 14, 10))
# rst adflow (end)
# ======================================================================
#         Set up flow conditions with AeroProblem
# ======================================================================
# rst aeroproblem (beg)
ap = AeroProblem(name="wing", alpha=1.5, mach=0.8, altitude=10000, areaRef=45.5, chordRef=3.25, evalFuncs=["cl", "cd"])

# Add angle of attack variable
ap.addDV("alpha", value=1.5, lower=0, upper=10.0, scale=0.1)
# rst aeroproblem (end)
# ======================================================================
#         Geometric Design Variable Set-up
# ======================================================================
# rst dvgeo (beg)
# Create DVGeometry object
FFDFile = "ffd.xyz"
DVGeo = DVGeometry(FFDFile)

# Create reference axis
nRefAxPts = DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="k")
nTwist = nRefAxPts - 1


# Set up global design variables
def twist(val, geo):
    for i in range(1, nRefAxPts):
        geo.rot_z["wing"].coef[i] = val[i - 1]


DVGeo.addGlobalDV(dvName="twist", value=[0] * nTwist, func=twist, lower=-10, upper=10, scale=0.01)

# Set up local design variables
DVGeo.addLocalDV("local", lower=-0.5, upper=0.5, axis="y", scale=1)

# Add DVGeo object to CFD solver
CFDSolver.setDVGeo(DVGeo)
# rst dvgeo (end)
# ======================================================================
#         DVConstraint Setup, and Thickness and Volume Constraints
# ======================================================================
# rst dvconVolThick (beg)
DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)

# Only ADflow has the getTriangulatedSurface Function
DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

# Volume constraints
leList = [[0.01, 0, 0.001], [7.51, 0, 13.99]]
teList = [[4.99, 0, 0.001], [8.99, 0, 13.99]]
DVCon.addVolumeConstraint(leList, teList, nSpan=20, nChord=20, lower=1.0, scaled=True)

# Thickness constraints
DVCon.addThicknessConstraints2D(leList, teList, nSpan=10, nChord=10, lower=1.0, scaled=True)
# rst dvconVolThick (end)
# ======================================================================
#         DVConstraint Setup, and LeTe Constraints
# ======================================================================
# rst dvconLeTe (beg)
# Le/Te constraints
DVCon.addLeTeConstraints(0, "iLow")
DVCon.addLeTeConstraints(0, "iHigh")

if comm.rank == 0:
    # Only make one processor do this
    DVCon.writeTecplot(os.path.join(args.output, "constraints.dat"))
# rst dvconLeTe (end)
# ======================================================================
#         Mesh Warping Set-up
# ======================================================================
# rst warp (beg)
meshOptions = {"gridFile": args.gridFile}
mesh = USMesh(options=meshOptions, comm=comm)
CFDSolver.setMesh(mesh)


# rst warp (end)
# ======================================================================
#         Functions:
# ======================================================================
# rst funcs (beg)
def cruiseFuncs(x):
    if comm.rank == 0:
        print(x)
    # Set design vars
    DVGeo.setDesignVars(x)
    ap.setDesignVars(x)
    # Run CFD
    CFDSolver(ap)
    # Evaluate functions
    funcs = {}
    DVCon.evalFunctions(funcs)
    CFDSolver.evalFunctions(ap, funcs)
    CFDSolver.checkSolutionFailure(ap, funcs)
    if comm.rank == 0:
        print(funcs)
    return funcs


def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    CFDSolver.evalFunctionsSens(ap, funcsSens)
    CFDSolver.checkAdjointFailure(ap, funcsSens)
    return funcsSens


def objCon(funcs, printOK):
    # Assemble the objective and any additional constraints:
    funcs["obj"] = funcs[ap["cd"]]
    funcs["cl_con_" + ap.name] = funcs[ap["cl"]] - 0.5
    if printOK:
        print("funcs in obj:", funcs)
    return funcs


# rst funcs (end)
# ======================================================================
#         Optimization Problem Set-up
# ======================================================================
# rst optprob (beg)
# Create optimization problem
optProb = Optimization("opt", MP.obj, comm=comm)

# Add objective
optProb.addObj("obj", scale=1e2)

# Add variables from the AeroProblem
ap.addVariablesPyOpt(optProb)

# Add DVGeo variables
DVGeo.addVariablesPyOpt(optProb)

# Add constraints
DVCon.addConstraintsPyOpt(optProb)
optProb.addCon("cl_con_" + ap.name, lower=0.0, scale=10.0)

# The MP object needs the 'obj' and 'sens' function for each proc set,
# the optimization problem and what the objcon function is:
MP.setProcSetObjFunc("cruise", cruiseFuncs)
MP.setProcSetSensFunc("cruise", cruiseFuncsSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)
optProb.printSparsity()
# rst optprob (end)
# rst optimizer
# Set up optimizer
if args.opt == "SLSQP":
    optOptions = {"IFILE": os.path.join(args.output, "SLSQP.out")}
elif args.opt == "SNOPT":
    optOptions = {
        "Major feasibility tolerance": 1e-4,
        "Major optimality tolerance": 1e-4,
        "Hessian full memory": None,
        "Function precision": 1e-8,
        "Print file": os.path.join(args.output, "SNOPT_print.out"),
        "Summary file": os.path.join(args.output, "SNOPT_summary.out"),
        "Major iterations limit": 1000,
    }
elif args.opt == "IPOPT":
    optOptions = {
        "limited_memory_max_history": 1000,
        "print_level": 5,
        "tol": 1e-6,
        "acceptable_tol": 1e-5,
        "max_iter": 300,
        "start_with_resto": "yes",
    }
optOptions.update(args.optOptions)
opt = OPT(args.opt, options=optOptions)

# Run Optimization
sol = opt(optProb, MP.sens, storeHistory=os.path.join(args.output, "opt.hst"))
if comm.rank == 0:
    print(sol)
