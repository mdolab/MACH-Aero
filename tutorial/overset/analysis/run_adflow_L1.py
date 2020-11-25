from __future__ import print_function
import numpy
from adflow import ADFLOW
from baseclasses import *
from mpi4py import MPI

level = 'L1'
alpha = 3.06       
reynolds = 11.72e6 

T = 288.15
mach = 0.8395 


aeroOptions = {
    # Common Parameters
    'gridFile': '../mesh/wing_final_{}.cgns'.format(level),
    'outputDirectory':'output',
    'zippersurfacefamily': 'overset',
    

    # Physics Parameters
    'equationType':'RANS',

    # RK
    'smoother':'runge kutta',
    'rkreset':True,
    'nrkreset':100,
    'CFL':0.8,
    'MGCycle':'sg',
        
    # ANK
    'useanksolver' : True,
    'ankuseturbdadi': False,

    
    # NK
    'useNKSolver':True,
    'nkswitchtol':1e-8,

    
    # General
    'monitorvariables':['resrho', 'resturb', 'cl','cd'],
    'printIterations': True,
    'writeSurfaceSolution': True,
    'writeVolumeSolution': True,
    'outputsurfacefamily': 'wall',
    'surfacevariables': ['cp','vx', 'vy','vz', 'mach', 'blank'],
    'volumevariables': ['resrho', 'blank'],
    'liftIndex':3,
    'nCycles':20000,
    'L2Convergence':1e-14,
}


# Create solver
CFDSolver = ADFLOW(options=aeroOptions)

# Add features
#CFDSolver.addLiftDistribution(150, 'z')
#CFDSolver.addSlices('z', numpy.linspace(0.1, 14, 10))

name = 'Re{}_M{}_AoA{}_{}'.format(reynolds, mach, alpha, level)
ap = AeroProblem(name=name, alpha=alpha, mach=mach, reynolds=reynolds,
                 reynoldsLength=0.64607, T=T, areaRef=0.75296, chordRef=0.64607,
                 evalFuncs=['cl','cd', 'cmz'])


# Solve the flow
CFDSolver(ap)

# Evaluate functions
funcs = {}
CFDSolver.evalFunctions(ap, funcs)


if MPI.COMM_WORLD.rank == 0:
    print("CL: {}, CD: {}, CM: {}".format(
        funcs[name+'_cl'], funcs[name+'_cd'], -funcs[name+'_cmz']
    ))