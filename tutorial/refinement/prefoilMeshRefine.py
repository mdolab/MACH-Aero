from pyhyp import pyHyp
from prefoil import sampling, Airfoil
from prefoil.utils import generateNACA


# L2 layer mesh grid initilization
# We will refine the mesh from this starting grid
nTE_cells_L2 = 5
nSurfPts_L2 = 200
nLayers_L2 = 80
s0_L2 = 4e-6

# Increasing the mesh sizes
refinement = [1, 2, 4]
level = ["L2", "L1", "L0"]

for i in range(len(refinement)):
    # number of points on the airfoil surface
    nSurfPts = refinement[i] * nSurfPts_L2

    # number of points on the TE.
    nTEPts = refinement[i] * nTE_cells_L2

    # number of extrusion layers
    nExtPts = refinement[i] * nLayers_L2

    # first off wall spacing
    s0 = s0_L2 / refinement[i]

    #### We can either import our desired airfoil .dat file and continue the meshing proces ####
    #### Or we can generate the NACA airfoils if our baseline is a 4 series NACA airfoil    ####

    # We can also  generate NACA 4 series airfoils
    code = "0012"
    nPts = 150
    initCoords = generateNACA(code, nPts, spacingFunc=sampling.polynomial, func_args={"order": 8})
    airfoil = Airfoil(initCoords)

    coords = airfoil.getSampledPts(
        nSurfPts,
        spacingFunc=sampling.polynomial,
        func_args={"order": 8},
        nTEPts=nTEPts,
    )

    # Write surface mesh
    airfoil.writeCoords(f"./input/naca0012_{level[i]}", file_format="plot3d")

    options = {
        # ---------------------------
        #        Input Parameters
        # ---------------------------
        "inputFile": f"./input/naca0012_{level[i]}.xyz",
        "unattachedEdgesAreSymmetry": False,
        "outerFaceBC": "farfield",
        "autoConnect": True,
        "BC": {1: {"jLow": "zSymm", "jHigh": "zSymm"}},
        "families": "wall",
        # ---------------------------m
        #        Grid Parameters
        # ---------------------------
        "N": nExtPts,
        "s0": s0,
        "marchDist": 100.0,
    }

    hyp = pyHyp(options=options)
    hyp.run()
    hyp.writeCGNS(f"./input/naca0012_{level[i]}.cgns")
