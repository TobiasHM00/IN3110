"""Script containing the custom pytest fixture, imported automatically by pytest during execution 
"""

import os
import shutil
import sys
from pathlib import Path

from pytest import fixture

# Add assignment2 to path
sys.path.insert(0, str(Path(__file__).parents[1].resolve()))


def pytest_configure(config):
    # register our markers to avoid warnings
    config.addinivalue_line("markers", "task12: run tests associated with task 1.2")
    config.addinivalue_line("markers", "task22: run tests associated with task 2.2")
    config.addinivalue_line("markers", "task24: run tests associated with task 2.4")
    config.addinivalue_line("markers", "task26: run tests associated with task 2.6")
    config.addinivalue_line("markers", "task31: run tests associated with task 3.1")
    config.addinivalue_line("markers", "task32: run tests associated with task 3.2")
    config.addinivalue_line("markers", "task33: run tests associated with task 3.3")


@fixture
def example_config(tmp_path):
    """Custom pytest fixture that contains the example configuration referred to in Figure 1 of the
        assignment description.

    Parameters:
    tmp_path (pathlib.Path): fixture which will provide a temporary directory unique
                             to the test invocation, created in the base temporary directory.
    """
    by_src_dir = tmp_path / "pollution_data" / "by_src"
    by_src_dir.mkdir(parents=True, exist_ok=True)

    # create the structure from the example in assignment
    argriculture_dir = by_src_dir / "src_agriculture"
    argriculture_dir.mkdir(exist_ok=True)
    (argriculture_dir / "N2O_455.npy").touch()
    (argriculture_dir / "H2.csv").touch()
    (argriculture_dir / "H2_mkL.csv").touch()

    airtraffic_dir = by_src_dir / "src_airtraffic"
    airtraffic_dir.mkdir(exist_ok=True)
    (airtraffic_dir / "CO2.csv").touch()
    (airtraffic_dir / "CO2_GHk.csv").touch()
    (airtraffic_dir / "CH4_327.npy").touch()

    oil_and_gass_dir = by_src_dir / "src_oil_and_gass"
    oil_and_gass_dir.mkdir(exist_ok=True)
    (oil_and_gass_dir / "CH4.csv").touch()
    (oil_and_gass_dir / "SF6_Hgt.csv").touch()
    (oil_and_gass_dir / "H2O.csv").touch()
    (oil_and_gass_dir / "CO2.csv").touch()

    save_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(save_cwd)


@fixture
def tmp_workdir(tmp_path):
    """Custom pytest fixture that contains an exact copy of the pollution_data, retrieved from assignment2
    Used to check if the student has implemented functions within analyze_pollution_data.py correctly.
    """
    tmp_pollution_data = tmp_path / "pollution_data"
    tmp_pollution_data.mkdir(exist_ok=True)
    real_workdir = Path(__file__).parents[1].resolve()

    shutil.copytree(
        real_workdir / "pollution_data", tmp_pollution_data, dirs_exist_ok=True
    )
    save_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(save_cwd)
