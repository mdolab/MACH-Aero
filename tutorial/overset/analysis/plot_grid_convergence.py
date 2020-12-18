import numpy as np
import matplotlib.pyplot as plt

# Data from: https://turbmodels.larc.nasa.gov/Onerawingnumerics_val/SA/combined_forces_pitchmom_maxmut.dat

data = {
    'ADflow': {
        'N': np.array([153473, 1277538, 10476201]),
        'C_L': np.array([0.26064807, 0.26815573, 0.27054311]),
        'C_D': np.array([0.01879813, 0.01703536, 0.01699923]),
        'C_Dp': np.array([0.01326940, 0.01180256, 0.01177125]),
        'C_Dv': np.array([0.00552873, 0.00523279, 0.00522798]),
        'C_M': np.array([-0.18639411, -0.19025530, -0.19248581])
    },
    'USM3D, Prism_Hex': {
        'N': np.array([69206016, 8650752, 1081344, 135168]),
        'h': np.array([2.44E-03, 4.87E-03, 9.74E-03, 1.95E-02]),
        'C_L': np.array([2.69E-01, 2.67E-01, 2.67E-01, 2.61E-01]),
        'C_D': np.array([1.70E-02, 1.70E-02, 1.77E-02, 2.13E-02]),
        'C_Dp': np.array([1.17E-02, 1.17E-02, 1.22E-02, 1.51E-02]),
        'C_Dv': np.array([5.30E-03, 5.33E-03, 5.55E-03, 6.18E-03]),
        'C_M': np.array([-1.90E-01, -1.88E-01, -1.88E-01, -1.85E-01])
    },
    'USM3D, Tetrahedral': {
        'N': np.array([363331584, 45416448, 5677056, 709632, 88704]),
        'h': np.array([1.40E-03, 2.80E-03, 5.61E-03, 1.12E-02, 2.24E-02]),
        'C_L': np.array([2.71E-01, 2.69E-01, 2.67E-01, 2.64E-01, 2.50E-01]),
        'C_D': np.array([1.70E-02, 1.71E-02, 1.74E-02, 1.90E-02, 2.64E-02]),
        'C_Dp': np.array([1.17E-02, 1.18E-02, 1.21E-02, 1.37E-02, 2.11E-02]),
        'C_Dv': np.array([5.31E-03, 5.28E-03, 5.28E-03, 5.37E-03, 5.25E-03]),
        'C_M': np.array([-1.91E-01, -1.90E-01, -1.88E-01, -1.85E-01, -1.75E-01])
    },
    'FUN3D-FV': {
        'N': np.array([60777345, 7625153, 960225, 121841, 15705, 2093, 300]),
        'h': np.array([2.54E-03, 5.08E-03, 1.01E-02, 2.02E-02, 3.99E-02, 7.82E-02, 0.149380158]),
        'C_L': np.array([0.269545512, 0.267878736, 0.265852518, 0.258628725, 0.248903715, 0.228937233, 0.185943039]),
        'C_D': np.array([1.69E-02, 1.69E-02, 1.72E-02, 2.01E-02, 3.22E-02, 5.30E-02, 7.79E-02]),
        'C_Dp': np.array([1.17E-02, 1.16E-02, 1.18E-02, 1.39E-02, 2.40E-02, 4.01E-02, 6.19E-02]),
        'C_Dv': np.array([5.28E-03, 5.29E-03, 5.41E-03, 6.17E-03, 8.21E-03, 1.29E-02, 1.60E-02]),
        'C_M': np.array([-0.190665241, -0.188882665, -0.186834678, -0.181220113, -0.183886843, -0.191312751, -0.183210354])
    },
    'CFL3D': {
        'N': np.array([69206016, 69206016, 8650752, 1081344, 135168]),
        'h': np.array([2.44E-03, 2.44E-03, 4.87E-03, 9.74E-03, 1.95E-02]),
        'C_L': np.array([2.69E-01, 2.69E-01, 2.66E-01, 2.66E-01, 2.61E-01]),
        'C_D': np.array([1.70E-02, 1.70E-02, 1.69E-02, 1.74E-02, 1.90E-02]),
        'C_Dp': np.array([1.17E-02, 1.17E-02, 1.16E-02, 1.18E-02, 1.28E-02]),
        'C_Dv': np.array([5.30E-03, 5.30E-03, 5.32E-03, 5.54E-03, 6.21E-03]),
        'C_M': np.array([-1.90E-01, -1.90E-01, -1.87E-01, -1.87E-01, -1.84E-01])
    },
    'FUN3D-FE': {
        'N': np.array([7625153, 960225, 121841, 15705]),
        'h': np.array([5.08E-03, 1.01E-02, 2.02E-02, 3.99E-02]),
        'C_L': np.array([0.271195, 0.270826, 0.263215, 0.244181]),
        'C_D': np.array([0.016979, 0.017088, 0.01833, 0.025362]),
        'C_Dp': np.array([0.011747, 0.011849, 0.01327, 0.02273]),
        'C_Dv': np.array([0.0052317, 0.0052393, 0.0050567, 0.0026322]),
        'C_M': np.array([-0.19187, -0.19169, -0.18518, -0.172697])
    }
}

# data['ADflow']['h'] = (1 / data['ADflow']['N']) ** (1/3)

fig, ax = plt.subplots(2, 2)

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
n = 0
for solver, solver_data in data.items():
    solver_data['h'] = (1 / solver_data['N']) ** (1/3)
    
    if solver != 'ADflow':
        ax[0][0].plot(solver_data['h'], solver_data['C_L'], 'o--' + colors[n], label=solver)
        ax[0][1].plot(solver_data['h'], solver_data['C_D'], 'o--' + colors[n])
        ax[1][0].plot(solver_data['h'], solver_data['C_M'], 'o--' + colors[n], label=solver)
        ax[1][1].plot(solver_data['h'], solver_data['C_Dp'], 'v--' + colors[n])
        ax[1][1].plot(solver_data['h'], solver_data['C_Dv'], 's:' + colors[n])
    else:
        ax[0][0].plot(solver_data['h'], solver_data['C_L'], 'o-' + colors[n], label=solver)
        ax[0][1].plot(solver_data['h'], solver_data['C_D'], 'o-' + colors[n])
        ax[1][0].plot(solver_data['h'], solver_data['C_M'], 'o-' + colors[n], label=solver)
        ax[1][1].plot(solver_data['h'], solver_data['C_Dp'], 'v-' + colors[n])
        ax[1][1].plot(solver_data['h'], solver_data['C_Dv'], 's-' + colors[n])
    n += 1

ax[1][1].plot(0, 0, 'k--', label='Cd pressure')
ax[1][1].plot(0, 0, 'k:', label='Cd viscous')

ax[0][0].legend()
ax[0][0].set_xlim((0, 0.025))
ax[0][0].set_ylim((0.255, 0.275))
ax[0][0].set_ylabel('Cl')

ax[0][1].set_xlim((0, 0.025))
ax[0][1].set_ylim((0.016, 0.024))
ax[0][1].set_ylabel('Cd')

ax[1][0].set_xlim((0, 0.025))
ax[1][0].set_ylim((-0.196, -0.18))
ax[1][0].set_ylabel('Cm')

ax[1][1].legend()
ax[1][1].set_xlim((0, 0.025))
ax[1][1].set_ylim((0.0045, 0.016))
ax[1][1].set_ylabel('Cdp & Cdv')

for ix, iy in np.ndindex(ax.shape):
    ax[ix, iy].grid()



plt.show()