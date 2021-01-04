# rst Imports
from pyhyp import pyHyp

# rst general
options = {
    # ---------------------------
    #   General options
    # ---------------------------
    "inputFile": "wing.cgns",
    "fileType": "cgns",
    "unattachedEdgesAreSymmetry": True,
    "outerFaceBC": "farfield",
    "autoConnect": True,
    "BC": {},
    "families": "wall",
    # rst grid
    # ---------------------------
    #   Grid Parameters
    # ---------------------------
    "N": 49,
    "s0": 1e-5,
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
    "epsE": 1.0,
    "epsI": 2.0,
    "theta": 3.0,
    "volCoef": 0.2,
    "volBlend": 0.0005,
    "volSmoothIter": 20,
    # rst solution
    # ---------------------------
    #   Solution Parameters
    # ---------------------------
    "kspRelTol": 1e-10,
    "kspMaxIts": 1500,
    "kspSubspaceSize": 50,
}
# rst run pyHyp
hyp = pyHyp(options=options)
hyp.run()
hyp.writeCGNS("wing_vol.cgns")
