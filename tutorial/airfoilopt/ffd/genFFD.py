# this script is used to generate x-uniform FFD boxes for a given airfoil

# rst Import
import numpy as np

# rst Load
airfoil = np.loadtxt("n0012.dat")
npts = airfoil.shape[0]
nmid = (npts + 1) // 2


# rst UpperLower
def getupper(xtemp):
    myairfoil = np.ones(npts)
    for i in range(nmid):
        myairfoil[i] = abs(airfoil[i, 0] - xtemp)
    myi = np.argmin(myairfoil)
    return airfoil[myi, 1]


def getlower(xtemp):
    myairfoil = np.ones(npts)
    for i in range(nmid, npts):
        myairfoil[i] = abs(airfoil[i, 0] - xtemp)
    myi = np.argmin(myairfoil)
    return airfoil[myi, 1]


# rst FFDBox1
nffd = 10

FFDbox = np.zeros((nffd, 2, 2, 3))

xslice = np.zeros(nffd)
yupper = np.zeros(nffd)
ylower = np.zeros(nffd)

xmargin = 0.001
ymargin1 = 0.02
ymargin2 = 0.005

for i in range(nffd):
    xtemp = i * 1.0 / (nffd - 1.0)
    xslice[i] = -1.0 * xmargin + (1 + 2.0 * xmargin) * xtemp
    ymargin = ymargin1 + (ymargin2 - ymargin1) * xslice[i]
    yupper[i] = getupper(xslice[i]) + ymargin
    ylower[i] = getlower(xslice[i]) - ymargin

# rst FFDBox2
# X
FFDbox[:, 0, 0, 0] = xslice[:].copy()
FFDbox[:, 1, 0, 0] = xslice[:].copy()
# Y
# lower
FFDbox[:, 0, 0, 1] = ylower[:].copy()
# upper
FFDbox[:, 1, 0, 1] = yupper[:].copy()
# copy
FFDbox[:, :, 1, :] = FFDbox[:, :, 0, :].copy()
# Z
FFDbox[:, :, 0, 2] = 0.0
# Z
FFDbox[:, :, 1, 2] = 1.0

# rst WriteFile
with open("ffd.xyz", "w") as f:
    f.write("1\n")
    f.write(str(nffd) + " 2 2\n")
    for ell in range(3):
        for k in range(2):
            for j in range(2):
                for i in range(nffd):
                    f.write("%.15f " % (FFDbox[i, j, k, ell]))
                f.write("\n")
