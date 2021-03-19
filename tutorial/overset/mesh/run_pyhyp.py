# ======================================================================
#         Import modules
# ======================================================================
# rst Imports (beg)
from collections import OrderedDict
from mpi4py import MPI
from pyhyp import pyHypMulti
from cgnsutilities.cgnsutilities import readGrid, combineGrids
import argparse

# rst Imports (end)


# ======================================================================
#         Init stuff
# ======================================================================
# rst Init (beg)
rank = MPI.COMM_WORLD.rank

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", default=".")
parser.add_argument("--output_dir", default=".")
parser.add_argument("--level", default="L1")
args = parser.parse_args()
# rst Init (end)


# ======================================================================
#         Specify parameters for extrusion
# ======================================================================
# rst parameters (beg)
# Near-Field
# reference first off wall spacing for L2 level meshes
s0 = 1.4e-7

# number of Levels in the near-Field
nNearfield = {"L3": 31, "L2": 61, "L1": 121}[args.level]


# Farfield
# background mesh spacing
dhStar = {"L3": 0.178, "L2": 0.09, "L1": 0.045}[args.level]

nFarfield = {"L3": 13, "L2": 25, "L1": 49}[args.level]


# General
# factor for spacings
fact = {"L3": 1.0, "L2": 2.0, "L1": 4.0}[args.level]

# levels of coarsening for the surface meshes
coarsen = {"L1": 1, "L2": 2, "L3": 3}[args.level]
# rst parameters (end)


# ======================================================================
#         Common PyHyp options
# ======================================================================
# rst common_options (beg)
commonOptions = {
    # ---------------------------
    #        Input Parameters
    # ---------------------------
    "unattachedEdgesAreSymmetry": False,
    "outerFaceBC": "overset",
    "autoConnect": True,
    "fileType": "cgns",
    # ---------------------------
    #        Grid Parameters
    # ---------------------------
    "N": nNearfield,
    "s0": s0 / fact,
    "marchDist": 2.5 * 0.8,
    "coarsen": coarsen,
    "nConstantEnd": 2,
    # ---------------------------
    #   Pseudo Grid Parameters
    # ---------------------------
    "ps0": -1,
    "pGridRatio": -1,
    "cMax": 1.0,
    # ---------------------------
    #   Smoothing parameters
    # ---------------------------
    "epsE": 1.0,
    "epsI": 2.0,
    "theta": 1.0,
    "volCoef": 0.5,
    "volBlend": 0.00001,
    "volSmoothIter": int(100 * fact),
}
# rst common_options (end)


# ======================================================================
#         Individual PyHyp options
# ======================================================================
# rst individual_options (beg)
# wing options
wing_dict = {
    "inputFile": "%s/near_wing.cgns" % (args.input_dir),
    "outputFile": "%s/near_wing_vol_%s.cgns" % (args.output_dir, args.level),
    "BC": {1: {"iLow": "ySymm"}, 2: {"iLow": "ySymm"}, 3: {"iLow": "ySymm"}},
    "families": "near_wing",
}

# tip options
tip_dict = {
    "inputFile": "%s/near_tip.cgns" % (args.input_dir),
    "outputFile": "%s/near_tip_vol_%s.cgns" % (args.output_dir, args.level),
    "families": "near_tip",
    "splay": 0.0,
}
# rst individual_options (end)


# ======================================================================
#         Generate Near-Field
# ======================================================================
# rst near_field (beg)
# figure out what grids we will generate again
options = OrderedDict()
options["wing"] = wing_dict
options["tip"] = tip_dict

# Run pyHypMulti
hyp = pyHypMulti(options=options, commonOptions=commonOptions)
MPI.COMM_WORLD.barrier()
# rst near_field (end)


# ======================================================================
#        Combine Near-Field
# ======================================================================
# rst combine_near_field (beg)
# read the grids
wing = "%s/near_wing_vol_%s.cgns" % (args.output_dir, args.level)
tip = "%s/near_tip_vol_%s.cgns" % (args.output_dir, args.level)

wingGrid = readGrid(wing)
tipGrid = readGrid(tip)

gridList = [wingGrid, tipGrid]

# combine grids
combinedGrid = combineGrids(gridList)

# move to y=0
combinedGrid.symmZero("y")
# rst combine_near_field (end)


# ======================================================================
#        Generate Far-Field
# ======================================================================
# rst far_field (beg)
farfield = "%s/far_%s.cgns" % (args.output_dir, args.level)
combinedGrid.simpleOCart(dhStar, 40.0, nFarfield, "y", 1, farfield)
# rst far_field (end)


# ======================================================================
#        Combine all Grids
# ======================================================================
# rst combine (beg)
# we can do the stuff in one proc after this point
if rank == 0:
    # read the grids
    farfieldGrid = readGrid(farfield)
    gridList.append(farfieldGrid)
    finalGrid = combineGrids(gridList)

    # write the final file
    finalGrid.writeToCGNS("%s/ONERA_M6_%s.cgns" % (args.output_dir, args.level))
# rst combine (end)
