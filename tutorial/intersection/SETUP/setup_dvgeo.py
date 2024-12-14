import os
import numpy as np
from pygeo import DVGeometry, DVGeometryMulti, geo_utils


def setup(inputDir, DVs):
    # rst ffd
    # Get the FFD files
    fuseFFD = os.path.join(inputDir, "ffd", "dlr-f6_fuse.xyz")
    wingFFD = os.path.join(inputDir, "ffd", "dlr-f6_wing.xyz")

    # rst tri
    # Get the triangulated surface mesh files
    fuseTri = os.path.join(inputDir, "tri", "dlr-f6_fuse.cgns")
    wingTri = os.path.join(inputDir, "tri", "dlr-f6_wing.cgns")

    # rst featureCurves
    # Define feature curves on the wing
    featureCurves = {
        "curve_te_upp": 2,  # upper trailing edge
        "curve_te_low": 2,  # lower trailing edge
        "curve_le": 2,  # leading edge
        "root_skin": None,
        "root_te": None,
    }

    # rst curveEpsDict
    # Define the curve projection tolerances
    curveEpsDict = {
        "curve_te_upp": 0.5e-4,  # upper trailing edge
        "curve_te_low": 0.5e-4,  # lower trailing edge
        "curve_le": 0.5e-4,  # leading edge
        "root_skin": 0.5e-4,
        "root_te": 0.5e-4,
        "intersection": 1.3e-4,
    }

    # rst objects
    # Create DVGeometry objects
    DVGeoFuse = DVGeometry(fuseFFD)
    DVGeoWing = DVGeometry(wingFFD)

    # Create the DVGeometryMulti object
    DVGeo = DVGeometryMulti()

    # rst components
    # Define component names
    comps = ["fuse", "wing"]

    # Add components
    DVGeo.addComponent(comps[0], DVGeoFuse, triMesh=fuseTri, scale=0.001)
    DVGeo.addComponent(comps[1], DVGeoWing, triMesh=wingTri, scale=0.001)

    # rst intersection
    # Add intersection
    DVGeo.addIntersection(
        comps[0],
        comps[1],
        dStarA=0.06,
        dStarB=0.15,
        featureCurves=featureCurves,
        project=True,
        includeCurves=True,
        curveEpsDict=curveEpsDict,
    )

    # rst wing dvs
    # Add the reference axis, which we use for twist and translation
    if "t" in DVs or "v" in DVs or "h" in DVs:
        # Define a reference axis
        nTwist = DVGeoWing.addRefAxis("wing_axis", xFraction=0.25, alignIndex="j", rotType=4, volumes=[0])

    # Add wing twist design variables
    if "t" in DVs:

        def twist(val, geo):
            # Set all the twist values
            for i in range(nTwist):
                geo.rot_y["wing_axis"].coef[i] = val[i]

        DVGeoWing.addGlobalDV("twist", func=twist, value=np.zeros(nTwist), lower=-4, upper=4, scale=0.1)

    # Add wing shape design variables
    if "s" in DVs:
        DVGeoWing.addLocalDV("shape", lower=-0.01, upper=0.01, axis="z", scale=100.0)

    # Add wing horizontal displacement variable
    if "h" in DVs:

        def wing_x(val, geo):
            # Extract control points of the reference axis
            C = geo.extractCoef("wing_axis")

            # Translate each control point in x
            for i in range(len(C)):
                C[i, 0] = C[i, 0] + val[0]

            # Restore control points to the reference axis
            geo.restoreCoef(C, "wing_axis")

        DVGeoWing.addGlobalDV("wing_x", func=wing_x, value=0.0, lower=-0.1, upper=0.1, scale=1.0)

    # Add wing vertical displacement variable
    if "v" in DVs:

        def wing_z(val, geo):
            # Extract control points of the reference axis
            C = geo.extractCoef("wing_axis")

            # Translate each control point in z
            for i in range(len(C)):
                C[i, 2] = C[i, 2] + val[0]

            # Restore control points to the reference axis
            geo.restoreCoef(C, "wing_axis")

        DVGeoWing.addGlobalDV("wing_z", func=wing_z, value=0.0, lower=-0.1, upper=0.1, scale=0.1)

    # rst fuse dvs
    # Add fuselage design variables
    if "f" in DVs:
        # Create point select to get specific points for the normal variables
        ijkBounds = {0: [[2, -3], [0, 2], [3, -4]]}
        PS = geo_utils.PointSelect("ijkBounds", ijkBounds=ijkBounds)

        # Add normal pertubations to the fairing section
        DVGeoFuse.addLocalSectionDV("normals", "k", pointSelect=PS, lower=-0.04, upper=0.00, scale=200.0)

    # rst end

    return DVGeo
