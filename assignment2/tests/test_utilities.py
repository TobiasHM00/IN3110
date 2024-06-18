""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path

import pytest

# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)


@pytest.mark.task12
def test_get_diagnostics(example_config):
    """Test functionality of get_diagnostics in utilities module

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
                                     from Figure 1 in assignment2.md

    Returns:
    None
    """
    result = get_diagnostics(example_config)

    # This will count the starting directory as a subdirectory, if I want to change this I would do:
    # assert result["subdirectories"]-1 == 4
    assert result["subdirectories"] == 5
    assert result["files"] == 10
    assert result[".csv files"] == 8
    assert result[".npy files"] == 2
    assert result[".txt files"] == 0
    assert result[".md files"] == 0


@pytest.mark.task12
@pytest.mark.parametrize(
    "exception, dir",
    [
        (NotADirectoryError, "Not_a_real_directory"),
        (TypeError, True)
    ],
)
def test_get_diagnostics_exceptions(exception, dir):
    """Test the error handling of get_diagnostics function

    Parameters:
        exception (concrete exception): The exception to raise
        dir (str or pathlib.Path): The parameter to pass as 'dir' to the function

    Returns:
        None
    """
    try:
        get_diagnostics(dir)
    except exception as e:
        print(f"{exception}: {e}")


@pytest.mark.task22
def test_is_gas_csv():
    """Test functionality of is_gas_csv from utilities module

    Parameters:
        None

    Returns:
        None
    """

    path = "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/pollution_data/by_src"
    assert is_gas_csv(path + "/src_agriculture/CH4.csv") == True
    assert is_gas_csv(path + "/src_industry/CO2.csv") == True
    assert is_gas_csv(path + "/src_airtraffic/N2O.csv") == True
    assert is_gas_csv("CO2.csv") == True
    assert is_gas_csv("SF6.csv") == True


@pytest.mark.task22
@pytest.mark.parametrize(
    "exception, path",
    [
        (ValueError, Path(__file__).parent.absolute()),
        (ValueError, "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/pollution_data/by_src/scr_agriculture/CO4.txt"),
        (ValueError, "SO4.md"),
        (TypeError, 1)
    ],
)
def test_is_gas_csv_exceptions(exception, path):
    """Test the error handling of is_gas_csv function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'path' to function

    Returns:
        None
    """
    
    try:
        is_gas_csv(path)
    except exception as e:
        print(f"{exception}: {e}")

@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    """Test functionality of get_dest_dir_from_csv_file in utilities module.

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
            from Figure 1 in assignment2.md

    Returns:
        None
    """
    
    file_path = "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/pollution_data/by_src/src_agriculture/CO2.csv"
    dest_path = get_dest_dir_from_csv_file(example_config, file_path)
    assert dest_path.is_dir()
    assert dest_path.name == "gas_CO2"

@pytest.mark.task24
@pytest.mark.parametrize(
    "exception, dest_parent, file_path",
    [
        (ValueError, Path(__file__).parent.absolute(), "foo.txt"),
        (TypeError, Path(__file__).parent.absolute(), 1),
        (NotADirectoryError, "Not_a_dir", "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/pollution_data/by_src/src_agriculture/CO2.csv"),
        (TypeError, 1, "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/pollution_data/by_src/src_agriculture/CO2.csv")
    ],
)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    """Test the error handling of get_dest_dir_from_csv_file function

    Parameters:
        exception (concrete exception): The exception to raise
        dest_parent (str or pathlib.Path): The parameter to pass as 'dest_parent' to the function
        file_path (str or pathlib.Path): The parameter to pass as 'file_path' to the function

    Returns:
        None
    """

    try:
        get_dest_dir_from_csv_file(dest_parent, file_path)
    except exception as e:
        print(f"{exception}: {e}")


@pytest.mark.task26
def test_merge_parent_and_basename():
    """Test functionality of merge_parent_and_basename from utilities module

    Parameters:
        None

    Returns:
        None
    """

    path1 = "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/pollution_data/by_src/src_agriculture/CO2.csv"
    path2 = "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/pollution_data/by_src/src_road_traffic/N2O.csv"
    path3 = "some_dir/file.txt"
    
    assert merge_parent_and_basename(path1) == "src_agriculture_CO2.csv"
    assert merge_parent_and_basename(path2) == "src_road_traffic_N2O.csv"
    assert merge_parent_and_basename(path3) == "some_dir_file.txt"
    

@pytest.mark.task26
@pytest.mark.parametrize(
    "exception, path",
    [
        (TypeError, 33),
        (ValueError, "some_file.txt")
    ],
)
def test_merge_parent_and_basename_exceptions(exception, path):
    """Test the error handling of merge_parent_and_basename function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'pass' to the function

    Returns:
        None
    """
    
    try:
        merge_parent_and_basename(path)
    except exception as e:
        print(f"{exception}: {e}")