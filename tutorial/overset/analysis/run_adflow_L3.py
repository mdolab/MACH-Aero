# ======================================================================
#         Import modules
# ======================================================================
# rst Imports (beg)
from adflow_util import ADFLOW_UTIL
# rst Imports (end)



# ======================================================================
#         Grid Level
# ======================================================================
# rst Level (beg)
level = 'L3'
# rst Level (end)



# ======================================================================
#         adflow_util options
# ======================================================================
# rst Options (beg)
options = {
    'name': 'ONERA_M6_%s'%(level),
    'surfaceFamilyGroups': {
        'wall': ['near_wing', 'near_tip']
    }
}
# rst Options (end)



# ======================================================================
#         AeroProblem options
# ======================================================================
# rst AeroOptions (beg)
aeroOptions = {
    'alpha': 3.06,

    'mach': 0.8395,
    'reynolds': 11.72e6,
    'reynoldsLength': 0.646,
    'T': 300,

    'xRef': 0.0,
    'areaRef': 0.75750,
    'chordRef': 0.646,
    'evalFuncs': ['cl','cd', 'cmy', 'cdp', 'cdv'],
}
# rst AeroOptions (end)



# ======================================================================
#         Solver options
# ======================================================================
# rst SolverOptions (beg)
solverOptions = {
    # Common Parameters
    'gridFile': 'ONERA_M6_%s.cgns'%(level),
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
    'anksecondordswitchtol': 1e-3,
    'ankcoupledswitchtol': 1e-5, 
    
    # NK
    'useNKSolver':True,
    'nkswitchtol':1e-6,
    
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
# rst SolverOptions (end)



# ======================================================================
#         Run ADflow
# ======================================================================
# rst Run (beg)
au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
# rst Run (end)