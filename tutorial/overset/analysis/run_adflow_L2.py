from adflow_util import ADFLOW_UTIL

level = 'L2'

options = {
    'name': 'ONERA_M6_%s'%(level),
    'surfaceFamilyGroups': {
        'wall': {'near_wing', 'near_tip'}
    }
}

aeroOptions = {
    'alpha': 3.06,
    'reynolds': 11.72e6,
    'mach': 0.8395,
    'T': 460,
    'P': 315980,
    
    'reynoldsLength': 0.646,
    'xRef': 0.0,
    'areaRef': 0.75750,
    'chordRef': 0.646,
    'evalFuncs': ['cl','cd', 'cmy', 'cdp', 'cdv'],
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
    'nrkreset':35,
    'CFL':0.8,
    'MGCycle':'sg',
    'nsubiterturb': 5, 
        
    # ANK
    'useanksolver': True,
    'anklinresmax': 0.1,
    'anksecondordswitchtol': 1e-4,
    # 'ankcoupledswitchtol': 1e-5, 
    'ankunsteadylstol': 1.2,

    # CHECK THIS
    'ankphysicallstol': 0.4,
    
    # NK
    'useNKSolver':True,
    'nkswitchtol':1e-8,
    
    # General
    'liftindex': 3,
    'monitorvariables':['resrho', 'resturb', 'cl','cd', 'yplus'],
    'printIterations': True,
    'writeSurfaceSolution': True,
    'writeVolumeSolution': True,
    'outputsurfacefamily': 'wall',
    'zippersurfacefamily': 'wall',
    'surfacevariables': ['cp','vx', 'vy','vz', 'blank'],
    'volumevariables': ['resrho', 'rmach', 'blank'],
    'nCycles':10000,
    'L2Convergence':1e-12,
}

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()