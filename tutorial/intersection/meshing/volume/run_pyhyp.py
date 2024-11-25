from pyhyp import pyHyp

options = {
    "inputFile": "collar_surf.cgns",
    "fileType": "CGNS",
    "unattachedEdgesAreSymmetry": False,
    "outerFaceBC": "overset",
    "N": 65,
    "s0": 1e-5,
    "marchDist": 0.25,
    "splay": 0.25,
    "epsE": 10.0,
    "epsI": 20.0,
    "theta": 6.0,
    "volCoef": 0.9,
    "volBlend": 1e-8,
    "volSmoothIter": 20,
}

# Run pyHyp
hyp = pyHyp(options=options)
hyp.run()
hyp.writeCGNS("collar_vol.cgns")
