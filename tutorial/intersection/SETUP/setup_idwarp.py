from idwarp import USMesh


def setup(comm, gridFile):
    meshOptions = {"gridFile": gridFile}
    mesh = USMesh(options=meshOptions, comm=comm)
    return mesh
