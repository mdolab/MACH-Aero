# IMPORTS
import os
import sys
from collections import OrderedDict
from mpi4py import MPI
from pyhyp import pyHypMulti
from cgnsutilities.cgnsutilities import *
import argparse
import numpy

rank = MPI.COMM_WORLD.rank

parser=argparse.ArgumentParser()
parser.add_argument('--input_dir', default = '.')
parser.add_argument('--output_dir', default = '.')
parser.add_argument('--level', default='L1')
args = parser.parse_args()

# reference first off wall spacing for L2 level meshes
s0 = 1.0e-6

# background mesh spacing
dhStar = {
    'L3': 0.15,
    'L2': 0.125,
    'L1': 0.075,
}[args.level]

# factor for spacings
levelFact = {
    'L3':0.5,
    'L2':1.0,
    'L1':2.0,
}
fact = levelFact[args.level]



# levels of coarsening for the surface meshes
levelCoarsen = {
                'L1':   1,
                'L2':   2,
                'L3':   3}
coarsen = levelCoarsen[args.level]

levelNGrid = {
    'L3': 31,
    'L2': 61,
    'L1': 121,
}
nGrid = levelNGrid[args.level]



# pyHypMulti options
commonOptions = {

    # ---------------------------
    #        Input Parameters
    # ---------------------------
    'unattachedEdgesAreSymmetry':False,
    'outerFaceBC':'overset',
    'autoConnect':True,
    'fileType':'cgns',
    'families':'wall',
    # ---------------------------
    #        Grid Parameters
    # ---------------------------
    'N': nGrid, 
    's0':s0/fact,
    'marchDist':2.5*0.8,
    'splay':0.025,

    # 'nConstantEnd':3,
    # 'splay': .2,
    # 'cornerAngle':75.0,
    'coarsen':coarsen,
    # ---------------------------
    #   Pseudo Grid Parameters
    # ---------------------------
    'ps0':-1,
    'pGridRatio':-1,
    'cMax': 1.0,

    # ---------------------------
    #   Smoothing parameters
    # ---------------------------
    'epsE': 1.0,
    'epsI': 2.0,
    'theta': 1.0,
    'volCoef': .5,
    'volBlend': 0.00001,
    'volSmoothIter': int(100*fact),
    # 'kspreltol':1e-8,
}

# Set individual options
options = OrderedDict()

wing_dict = {
    'inputFile': '%s/wing.cgns'%(args.input_dir),
    'outputFile': '%s/wing_vol_%s.cgns'%(args.output_dir, args.level),
    'BC':{
        3:{'jLow':'ySymm'},
        4:{'jLow':'ySymm'},
        9:{'jLow':'ySymm'}
    },
    'splay':0.5,
}

tip_dict = {
    'inputFile': '%s/tip.cgns'%(args.input_dir),
    'outputFile': '%s/tip_vol_%s.cgns'%(args.output_dir, args.level),
}


# figure out what grids we will generate again
options['wing'] = wing_dict
options['tip'] = tip_dict

# Run pyHypMulti
hyp = pyHypMulti(options=options, commonOptions=commonOptions)
MPI.COMM_WORLD.barrier()

# quit()

# combine
wing =  '%s/wing_vol_%s.cgns'%(args.output_dir, args.level )
tip =   '%s/tip_vol_%s.cgns'%(args.output_dir, args.level)


wingGrid     = readGrid(wing)
tipGrid = readGrid(tip)


gridList = [wingGrid, tipGrid]

# combine grids
combinedGrid = combineGrids(gridList)

# move to y=0
combinedGrid.symmZero('y')

# create a background mesh
farfield = '%s/farfield_%s.cgns'%(args.output_dir, args.level)

nFarfield = {
    'L3': 13,
    'L2': 25,
    'L1': 49,
}[args.level]


combinedGrid.simpleOCart(dhStar, 100., nFarfield, 'y', 1, farfield)

# we can do the stuff in one proc after this point
if rank == 0:

    farfieldGrid = readGrid(farfield)
    gridList.append(farfieldGrid)
    finalGrid = combineGrids(gridList)

    # write the final file
    finalGrid.writeToCGNS('%s/wing_final_%s.cgns'%(args.output_dir, args.level))

quit()
