import os
from pygeo import DVConstraints


def setup(comm, outDir, DVGeo, CFDSolver, DVs):
    DVCon = DVConstraints()
    DVCon.setDVGeo(DVGeo)

    # Only ADflow has the getTriangulatedSurface Function
    DVCon.setSurface(CFDSolver.getTriangulatedMeshSurface())

    # Only add constraints if we have wing shape DVs
    if "s" in DVs:
        # rst LE/TE (start)
        # Add LE/TE constraints
        DVCon.addLeTeConstraints(0, "iLow", comp="wing")
        DVCon.addLeTeConstraints(0, "iHigh", comp="wing")
        # rst LE/TE (end)

        # Add thickness constraints
        leList = [
            [0.0450188791478617292, 0.0848143087801493439, 0.0],
            [0.12148715764275983, 0.234069846128850151, 0.0],
            [0.30061673153558871, 0.584771109087198315, 0.0],
        ]
        teList = [
            [0.238116898268081913, 0.0848143087801493439, 0.0],
            [0.238116898268081913, 0.234069846128850151, 0.0],
            [0.360958503475738213, 0.584771109087198315, 0.0],
        ]
        # rst thickness (start)
        DVCon.addThicknessConstraints2D(
            name="thickness",
            leList=leList,
            teList=teList,
            nSpan=10,
            nChord=10,
            lower=1.0,
            upper=3.0,
            compNames=["wing"],
        )
        # rst thickness (end)

    # Write out constraints file for visualization
    if comm.rank == 0:
        conFileName = os.path.join(outDir, "constraints_wing.dat")
        DVCon.writeTecplot(conFileName)

    return DVCon
