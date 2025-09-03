import numpy as np
from adflow import ADFLOW


def setup(comm, gridFile, outputDirectory):
    # rst cutCallback (start)
    # Define function to blank cells behind symmetry plane
    def cutCallback(xCen, CGNSZoneNameIDs, cellIDs, flags):
        flags[xCen[:, 1] < 0] = 1

    # rst cutCallback (end)

    aeroOptions = {
        # I/O parameters
        "gridFile": gridFile,
        "outputDirectory": outputDirectory,
        "writeSurfaceSolution": True,
        "writeVolumeSolution": True,
        "writeTecplotSurfaceSolution": True,
        "isoSurface": {"shock": 1, "vx": -0.0001},
        "solutionPrecision": "double",
        "monitorVariables": ["resrho", "resturb", "cl", "cd", "cpu"],
        "surfaceVariables": [
            "vx",
            "vy",
            "vz",
            "rho",
            "P",
            "cp",
            "cf",
            "cfx",
            "cfy",
            "cfz",
            "blank",
        ],
        "volumeVariables": ["resrho", "mach", "cp", "resturb", "blank"],
        # Physics parameters
        "equationType": "RANS",
        "useQCR": True,
        "useRotationSA": True,
        "liftIndex": 3,
        # Discretization parameters
        "CFL": 1.25,
        "MGCycle": "sg",
        "nSubiterTurb": 7,
        # NK parameters
        "useNKSolver": True,
        "NKADPC": True,
        "NKASMOverlap": 2,
        "NKInnerPreconIts": 2,
        "NKJacobianLag": 5,
        "NKLS": "non-monotone",
        "NKOuterPreconIts": 2,
        "NKSubspaceSize": 100,
        "NKSwitchTol": 1e-07,
        # ANK parameters
        "useANKSolver": True,
        "ANKSecondOrdSwitchTol": 1e-4,
        "ANKStepMin": 0.1,
        "ANKSwitchTol": 10.0,
        "ANKASMOverlap": 2,
        # Convergence criteria
        "nCycles": 8000,
        "L2Convergence": 1e-10,
        # Adjoint parameters
        "adjointL2Convergence": 1e-10,
        "adjointMaxIter": 250,
        "adjointSubspaceSize": 250,
        "ADPC": True,
        "ILUFill": 2,
        "ASMOverlap": 2,
        "innerPreconIts": 3,
        "skipAfterFailedAdjoint": False,
        # Overset parameters
        "nearWallDist": 0.001,
        "cutCallback": cutCallback,
    }

    # Create solver
    CFDSolver = ADFLOW(options=aeroOptions, comm=comm)

    # rst families (start)
    # Add wing family group
    CFDSolver.addFamilyGroup(
        "wing_full",
        [
            "intersection_0",
            "wing",
        ],
    )

    # Add wing and total lift distribution
    CFDSolver.addLiftDistribution(200, "y", groupName="wing_full")
    CFDSolver.addLiftDistribution(200, "y")

    # Add fuselage slice
    CFDSolver.addSlices("y", 0.0001)

    # Add wing slices
    CFDSolver.addSlices("y", np.linspace(0.074, 0.55, 10), groupName="wing_full")
    # rst families (end)

    # rst CFDPointSetKwargs (start)
    # Set point set arguments for DVGeoMulti
    CFDPointSetKwargs = {
        "applyIC": True,
        "comm": comm,
    }
    # rst CFDPointSetKwargs (end)

    return CFDSolver, CFDPointSetKwargs
