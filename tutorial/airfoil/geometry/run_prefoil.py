# rst Import
import numpy as np
from prefoil import airfoil, sampling, utils
import niceplots
import matplotlib.pyplot as plt

# rst ReadCoords
X = utils.readCoordFile("n0012.dat")  # load coords
foil = airfoil.Airfoil(X)  # create airfoil object

# rst PlotIntial
fig1 = foil.plot()
fig1.savefig("NACA0012.pdf")

# rst CreateTE
foil.makeBluntTE(0.995)  # create blunt TE
foil.normalizeChord()  # normalize chord length to 1.0 after cutting airfoil to make blunt TE 

# rst Sampling
numsamppts = 277  # number of sampling points
coords = foil.getSampledPts(numsamppts, spacingFunc=[sampling.cosine]*2, func_args={"m": np.pi}, nTEPts = 15)

# rst Output
foil.writeCoords("n0012_processed", file_format='dat')  # sampled points point cloud
foil.writeCoords("n0012_processed",file_format='plot3d')  # intermediate.xyz for pyHyp meshing

# rst PlotFinal
fig2 = foil.plot()
fig2.savefig("processedNACA0012.pdf")
