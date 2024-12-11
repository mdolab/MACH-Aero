import os
import unittest
import subprocess
import shutil
from parameterized import parameterized

tutorialDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tutorial")  # Path to current folder
has_SNOPT = os.environ.get("IMAGE") == "private"
try:
    from pyOCSM import ocsm
except ImportError:
    ocsm = None


# note that this is NOT the testflo directive! We are explicitly calling mpirun ourselves
NPROCS = 2
mpiCmd = ["mpirun", "-n", f"{NPROCS}"]
gridFlag = ["--gridFile", "wing_vol_coarsen.cgns"]
optimizer = {
    "SLSQP": ["--opt", "SLSQP", "--optOptions", "{'MAXIT': 0}"],
    "SNOPT": ["--opt", "SNOPT", "--optOptions", "{'Major iterations limit': 0}"],
    "IPOPT": ["--opt", "IPOPT", "--optOptions", "{'max_iter': 0}"],
}


class TestWingAnalysis(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(tutorialDir, "aero/analysis"))
        if not os.path.isfile("wing_vol_coarsen.cgns"):
            subprocess.check_call(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"])
        os.chdir("../")

    def test(self):
        # aero/geometry
        os.chdir("geometry")
        subprocess.check_call(["python", "generate_wing.py"])
        # aero/meshing/volume
        os.chdir("../meshing/volume")
        cmd = ["python", "run_pyhyp.py"]
        subprocess.check_call(mpiCmd + cmd)
        # aero analysis
        os.chdir("../../analysis")
        shutil.rmtree("output", ignore_errors=True)
        shutil.rmtree("output_drag_polar", ignore_errors=True)
        cmd = ["python", "aero_run.py"]
        subprocess.check_call(mpiCmd + cmd + gridFlag)
        # drag polar
        cmd = ["python", "aero_run.py", "--task", "polar", "--output", "output_drag_polar"]
        subprocess.check_call(mpiCmd + cmd + gridFlag)


class TestWingOpt(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(tutorialDir, "opt"))
        # Prepare optimization INPUT files
        # first generate FFD grids
        os.chdir("ffd")
        subprocess.check_call(["python", "simple_ffd.py"])
        # then coarsen the grid
        os.chdir("../../aero/analysis")
        if not os.path.isfile("wing_vol_coarsen.cgns"):
            subprocess.check_call(["cgns_utils", "coarsen", "wing_vol.cgns", "wing_vol_coarsen.cgns"])
        # go back to opt dir
        os.chdir(os.path.join(tutorialDir, "opt"))

    def test_ffd_parameterize(self):
        os.chdir("ffd")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
        subprocess.check_call(["python", "parametrize.py"])

    def test_pyoptsparse(self):
        os.chdir("pyoptsparse")
        subprocess.check_call(["python", "rosenbrock.py"])

    def _prepareDirAndFiles(self):
        # copy files
        os.chdir("aero")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../../aero/analysis/wing_vol_coarsen.cgns", "wing_vol_coarsen.cgns")

    @parameterized.expand(["SLSQP", "SNOPT", "IPOPT"])
    def test_wing_opt(self, optName):
        # Check if anything needs to be skipped based on available optimizers and modules
        if optName == "SNOPT" and not has_SNOPT:
            raise unittest.SkipTest("SNOPT is required for this test")
        self._prepareDirAndFiles()
        shutil.rmtree("output", ignore_errors=True)
        cmd = ["python", "aero_opt.py"]
        subprocess.check_call(mpiCmd + cmd + gridFlag + optimizer[optName])

    @parameterized.expand(["SLSQP", "SNOPT", "IPOPT"])
    @unittest.skipIf(ocsm is None, "pyOCSM is required for this test")
    def test_wing_opt_ESP(self, optName):
        # Check if anything needs to be skipped based on available optimizers and modules
        if optName == "SNOPT" and not has_SNOPT:
            raise unittest.SkipTest("SNOPT is required for this test")
        self._prepareDirAndFiles()
        shutil.rmtree("output_ESP", ignore_errors=True)
        cmd = ["python", "aero_opt_esp.py", "--output", "output_ESP"]
        subprocess.check_call(mpiCmd + cmd + gridFlag + optimizer[optName])


class TestAirfoilOpt(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(tutorialDir, "airfoilopt"))
        # mesh
        os.chdir("mesh")
        subprocess.check_call(["python", "genMesh.py"])
        # FFD
        os.chdir("../ffd")
        shutil.copy("../mesh/n0012.dat", ".")
        subprocess.check_call(["python", "genFFD.py"])
        os.chdir("../")

    def _prepareDirAndFiles(self, runDir):
        os.chdir(runDir)
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../mesh/n0012.cgns", ".")
        shutil.rmtree("output", ignore_errors=True)

    @parameterized.expand(["SLSQP", "SNOPT"])
    def test_single_point(self, optName):
        if optName == "SNOPT" and not has_SNOPT:
            raise unittest.SkipTest("SNOPT is required for this test")
        self._prepareDirAndFiles("singlepoint")
        cmd = ["python", "airfoil_opt.py"]
        subprocess.check_call(mpiCmd + cmd + optimizer[optName])

    @parameterized.expand(["SLSQP", "SNOPT"])
    def test_multipoint(self, optName):
        if optName == "SNOPT" and not has_SNOPT:
            raise unittest.SkipTest("SNOPT is required for this test")
        self._prepareDirAndFiles("multipoint")
        cmd = ["python", "airfoil_multiopt.py"]
        subprocess.check_call(mpiCmd + cmd + optimizer[optName])


class TestOverset(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(tutorialDir, "overset"))

    def test_pyhyp(self):
        os.chdir("mesh")
        cmd = ["python", "run_pyhyp.py", "--level", "L3"]
        subprocess.check_call(mpiCmd + cmd)

        # now we test the ihc check script
        cmd = ["python", "ihc_check.py", "--level", "L3"]
        subprocess.check_call(cmd)
        self.assertTrue(os.path.isfile("ONERA_M6_L3_IHC.cgns"))

    def test_analysis(self):
        os.chdir("analysis")
        cmd = ["python", "run_adflow_L3.py"]
        subprocess.check_call(mpiCmd + cmd)


class TestIntersect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.join(tutorialDir, "intersection"))

        cmd = ["./get-input-files.sh"]
        subprocess.check_call(cmd)

        cmd = ["ulimit", "-s", "65536"]
        subprocess.check_call(cmd)

    def test_pyhyp(self):
        os.chdir("meshing/volume")

        cmd = ["python", "run_pyhyp.py", "--level", "L3"]
        subprocess.check_call(mpiCmd + cmd)

        self.assertTrue(os.path.isfile("collar_vol.cgns"))

    def test_analysis(self):
        cmd = ["python", "aero_run.py"]
        subprocess.check_call(mpiCmd + cmd)


if __name__ == "__main__":
    unittest.main()
