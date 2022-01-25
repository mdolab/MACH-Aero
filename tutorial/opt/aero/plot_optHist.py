import os
import argparse
import matplotlib.pyplot as plt
from pyoptsparse import History

plt.rcParams["text.usetex"] = True # Comment out if latex installation is not present
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 20
plt.rcParams["xtick.labelsize"] = 16
plt.rcParams["ytick.labelsize"] = 16
plt.rcParams["lines.linewidth"] = 3.0

parser = argparse.ArgumentParser()
parser.add_argument("--histFile", type=str, default="opt.hst")
parser.add_argument("--outputDir", type=str, default="./")
args = parser.parse_args()

optHist = History(args.histFile)
histValues = optHist.getValues()

fig, axes = plt.subplots(nrows=5, sharex=True, constrained_layout=True, figsize=(14, 10))

axes[0].plot("nMajor", "optimality", data=histValues, label="Optimality")
axes[0].plot("nMajor", "feasibility", data=histValues, label="Feasibility")
axes[0].set_yscale("log")
axes[0].axhline(1e-4, linestyle="--", color="gray")
axes[0].annotate("Convergence Criteria", xy=(3, 9e-5), ha="left", va="top", fontsize=24, color="gray")
axes[0].legend(fontsize=20, labelcolor="linecolor", loc="upper right", frameon=False)
axes[0].autoscale(enable=True, tight=True)

axes[1].plot("nMajor", "obj", data=histValues, label="Objective")
axes[1].set_ylabel("Objective \n($C_D$)", rotation="horizontal", ha="right", fontsize=24)

axes[2].plot("nMajor", "alpha_fc", data=histValues, label="Alpha")
axes[2].set_ylabel(r"$\alpha [^\circ]$", rotation="horizontal", ha="right", fontsize=24)

axes[3].plot("nMajor", "twist", data=histValues, label="Twist")
axes[3].set_ylabel(r"Twist $[^\circ]$", rotation="horizontal", ha="right", fontsize=24)

axes[4].plot("nMajor", "cl_con_fc", data=histValues, label="cl_con")
axes[4].set_ylabel("Lift constraint", rotation="horizontal", ha="right", fontsize=24)

for ax in axes:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Drop the rest of the spines
    ax.spines['left'].set_position(('outward', 12))
    ax.spines['bottom'].set_position(('outward', 12))

plt.savefig(os.path.join(args.outputDir, 'aero_wing_opt_hist.png'))
