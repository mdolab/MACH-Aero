# rst Imports
import argparse
from pyhyp import pyHyp

parser = argparse.ArgumentParser()
parser.add_argument("--level", default="L1")
args = parser.parse_args()

# rst SetLevels
if args.level in ["L0.5", "L1.5", "L2", "L3"]:
    family = args.level
else:
    family = "L1"

coarsen_levels = {
    "L0.5": 1,
    "L1": 1,
    "L1.5": 2,
    "L2": 2,
    "L3": 3,  # debug only level
}
coarsen = coarsen_levels[args.level]

ngrid_levels = {
    "L0.5": 257,
    "L1": 193,
    "L1.5": 129,
    "L2": 97,
    "L3": 49,
}
ngrid = ngrid_levels[args.level]

level_fact = {
    "L0.5": 4 * 1.414,
    "L1": 4.0,
    "L1.5": 2.0 * 1.414,
    "L2": 2.0,
    "L3": 1.0,
}
s0 = 1e-5 / level_fact[args.level]


# rst general
options = {
    # ---------------------------
    #   General options
    # ---------------------------
    "inputFile": "wing_surf_L1.cgns",
    "fileType": "CGNS",
    "unattachedEdgesAreSymmetry": True,
    "outerFaceBC": "farfield",
    "autoConnect": True,
    "BC": {},
    "families": "wall",
    # rst grid
    # ---------------------------
    #   Grid Parameters
    # ---------------------------
    "coarsen": coarsen,
    "N": ngrid,
    "s0": s0,
    "marchDist": 23.2 * 14,
    # rst pseudo
    # ---------------------------
    #   Pseudo Grid Parameters
    # ---------------------------
    "ps0": -1.0,
    "pGridRatio": -1.0,
    "cMax": 1.0,
    # rst smoothing
    # ---------------------------
    #   Smoothing parameters
    # ---------------------------
    "theta": 3.0,
    "volCoef": 0.25,
    # apply scheduling to all grids
    "volSmoothiter": [[0.0, 20], [0.3, 50], [0.7, 100], [1.0, 100]],
    "volBlend": [[0.0, 1e-6], [0.5, 1e-6], [0.8, 1e-4], [1.0, 1e-3]],
    "epsE": [[0.0, 0.5], [0.5, 1.0], [0.9, 2.0], [1.0, 4.0]],
    "epsI": [[0.0, 1.0], [0.5, 2.0], [0.9, 4.0], [1.0, 8.0]],
    # rst solution
    # ---------------------------
    #   Solution Parameters
    # ---------------------------
    "kspRelTol": 1e-8,
    "kspMaxIts": 1500,
    "kspSubspaceSize": 50,
}
# rst run pyHyp
hyp = pyHyp(options=options)
hyp.run()
hyp.writeCGNS(f"wing_vol_{args.level}.cgns")
