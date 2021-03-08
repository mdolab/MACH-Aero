import os
import unittest
import subprocess
import shutil

tutorialDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tutorial")  # Path to current folder
try:
    import pyOCSM
except ModuleNotFoundError:
    pyOCSM = None

try:
    from pyoptsparse import SNOPT
except ModuleNotFoundError:
    SNOPT = None


class TestWingAnalysis(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(os.path.join(tutorialDir, "aero"))

    def test(self):
        # aero/geometry
        os.chdir("geometry")
        subprocess.run(["python", "generate_wing.py"], check=True)
        # aero/meshing/volume
        os.chdir("../meshing/volume")
        subprocess.run(["mpirun", "-n", f"{self.NPROCS}", "python", "run_pyhyp.py"], check=True)
        # aero analysis
        os.chdir("../../analysis")
        shutil.rmtree("output", ignore_errors=True)
        shutil.rmtree("output_drag_polar", ignore_errors=True)
        subprocess.run(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"], check=True)
        subprocess.run(
            ["mpirun", "-n", f"{self.NPROCS}", "python", "aero_run.py", "--gridFile", "wing_vol_coarsen.cgns"],
            check=True,
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
            ],
            check=True,
        )


class TestWingOpt(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(os.path.join(tutorialDir, "opt"))
        # Prepare optimization INPUT files
        # first generate FFD grids
        os.chdir("ffd")
        subprocess.run(["python", "simple_ffd.py"], check=True)
        # now copy files
        os.chdir("../aero")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
        # go back to opt dir
        os.chdir(os.path.join(tutorialDir, "opt"))

    def test_ffd_parameterize(self):
        os.chdir("ffd")
        subprocess.run(["python", "parametrize.py"], check=True)

    def test_pyoptsparse(self):
        os.chdir("pyoptsparse")
        subprocess.run(["python", "rosenbrock.py"], check=True)

    @unittest.skipUnless(SNOPT, "SNOPT is required for this test")
    def test_wing_opt_SNOPT(self):
        shutil.rmtree("output", ignore_errors=True)
        subprocess.run(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"], check=True)
        subprocess.run(
            [
                "mpirun",
                "-n",
                f"{self.NPROCS}",
                "python",
                "aero_opt.py",
                "--gridFile",
                "wing_vol_coarsen.cgns",
                "--opt",
                "SNOPT",
                "--optOptions",
                "{'Major iterations limit': 1}",
            ],
            check=True,
        )

    def test_wing_opt_IPOPT(self):
        shutil.rmtree("output", ignore_errors=True)
        subprocess.run(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"], check=True)
        subprocess.run(
            [
                "mpirun",
                "-n",
                f"{self.NPROCS}",
                "python",
                "aero_opt.py",
                "--gridFile",
                "wing_vol_coarsen.cgns",
                "--opt",
                "IPOPT",
                "--optOptions",
                "{'max_iter': 1}",
            ],
            check=True,
        )

    @unittest.skipUnless(pyOCSM and SNOPT, "pyOCSM and SNOPT are required for this test")
    def test_wing_opt_ESP_SNOPT(self):
        shutil.rmtree("output_ESP", ignore_errors=True)
        subprocess.run(
            [
                "mpirun",
                "-n",
                f"{self.NPROCS}",
                "python",
                "aero_opt_esp.py",
                "--output",
                "output_ESP",
                "--gridFile",
                "wing_vol_coarsen.cgns",
                "--opt",
                "SNOPT",
                "--optOptions",
                "{'Major iterations limit': 1}",
            ],
            check=True,
        )


class TestAirfoilOpt(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(os.path.join(tutorialDir, "airfoilopt"))

    @unittest.skipUnless(SNOPT, "SNOPT is required for this test")
    def test(self):
        # mesh
        os.chdir("mesh")
        subprocess.run(["python", "genMesh.py"], check=True)
        # FFD
        os.chdir("../ffd")
        subprocess.run(["python", "genFFD.py"], check=True)
        os.chdir("../singlepoint")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../mesh/n0012.cgns", ".")
        shutil.rmtree("output", ignore_errors=True)
        subprocess.run(
            [
                "mpirun",
                "-n",
                f"{self.NPROCS}",
                "python",
                "airfoil_opt.py",
                "--opt",
                "SNOPT",
                "--optOptions",
                "{'Major iterations limit': 1}",
            ],
            check=True,
        )
        os.chdir("../multipoint")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../mesh/n0012.cgns", ".")
        shutil.rmtree("output", ignore_errors=True)
        subprocess.run(
            [
                "mpirun",
                "-n",
                f"{self.NPROCS}",
                "python",
                "airfoil_multiopt.py",
                "--opt",
                "SNOPT",
                "--optOptions",
                "{'Major iterations limit': 1}",
            ],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()