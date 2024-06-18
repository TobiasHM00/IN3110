from pathlib import Path

import pytest
from analyze_pollution_data import (
    analyze_pollution_data,
    analyze_pollution_data_tmp,
    restructure_pollution_data,
)


@pytest.mark.task31
def test_restructure_pollution_data(tmp_workdir: Path):
    """Test restructure_pollution_data_function
    Parameters:
        - tmp_workdir (pathlib.Path): path to temporary directory with pollution_data in it
    Returns:
        - None
    """

    pollution_data = tmp_workdir / "pollution_data"
    by_gas = tmp_workdir / "pollution_data_restructured" / "by_gas"
    by_gas.mkdir(parents=True, exist_ok=True)

    restructure_pollution_data(pollution_data, by_gas)

    # Check by_gas_dir
    possible_gas_dirs = [
        by_gas / "gas_CO2",
        by_gas / "gas_CH4",
        by_gas / "gas_N2O",
        by_gas / "gas_H2",
        by_gas / "gas_SF6",
    ]
    # Check the contents of by_gas
    actual_gas_dirs = list(by_gas.iterdir())
    # Check that these subdirectories are non-empty
    assert (
        actual_gas_dirs
    ), "pollution_data_restructured/by_gas is empty but should not be"
    for p in actual_gas_dirs:
        # By gas must only contain correctly named directories
        assert (
            p in possible_gas_dirs
        ), f"{p} is an invalid subdirectory in pollution_data_restructured/by_gas "


@pytest.mark.task32
def test_analyze_pollution_data(tmp_workdir: Path):
    """Test analyze_pollution_data function

    Parameters:
        - tmp_workdir (pathlib.Path): path to temporary directory with pollution_data in it
    Returns:
        - None
    """
    analyze_pollution_data(tmp_workdir)

    # Check if pollution_data_restructured exists
    pollution_data_restructured = tmp_workdir / "pollution_data_restructured"
    assert (
        pollution_data_restructured.exists()
    ), "analyze_pollution_data did not create pollution_data_restructured"

    # Check if it's subdirectories exist
    by_gas = pollution_data_restructured / "by_gas"
    figures = pollution_data_restructured / "figures"
    assert (
        by_gas.exists()
    ), "analyze_pollution_data did not create pollution_data_restructured/by_gas"
    assert (
        figures.exists()
    ), "analyze_pollution_data did not create pollution_data_restructured/figures"

    # Check by_gas_dir
    possible_gas_dirs = [
        by_gas / "gas_CO2",
        by_gas / "gas_CH4",
        by_gas / "gas_N2O",
        by_gas / "gas_H2",
        by_gas / "gas_SF6",
    ]
    # Check the contents of by_gas
    actual_gas_dirs = list(by_gas.iterdir())
    # Check that these subdirectories are non-empty
    assert (
        actual_gas_dirs
    ), "pollution_data_restructured/by_gas is empty but should not be"
    for p in actual_gas_dirs:
        # By gas must only contain correctly named directories
        assert (
            p in possible_gas_dirs
        ), f"{p} is an invalid subdirectory in pollution_data_restructured/by_gas "

    # Finally, check if figures dir
    possible_files = [
        figures / "gas_CO2.png",
        figures / "gas_CH4.png",
        figures / "gas_N2O.png",
        figures / "gas_H2.png",
        figures / "gas_SF6.png",
    ]
    actual_figures = list(figures.iterdir())
    assert (
        actual_figures
    ), "pollution_data_restructured/figures is empty but should not be"
    for p in actual_figures:
        # Figures must only contain correctly named directories
        assert (
            p in possible_files
        ), f"{p} is an invalid file in pollution_data_restructured/figures"


@pytest.mark.task33
def test_analyze_pollution_data_tmp(tmp_workdir: Path):
    """Test analyze_pollution_data_tmp function

    Parameters:
        - tmp_workdir (pathlib.Path): path to temporary directory with pollution_data in it
    Returns:
        - None
    """
    try:
        analyze_pollution_data_tmp(tmp_workdir)
    except NotImplementedError as e:
        # Skip this test if the task was not implemented
        pytest.skip("Task 3.3 is not implemented")

    # Check if figures exists
    figures = tmp_workdir / "figures"
    assert (
        figures.exists()
    ), "analyze_pollution_data_tmp did not create figures directory"

    # Check that figures contains correct type of files
    possible_files = [
        figures / "gas_CO2.png",
        figures / "gas_CH4.png",
        figures / "gas_N2O.png",
        figures / "gas_H2.png",
        figures / "gas_SF6.png",
    ]
    actual_figures = list(figures.iterdir())
    assert actual_figures, "figures is empty but should not be"
    for p in actual_figures:
        # Figures must only contain correctly named directories
        assert p in possible_files, f"{p} is an invalid file in figures"
