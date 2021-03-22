# rst start
from baseclasses import AeroProblem
from adflow import ADFLOW
import argparse

# ======================================================================
#         Init stuff
# ======================================================================
# rst Init (beg)
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", default=".")
parser.add_argument("--output_dir", default=".")
parser.add_argument("--level", default="L1")
args = parser.parse_args()
# rst Init (end)

# ======================================================================
#         Input Information
# ======================================================================

# File name of the mesh
gridFile = "%s/ONERA_M6_%s.cgns" % (args.output_dir, args.level)

# Common aerodynamic problem description and design variables
ap = AeroProblem(name="ihc_check", mach=0.3, altitude=1000, areaRef=0.24 * 0.64 * 2, chordRef=0.24)

# dictionary with name of the zone as a key and a factor to multiply it with.
oversetpriority = {}

aeroOptions = {
    # Common Parameters
    "gridFile": gridFile,
    "outputDirectory": "./",
    "MGCycle": "sg",
    "volumeVariables": ["blank"],
    "surfaceVariables": ["blank"],
    # Physics Parameters
    "equationType": "RANS",
    # Debugging parameters
    "debugZipper": False,
    "useZipperMesh": False,
    # number of times to run IHC cycle
    "nRefine": 10,
    # number of flooding iterations per IHC cycle.
    # the default value of -1 just lets the algorithm run until flooded cells stop changing
    "nFloodIter": -1,
    "nearWallDist": 0.1,
    "oversetPriority": oversetpriority,
}

# Create solver
CFDSolver = ADFLOW(options=aeroOptions, debug=False)

# Uncoment this if just want to check flooding
CFDSolver.setAeroProblem(ap)

name = ".".join(gridFile.split(".")[0:-1])
CFDSolver.writeVolumeSolutionFile(name + "_IHC.cgns", writeGrid=True)
# rst end
