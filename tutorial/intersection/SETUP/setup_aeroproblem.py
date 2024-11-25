from baseclasses import AeroProblem


def setup():
    # Set initial angle of attack
    alpha0 = -0.082699

    ap = AeroProblem(
        name="fc",
        alpha=alpha0,
        mach=0.75,
        reynolds=5e6,
        reynoldsLength=0.1412,
        T=322.22,
        areaRef=0.1454 / 2.0,
        chordRef=0.1412,
        xRef=0.1579,
        yRef=0.0,
        zRef=-0.03392,
        evalFuncs=["cl", "cd"],
    )

    # Add angle of attack variable
    ap.addDV("alpha", value=alpha0, lower=-4.0, upper=10.0, scale=10.0)

    return ap
