import os
import unittest
import subprocess
import shutil

tutorialDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tutorial")  # Path to current folder


class TestWingAnalysis(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(os.path.join(tutorialDir, "aero"))

    def test(self):
        # aero/geometry
        os.chdir("geometry")
        subprocess.run(["python", "generate_wing.py"])
        # aero/meshing/volume
        os.chdir("../meshing/volume")
        subprocess.run(["mpirun", "-n", f"{self.NPROCS}", "python", "run_pyhyp.py"])
        # aero analysis
        os.chdir("../../analysis")
        subprocess.run(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"])
        subprocess.run(
            ["mpirun", "-n", f"{self.NPROCS}", "python", "aero_run.py", "--gridFile", "wing_vol_coarsen.cgns"]
        )
        # drag polar
        subprocess.run(
            [
                "mpirun",
                "-n",
                f"{self.NPROCS}",
                "python",
                "aero_run_drag_polar.py",
                "--gridFile",
                "wing_vol_coarsen.cgns",
            ]
        )


class TestWingOpt(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(os.path.join(tutorialDir, "opt"))

    def test_pyoptsparse(self):
        os.chdir("pyoptsparse")
        subprocess.run(["python", "rosenbrock.py"])

    def test_wing_opt(self):
        # first generate FFD grids
        os.chdir("ffd")
        subprocess.run(["python", "simple_ffd.py"])
        subprocess.run(["python", "parametrize.py"])
        # now run opt
        os.chdir("../aero")
        shutil.rmtree("output", ignore_errors=True)
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
        shutil.rmtree("output")
        shutil.rmtree("output_drag_polar")
        subprocess.run(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"])
        subprocess.run(
            ["mpirun", "-n", f"{self.NPROCS}", "python", "aero_opt.py", "--gridFile", "wing_vol_coarsen.cgns"]
        )


class TestAirfoilOpt(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(os.path.join(tutorialDir, "airfoilopt"))
        # mesh
        os.chdir("mesh")
        subprocess.run(["python", "genMesh.py"])
        # FFD
        os.chdir("../ffd")
        subprocess.run(["python", "genFFD.py"])
        os.chdir("../")

    def test_singlepoint(self):
        os.chdir("singlepoint")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../mesh/n0012.cgns", ".")
        shutil.rmtree("output")
        subprocess.run(["mpirun", "-n", f"{self.NPROCS}", "python", "airfoil_opt.py"])

    def test_multipoint(self):
        os.chdir("multipoint")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../mesh/n0012.cgns", ".")
        shutil.rmtree("output")
        subprocess.run(["mpirun", "-n", f"{self.NPROCS}", "python", "airfoil_multiopt.py"])


if __name__ == "__main__":
    unittest.main()
