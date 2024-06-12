import os
import argparse
import matplotlib.pyplot as plt
from pyoptsparse import History


def main(args):
    if not os.path.isfile(args.histFile):
        raise FileNotFoundError(f"History file '{args.histFile}' not found.")

    opt_hist = History(args.histFile)
    hist_values = opt_hist.getValues()

    if opt_hist.getMetadata()["optimizer"] == "SNOPT":
        _, axes = plt.subplots(nrows=5, sharex=True, figsize=(10, 14))

        # Objective Optimality and Feasibility
        axes[4].plot("nMajor", "optimality", data=hist_values, label="Optimality")
        axes[4].plot("nMajor", "feasibility", data=hist_values, label="Feasibility")
        axes[4].set_yscale("log")
        axes[4].axhline(1e-4, linestyle="--", color="gray")
        axes[4].annotate("Convergence Criteria", xy=(3, 9e-5), ha="left", va="top", fontsize=24, color="gray")
        axes[4].legend(fontsize=20, labelcolor="linecolor", loc="upper right", frameon=False)
        axes[4].autoscale(enable=True, tight=True)

    else:
        _, axes = plt.subplots(nrows=4, sharex=True, figsize=(10, 14))

    # Objective (Drag Coefficient)
    axes[0].plot("iter", "obj", data=hist_values, label="Objective ($C_D$)")
    axes[0].set_ylabel("Objective ($C_D$)", rotation="horizontal", ha="right", fontsize=24)

    # Angle of Attack
    axes[1].plot("iter", "alpha_wing", data=hist_values, label="Angle of Attack")
    axes[1].set_ylabel(r"$\alpha$ [$^\circ$]", rotation="horizontal", ha="right", fontsize=24)

    # Wing Twist
    axes[2].plot("iter", "twist", data=hist_values, label="Wing Twist")
    axes[2].set_ylabel("Twist [$^\circ$]", rotation="horizontal", ha="right", fontsize=24)

    # Lift Constraint
    axes[3].plot("iter", "cl_con_wing", data=hist_values, label="Lift Constraint")
    axes[3].set_ylabel("Lift Constraint", rotation="horizontal", ha="right", fontsize=24)

    # Adjust subplot aesthetics
    for ax in axes:
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["left"].set_position(("outward", 12))
        ax.spines["bottom"].set_position(("outward", 12))

    plt.show()
    plt.savefig(os.path.join(args.outputDir, "aero_wing_opt_hist.jpg"), bbox_inches="tight")


if __name__ == "__main__":
    # plt.rcParams["text.usetex"] = True  # Comment out if latex installation is not present
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.size"] = 20
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    plt.rcParams["lines.linewidth"] = 3.0

    parser = argparse.ArgumentParser()
    parser.add_argument("--histFile", type=str, default="opt.hst")
    parser.add_argument("--outputDir", type=str, default="./")
    args = parser.parse_args()

    main(args)
