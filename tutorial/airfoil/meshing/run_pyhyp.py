# rst Import
import numpy as np
from pyhyp import pyHyp

# rst GenOptions
options = {
    # ---------------------------
    #        Input Parameters
    # ---------------------------
    "inputFile": "n0012_processed.xyz",
    "unattachedEdgesAreSymmetry": False,
    "outerFaceBC": "farfield",
    "autoConnect": True,
    "BC": {1: {"jLow": "zSymm", "jHigh": "zSymm"}},
    "families": "wall",
    # rst GridOptions
    # ---------------------------
    #        Grid Parameters
    # ---------------------------
    "N": 129,
    "s0": 3e-6,
    "marchDist": 100.0,
    "nConstantStart": 5,
}
# rst Run
hyp = pyHyp(options=options)
hyp.run()
hyp.writeCGNS("n0012.cgns")
