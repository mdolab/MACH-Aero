# rst Imports
from pyoptsparse import OPT, Optimization
import argparse

# rst Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--opt", type=str, default="slsqp")
args = parser.parse_args()

# rst Callback function
def userfunc(xdict):
    x = xdict["xvars"]  # Extract array
    funcs = {}
    funcs["obj"] = 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2
    funcs["con"] = 0.1 - (x[0] - 1) ** 3 - (x[1] - 1)
    return funcs


# rst Sensitivity function
def userfuncsens(xdict, funcs):
    x = xdict["xvars"]  # Extract array
    funcsSens = {}
    funcsSens["obj"] = {
        "xvars": [2 * 100 * (x[1] - x[0] ** 2) * (-2 * x[0]) - 2 * (1 - x[0]), 2 * 100 * (x[1] - x[0] ** 2)]
    }
    funcsSens["con"] = {"xvars": [-3 * (x[0] - 1) ** 2, -1]}
    return funcsSens


# rst Optimization problem
optProb = Optimization("Rosenbrock function", userfunc)

# rst Add objective
optProb.addObj("obj")

# rst Add design variables
optProb.addVarGroup(name="xvars", nVars=2, type="c", value=[3, -3], lower=-5.12, upper=5.12, scale=1.0)
optProb.finalizeDesignVariables()

# rst Add constraints
optProb.addCon("con", upper=0, scale=1.0)

# rst Instantiate optimizer
optOptions = {}
opt = OPT(args.opt, options=optOptions)

# rst Solve
sol = opt(optProb, sens=userfuncsens, storeHistory="opt.hst")
print(sol)
