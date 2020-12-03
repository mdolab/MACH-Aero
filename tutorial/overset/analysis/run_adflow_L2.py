from adflow_util import ADFLOW_UTIL

level = 'L2'

options = {
    'name': 'ONERA_M6_%s'%(level),
}

aeroOptions = {
    'alpha': 3.06,
    'reynolds': 11.72e6,
    'mach': 0.8395,
    'T': 288,
    
    'reynoldsLength': 0.646,
    'xRef': 0.0,
    'areaRef': 0.75750,
    'chordRef': 0.646,
    'evalFuncs': ['cl','cd', 'cmz'],
}

solverOptions = {
    # Common Parameters
    'gridFile': '../mesh/ONERA_M6_%s.cgns'%(level),
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',

    # RK
    'smoother':'runge kutta',
    'rkreset':True,
    'nrkreset':20,
    'CFL':0.8,
    'MGCycle':'sg',
    'nsubiterturb': 5, 
        
    # ANK
    'useanksolver': True,
    'anklinresmax': 0.1,
    'anksecondordswitchtol': 1e-3,
    'ankasmoverlap': 4,
    "outerPreconIts": 3,
    'ankcoupledswitchtol': 1e-5, 
    'ankunsteadylstol': 1.5,
    
    # NK
    'useNKSolver':True,
    'nkswitchtol':1e-7,
    
    # General
    'monitorvariables':['resrho', 'resturb', 'cl','cd'],
    'printIterations': True,
    'writeSurfaceSolution': True,
    'writeVolumeSolution': True,
    'outputsurfacefamily': 'wall',
    'surfacevariables': ['cp','vx', 'vy','vz', 'blank'],
    'volumevariables': ['resrho', 'rmach', 'blank'],
    'nCycles':10000,
    'L2Convergence':1e-12,
}

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()