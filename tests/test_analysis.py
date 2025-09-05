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
NPROCS = 8
mpiCmd = ["mpirun", "-n", f"{NPROCS}"]
gridFlag = ["--gridFile", "wing_vol_L2.cgns"]
gridFlagOpt = ["--gridFile", "wing_vol_L3.cgns"]
optimizer = {
    "SLSQP": ["--opt", "SLSQP", "--optOptions", "{'MAXIT': 0}"],
    "SNOPT": ["--opt", "SNOPT", "--optOptions", "{'Major iterations limit': 0}"],
    "IPOPT": ["--opt", "IPOPT", "--optOptions", "{'max_iter': 0}"],
}


class TestWingAnalysis(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(tutorialDir, "aero"))

    def test_geo(self):
        # aero/geometry
        os.chdir("geometry")
        subprocess.check_call(["python", "generate_wing.py"])
        os.chdir("../")

    def test_pyhyp(self):
        # aero/meshing/volume
        os.chdir("meshing/volume")
        cmd = ["python", "run_pyhyp.py"]
        subprocess.check_call(mpiCmd + cmd)
        os.chdir("../../")

    def test_wing_aero(self):
        # aero analysis
        os.chdir("analysis")
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

    def test_ffd(self):
        os.chdir("ffd")
        subprocess.check_call(["python", "simple_ffd.py"])
        # go back to opt dir
        os.chdir(os.path.join(tutorialDir, "opt"))

    def test_ffd_parameterize(self):
        os.chdir("ffd")
        subprocess.check_call(["python", "parametrize.py"])
        os.chdir("../")

    @parameterized.expand(["SLSQP", "SNOPT", "IPOPT"])
    def test_wing_opt(self, optName):
        # Check if anything needs to be skipped based on available optimizers and modules
        if optName == "SNOPT" and not has_SNOPT:
            raise unittest.SkipTest("SNOPT is required for this test")
        shutil.rmtree("output", ignore_errors=True)
        cmd = ["python", "aero_opt.py"]
        subprocess.check_call(mpiCmd + cmd + gridFlagOpt + optimizer[optName])

    @parameterized.expand(["SLSQP", "SNOPT", "IPOPT"])
    @unittest.skipIf(ocsm is None, "pyOCSM is required for this test")
    def test_wing_opt_ESP(self, optName):
        # Check if anything needs to be skipped based on available optimizers and modules
        if optName == "SNOPT" and not has_SNOPT:
            raise unittest.SkipTest("SNOPT is required for this test")
        shutil.rmtree("output_ESP", ignore_errors=True)
        cmd = ["python", "aero_opt_esp.py", "--output", "output_ESP"]
        subprocess.check_call(mpiCmd + cmd + gridFlagOpt + optimizer[optName])

class TestAirfoil(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(tutorialDir, "airfoil"))

    def test_prefoil(self):
        # aero/geometry
        os.chdir("geometry")
        subprocess.check_call(["python", "run_prefoil.py"])
        os.chdir("../")

    def test_pyhyp(self):
        # aero/meshing/volume
        os.chdir("meshing")
        cmd = ["python", "run_pyhyp.py"]
        subprocess.check_call(mpiCmd + cmd)
        os.chdir("../")

    def test_aero(self):
        # aero analysis
        os.chdir("analysis")
        shutil.rmtree("output", ignore_errors=True)
        shutil.rmtree("output_drag_polar", ignore_errors=True)
        cmd = ["python", "aero_run.py"]
        subprocess.check_call(mpiCmd + cmd)
        # drag polar
        cmd = ["python", "aero_run.py", "--task", "polar", "--output", "output_drag_polar"]
        subprocess.check_call(mpiCmd + cmd)

class TestAirfoilOpt(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join(tutorialDir, "airfoilopt"))

    def _prepareDirAndFiles(self, runDir):
        os.chdir(runDir)
        shutil.rmtree("output", ignore_errors=True)

    def test_ffd(self):
        os.chdir("ffd")
        subprocess.check_call(["python", "run_ffd.py"])
        os.chdir("../")

    def test_pyoptsparse(self):
        os.chdir("pyoptsparse")
        subprocess.check_call(["python", "rosenbrock.py"])

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

    def test_pyhyp(self):
        os.chdir("meshing/volume")

        cmd = ["python", "run_pyhyp.py", "--level", "L3"]
        subprocess.check_call(mpiCmd + cmd)

        self.assertTrue(os.path.isfile("collar_vol.cgns"))

    def test_analysis(self):
        # Note: The ulimit command is necessary to prevent segmentation faults due to a small stack
        # when using Intel compiler (see https://github.com/mdolab/MACH-Aero/pull/169)

        mpiCmdStr = " ".join(mpiCmd)
        cmd = f"ulimit -s 65536 && {mpiCmdStr} python aero_run.py"
        subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    unittest.main()
