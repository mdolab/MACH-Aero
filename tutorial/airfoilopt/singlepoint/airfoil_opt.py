# ======================================================================
#         Import modules
# ======================================================================
# rst Imports (beg)
import os
import numpy as np
import argparse
import ast
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
parser.add_argument("--opt", type=str, default="SLSQP", choices=["SLSQP", "SNOPT"])
parser.add_argument("--gridFile", type=str, default="n0012.cgns")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
args = parser.parse_args()
# rst args (end)

# ======================================================================
#         Specify parameters for optimization
# ======================================================================
# rst parameters (beg)
# cL constraint
mycl = 0.5
# angle of attack
alpha = 1.5
# mach number
mach = 0.75
# cruising altitude
alt = 10000
# rst parameters (end)
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
    # Common Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
    # Physics Parameters
    "equationType": "RANS",
    "smoother": "DADI",
    "MGCycle": "sg",
    "nCycles": 20000,
    "monitorvariables": ["resrho", "cl", "cd"],
    "useNKSolver": True,
    "useanksolver": True,
    "nsubiterturb": 10,
    "liftIndex": 2,
    "infchangecorrection": True,
    # Convergence Parameters
    "L2Convergence": 1e-15,
    "L2ConvergenceCoarse": 1e-4,
    # Adjoint Parameters
    "adjointSolver": "GMRES",
    "adjointL2Convergence": 1e-12,
    "ADPC": True,
    "adjointMaxIter": 5000,
    "adjointSubspaceSize": 400,
    "ILUFill": 3,
    "ASMOverlap": 3,
    "outerPreconIts": 3,
    "NKSubSpaceSize": 400,
    "NKASMOverlap": 4,
    "NKPCILUFill": 4,
    "NKJacobianLag": 5,
    "nkswitchtol": 1e-6,
    "nkouterpreconits": 3,
    "NKInnerPreConIts": 3,
    "writeSurfaceSolution": False,
    "writeVolumeSolution": False,
    "frozenTurbulence": False,
    "restartADjoint": False,
}

# Create solver
CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
# rst adflow (end)
# ======================================================================
#         Set up flow conditions with AeroProblem
# ======================================================================
# rst aeroproblem (beg)
ap = AeroProblem(name="fc", alpha=alpha, mach=mach, altitude=alt, areaRef=1.0, chordRef=1.0, evalFuncs=["cl", "cd"])
# Add angle of attack variable
ap.addDV("alpha", value=alpha, lower=0, upper=10.0, scale=1.0)
# rst aeroproblem (end)
# ======================================================================
#         Geometric Design Variable Set-up
# ======================================================================
# rst dvgeo (beg)
# Create DVGeometry object
FFDFile = "ffd.xyz"

DVGeo = DVGeometry(FFDFile)
DVGeo.addLocalDV("shape", lower=-0.05, upper=0.05, axis="y", scale=1.0)

span = 1.0
pos = np.array([0.5]) * span
CFDSolver.addSlices("z", pos, sliceType="absolute")

# Add DVGeo object to CFD solver
CFDSolver.setDVGeo(DVGeo)
# rst dvgeo (end)
# ======================================================================
#         DVConstraint Setup
# ======================================================================
# rst dvcon (beg)

DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)

# Only ADflow has the getTriangulatedSurface Function
DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

# Le/Te constraints
lIndex = DVGeo.getLocalIndex(0)
indSetA = []
indSetB = []
for k in range(0, 1):
    indSetA.append(lIndex[0, 0, k])  # all DV for upper and lower should be same but different sign
    indSetB.append(lIndex[0, 1, k])
for k in range(0, 1):
    indSetA.append(lIndex[-1, 0, k])
    indSetB.append(lIndex[-1, 1, k])
DVCon.addLeTeConstraints(0, indSetA=indSetA, indSetB=indSetB)

# DV should be same along spanwise
lIndex = DVGeo.getLocalIndex(0)
indSetA = []
indSetB = []
for i in range(lIndex.shape[0]):
    indSetA.append(lIndex[i, 0, 0])
    indSetB.append(lIndex[i, 0, 1])
for i in range(lIndex.shape[0]):
    indSetA.append(lIndex[i, 1, 0])
    indSetB.append(lIndex[i, 1, 1])
DVCon.addLinearConstraintsShape(indSetA, indSetB, factorA=1.0, factorB=-1.0, lower=0, upper=0)

le = 0.0001
leList = [[le, 0, le], [le, 0, 1.0 - le]]
teList = [[1.0 - le, 0, le], [1.0 - le, 0, 1.0 - le]]

DVCon.addVolumeConstraint(leList, teList, 2, 100, lower=1, scaled=True)
DVCon.addThicknessConstraints2D(leList, teList, 2, 100, lower=0.1, upper=3.0)

if comm.rank == 0:
    fileName = os.path.join(args.output, "constraints.dat")
    DVCon.writeTecplot(fileName)
# rst dvcon (end)
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
    if MPI.COMM_WORLD.rank == 0:
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
    if MPI.COMM_WORLD.rank == 0:
        print(funcs)
    return funcs


def cruiseFuncsSens(x, funcs):
    funcsSens = {}
    DVCon.evalFunctionsSens(funcsSens)
    CFDSolver.evalFunctionsSens(ap, funcsSens)
    CFDSolver.checkAdjointFailure(ap, funcsSens)
    if MPI.COMM_WORLD.rank == 0:
        print(funcsSens)
    return funcsSens


def objCon(funcs, printOK):
    # Assemble the objective and any additional constraints:
    funcs["obj"] = funcs[ap["cd"]]
    funcs["cl_con_" + ap.name] = funcs[ap["cl"]] - mycl
    if printOK:
        print("funcs in obj:", funcs)
    return funcs


# rst funcs (end)
# ======================================================================
#         Optimization Problem Set-up
# ======================================================================
# rst optprob (beg)
# Create optimization problem
optProb = Optimization("opt", MP.obj, comm=MPI.COMM_WORLD)

# Add objective
optProb.addObj("obj", scale=1e4)

# Add variables from the AeroProblem
ap.addVariablesPyOpt(optProb)

# Add DVGeo variables
DVGeo.addVariablesPyOpt(optProb)

# Add constraints
DVCon.addConstraintsPyOpt(optProb)
optProb.addCon("cl_con_" + ap.name, lower=0.0, upper=0.0, scale=1.0)

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
    }
optOptions.update(args.optOptions)
opt = OPT(args.opt, options=optOptions)

# Run Optimization
sol = opt(optProb, MP.sens, storeHistory=os.path.join(args.output, "opt.hst"))
if MPI.COMM_WORLD.rank == 0:
    print(sol)
