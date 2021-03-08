import os
import unittest
import subprocess
import shutil

tutorialDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tutorial")  # Path to current folder


def _import_test(import_cmd):
    try:
        # have to test import via subprocess because otherwise we inadvertently import mpi4py
        # which will cause an obscure subprocess error
        subprocess.run(["python", "-c", import_cmd], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


has_SNOPT = _import_test("from pyoptsparse import SNOPT")
has_ESP = _import_test("import pyOCSM")


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
        # go back to opt dir
        os.chdir(os.path.join(tutorialDir, "opt"))

    def test_ffd_parameterize(self):
        os.chdir("ffd")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
        subprocess.run(["python", "parametrize.py"], check=True)

    def test_pyoptsparse(self):
        os.chdir("pyoptsparse")
        subprocess.run(["python", "rosenbrock.py"], check=True)

    @unittest.skipUnless(has_SNOPT, "SNOPT is required for this test")
    def test_wing_opt_SNOPT(self):
        # first copy files
        os.chdir("aero")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
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
                "{'Major iterations limit': 0}",
            ],
            check=True,
        )

    def test_wing_opt_IPOPT(self):
        # first copy files
        os.chdir("aero")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
        shutil.rmtree("output_IPOPT", ignore_errors=True)
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
                "--output",
                "output_IPOPT" "--optOptions",
                "{'max_iter': 0}",
            ],
            check=True,
        )

    @unittest.skipUnless(has_ESP and has_SNOPT, "pyOCSM and SNOPT are required for this test")
    def test_wing_opt_ESP_SNOPT(self):
        # first copy files
        os.chdir("aero")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
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
                "{'Major iterations limit': 0}",
            ],
            check=True,
        )

    @unittest.skipUnless(has_ESP, "pyOCSM is required for this test")
    def test_wing_opt_ESP_IPOPT(self):
        # first copy files
        os.chdir("aero")
        shutil.copy("../ffd/ffd.xyz", ".")
        shutil.copy("../../aero/analysis/wing_vol.cgns", "wing_vol.cgns")
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
                "IPOPT",
                "--optOptions",
                "{'max_iter': 0}",
            ],
            check=True,
        )


class TestAirfoilOpt(unittest.TestCase):
    def setUp(self):
        # note that this is NOT the testflo directive!
        # we are explicitly calling mpirun ourselves
        self.NPROCS = 2
        os.chdir(os.path.join(tutorialDir, "airfoilopt"))
        # mesh
        os.chdir("mesh")
        subprocess.run(["python", "genMesh.py"], check=True)
        # FFD
        os.chdir("../ffd")
        subprocess.run(["python", "genFFD.py"], check=True)
        os.chdir("../")

    @unittest.skipUnless(has_SNOPT, "SNOPT is required for this test")
    def test_single_point(self):
        os.chdir("singlepoint")
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
                "{'Major iterations limit': 0}",
            ],
            check=True,
        )

    def test_multipoint(self):
        os.chdir("multipoint")
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
                "{'Major iterations limit': 0}",
            ],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
