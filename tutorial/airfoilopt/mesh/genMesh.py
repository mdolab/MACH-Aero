# rst Import
import numpy as np
from pyhyp import pyHyp

# rst SurfMesh
data = np.loadtxt("n0012.dat")
x = data[:, 0].copy()
y = data[:, 1].copy()
ndim = x.shape[0]

airfoil3d = np.zeros((ndim, 2, 3))
for j in range(2):
    airfoil3d[:, j, 0] = x[:]
    airfoil3d[:, j, 1] = y[:]
# set the z value on two sides to 0 and 1
airfoil3d[:, 0, 2] = 0.0
airfoil3d[:, 1, 2] = 1.0
# write out plot3d
P3D_fname = "n0012.xyz"
with open(P3D_fname, "w") as p3d:
    p3d.write(str(1) + "\n")
    p3d.write(str(ndim) + " " + str(2) + " " + str(1) + "\n")
    for ell in range(3):
        for j in range(2):
            for i in range(ndim):
                p3d.write("%.15f\n" % (airfoil3d[i, j, ell]))

# rst GenOptions
options = {
    # ---------------------------
    #        Input Parameters
    # ---------------------------
    "inputFile": P3D_fname,
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
}
# rst Run
hyp = pyHyp(options=options)
hyp.run()
hyp.writeCGNS("n0012.cgns")
