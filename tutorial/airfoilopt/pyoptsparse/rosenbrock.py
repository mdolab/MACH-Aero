# rst Imports
from pyoptsparse import OPT, Optimization, History
import numpy as np
import argparse
import matplotlib.pyplot as plt

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
optProb.addVarGroup(name="xvars", nVars=2, varType="c", value=[3, -3], lower=-5.12, upper=5.12, scale=1.0)

# rst Add constraints
optProb.addCon("con", upper=0, scale=1.0)

# rst Instantiate optimizer
optOptions = {}
opt = OPT(args.opt, options=optOptions)

# rst Solve
sol = opt(optProb, sens=userfuncsens, storeHistory="opt.hst")
print(sol)

# rst Plot

# Load the history file
optHist = History("opt.hst")
values = optHist.getValues()

# Plot contours of the objective and the constraint boundary
x = np.linspace(-5.12, 5.12, 201)
X, Y = np.meshgrid(x, x)
objFunc = 100 * (Y - X**2) ** 2 + (1 - X) ** 2
conFunc = 0.1 - (X - 1) ** 3 - (Y - 1)

fig, ax = plt.subplots()
ax.contour(X, Y, objFunc, levels=40)
ax.contour(X, Y, conFunc, levels=[0.0], colors="r")
ax.contourf(X, Y, conFunc, levels=[0.0, np.inf], colors="r", alpha=0.3)

# Plot the path of the optimizer
ax.plot(values["xvars"][:, 0], values["xvars"][:, 1], "-o", markersize=6, clip_on=False)
ax.plot(values["xvars"][0, 0], values["xvars"][0, 1], "s", markersize=8, clip_on=False)
ax.plot(values["xvars"][-1, 0], values["xvars"][-1, 1], "^", markersize=8, clip_on=False)

fig.savefig("OptimizerPath.png")
