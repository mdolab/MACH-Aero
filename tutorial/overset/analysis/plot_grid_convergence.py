import numpy as np
import matplotlib.pyplot as plt

# Data from: https://turbmodels.larc.nasa.gov/Onerawingnumerics_val/SA/combined_forces_pitchmom_maxmut.dat

data = {
    "ADflow": {
        "N": np.array([153473, 1277538, 10476201]),
        "C_L": np.array([0.26064807, 0.26815573, 0.27054311]),
        "C_D": np.array([0.01879813, 0.01703536, 0.01699923]),
        "C_Dp": np.array([0.01326940, 0.01180256, 0.01177125]),
        "C_Dv": np.array([0.00552873, 0.00523279, 0.00522798]),
        "C_M": np.array([-0.18639411, -0.19025530, -0.19248581]),
    },
    "USM3D, Prism_Hex": {
        "N": np.array([69206016, 8650752, 1081344, 135168]),
        "h": np.array([2.44e-03, 4.87e-03, 9.74e-03, 1.95e-02]),
        "C_L": np.array([2.69e-01, 2.67e-01, 2.67e-01, 2.61e-01]),
        "C_D": np.array([1.70e-02, 1.70e-02, 1.77e-02, 2.13e-02]),
        "C_Dp": np.array([1.17e-02, 1.17e-02, 1.22e-02, 1.51e-02]),
        "C_Dv": np.array([5.30e-03, 5.33e-03, 5.55e-03, 6.18e-03]),
        "C_M": np.array([-1.90e-01, -1.88e-01, -1.88e-01, -1.85e-01]),
    },
    "USM3D, Tetrahedral": {
        "N": np.array([363331584, 45416448, 5677056, 709632, 88704]),
        "h": np.array([1.40e-03, 2.80e-03, 5.61e-03, 1.12e-02, 2.24e-02]),
        "C_L": np.array([2.71e-01, 2.69e-01, 2.67e-01, 2.64e-01, 2.50e-01]),
        "C_D": np.array([1.70e-02, 1.71e-02, 1.74e-02, 1.90e-02, 2.64e-02]),
        "C_Dp": np.array([1.17e-02, 1.18e-02, 1.21e-02, 1.37e-02, 2.11e-02]),
        "C_Dv": np.array([5.31e-03, 5.28e-03, 5.28e-03, 5.37e-03, 5.25e-03]),
        "C_M": np.array([-1.91e-01, -1.90e-01, -1.88e-01, -1.85e-01, -1.75e-01]),
    },
    "FUN3D-FV": {
        "N": np.array([60777345, 7625153, 960225, 121841, 15705, 2093, 300]),
        "h": np.array([2.54e-03, 5.08e-03, 1.01e-02, 2.02e-02, 3.99e-02, 7.82e-02, 0.149380158]),
        "C_L": np.array([0.269545512, 0.267878736, 0.265852518, 0.258628725, 0.248903715, 0.228937233, 0.185943039]),
        "C_D": np.array([1.69e-02, 1.69e-02, 1.72e-02, 2.01e-02, 3.22e-02, 5.30e-02, 7.79e-02]),
        "C_Dp": np.array([1.17e-02, 1.16e-02, 1.18e-02, 1.39e-02, 2.40e-02, 4.01e-02, 6.19e-02]),
        "C_Dv": np.array([5.28e-03, 5.29e-03, 5.41e-03, 6.17e-03, 8.21e-03, 1.29e-02, 1.60e-02]),
        "C_M": np.array(
            [-0.190665241, -0.188882665, -0.186834678, -0.181220113, -0.183886843, -0.191312751, -0.183210354]
        ),
    },
    "CFL3D": {
        "N": np.array([69206016, 69206016, 8650752, 1081344, 135168]),
        "h": np.array([2.44e-03, 2.44e-03, 4.87e-03, 9.74e-03, 1.95e-02]),
        "C_L": np.array([2.69e-01, 2.69e-01, 2.66e-01, 2.66e-01, 2.61e-01]),
        "C_D": np.array([1.70e-02, 1.70e-02, 1.69e-02, 1.74e-02, 1.90e-02]),
        "C_Dp": np.array([1.17e-02, 1.17e-02, 1.16e-02, 1.18e-02, 1.28e-02]),
        "C_Dv": np.array([5.30e-03, 5.30e-03, 5.32e-03, 5.54e-03, 6.21e-03]),
        "C_M": np.array([-1.90e-01, -1.90e-01, -1.87e-01, -1.87e-01, -1.84e-01]),
    },
    "FUN3D-FE": {
        "N": np.array([7625153, 960225, 121841, 15705]),
        "h": np.array([5.08e-03, 1.01e-02, 2.02e-02, 3.99e-02]),
        "C_L": np.array([0.271195, 0.270826, 0.263215, 0.244181]),
        "C_D": np.array([0.016979, 0.017088, 0.01833, 0.025362]),
        "C_Dp": np.array([0.011747, 0.011849, 0.01327, 0.02273]),
        "C_Dv": np.array([0.0052317, 0.0052393, 0.0050567, 0.0026322]),
        "C_M": np.array([-0.19187, -0.19169, -0.18518, -0.172697]),
    },
}

# data['ADflow']['h'] = (1 / data['ADflow']['N']) ** (1/3)

fig, ax = plt.subplots(2, 2)

colors = ["b", "g", "r", "c", "m", "y", "k"]
n = 0
for solver, solver_data in data.items():
    solver_data["h"] = (1 / solver_data["N"]) ** (1 / 3)

    if solver != "ADflow":
        ax[0][0].plot(solver_data["h"], solver_data["C_L"], "o--" + colors[n], label=solver)
        ax[0][1].plot(solver_data["h"], solver_data["C_D"], "o--" + colors[n])
        ax[1][0].plot(solver_data["h"], solver_data["C_M"], "o--" + colors[n], label=solver)
        ax[1][1].plot(solver_data["h"], solver_data["C_Dp"], "v--" + colors[n])
        ax[1][1].plot(solver_data["h"], solver_data["C_Dv"], "s:" + colors[n])
    else:
        ax[0][0].plot(solver_data["h"], solver_data["C_L"], "o-" + colors[n], label=solver)
        ax[0][1].plot(solver_data["h"], solver_data["C_D"], "o-" + colors[n])
        ax[1][0].plot(solver_data["h"], solver_data["C_M"], "o-" + colors[n], label=solver)
        ax[1][1].plot(solver_data["h"], solver_data["C_Dp"], "v-" + colors[n])
        ax[1][1].plot(solver_data["h"], solver_data["C_Dv"], "s-" + colors[n])
    n += 1

ax[1][1].plot(0, 0, "k--", label="Cd pressure")
ax[1][1].plot(0, 0, "k:", label="Cd viscous")

ax[0][0].legend()
ax[0][0].set_xlim((0, 0.025))
ax[0][0].set_ylim((0.255, 0.275))
ax[0][0].set_ylabel("Cl")

ax[0][1].set_xlim((0, 0.025))
ax[0][1].set_ylim((0.016, 0.024))
ax[0][1].set_ylabel("Cd")

ax[1][0].set_xlim((0, 0.025))
ax[1][0].set_ylim((-0.196, -0.18))
ax[1][0].set_ylabel("Cm")

ax[1][1].legend()
ax[1][1].set_xlim((0, 0.025))
ax[1][1].set_ylim((0.0045, 0.016))
ax[1][1].set_ylabel("Cdp & Cdv")

for ix, iy in np.ndindex(ax.shape):
    ax[ix, iy].grid()

plt.show()
