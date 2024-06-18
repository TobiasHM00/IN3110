"""This is the mane script orchestrating the restructuring and plotting of the content of the pollution_data directory.
"""

# Import necessary packages here
import os
from pathlib import Path
import shutil
from analytic_tools import utilities

from analytic_tools.utilities import (
    display_diagnostics,
    display_directory_tree,
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename
)

from analytic_tools.plotting import (
    plot_pollution_data
)


def restructure_pollution_data(pollution_dir: str | Path, dest_dir: str | Path) -> None:
    """This function searches the tree of pollution_data directory pointed to by pollution_dir for .csv files
        that satisfy the criteria described in the assignment. It then moves a renamed copy of these files to gas-specific
        sub-directories in dest_dir, which will be created based on the gasses present in pollution_data directory.

    Parameters:
        - pollution_dir (str or pathlib.Path) : The absolute path to pollution_data directory
        - dest_dir (str or pathlib.Path) : The absolute path to new directory where gas-specific subdirectories will
                                     be created, which must be pollution_data_restructured/by_gas

    Returns:
    None

    Pseudocode:
    1. Iterate through the contents of `pollution_dir`
    2. Find valid .csv files for gasses ([`[gas_formula].csv` files of correct gas types).
    3. Create/assign new directory to store them under `dest_dir` using `get_dest_dir_from_csv_file`
    4. Assign a new name using `merge_parent_and_basename` and copy the file to the new destination.
       If the file happens already to exist there, it should be overwritten.
    """

    # Do the correct error handling first
    if not isinstance(pollution_dir, (str, Path)):
        raise TypeError("Expected a path-like object, received another type")
    if not Path(pollution_dir).exists():
        raise NotADirectoryError("Expected a path to an existing directory, but did not receive that")
    if not Path(pollution_dir).is_dir():
        raise NotADirectoryError("Expected a path to a direcotry, but did not receive that")
    if not Path(dest_dir).exists():
        raise NotADirectoryError("Expected a path to an existing directory, but did not receive that")
    if not Path(dest_dir).is_dir():
        raise NotADirectoryError("Expected a path to a direcotry, but did not receive that")
            
    # Contents of pollution_data tree
    contents = Path(pollution_dir).rglob('*')
    
    for path in contents:
        if (path.suffix == ".csv" and is_gas_csv(path)):
            dest_path = get_dest_dir_from_csv_file(dest_dir, path)
            file_name = merge_parent_and_basename(path)
            dest_file_path = dest_path / Path(file_name)
            shutil.copy(path, dest_file_path)


def analyze_pollution_data(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data and plot
       the statistics showing emissions of each gas as function of all the corresponding
       sources. The new structure and the plots are saved in a separate directory under work_dir

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the new directories will be created

    Returns:
    None

    Pseudocode:
    - Create pollution_data_restructured in work_dir
    - Populate it with a by_gas subdirectory
    - Make a call to restructure_pollution_data
    - Populate pollution_data_restructured with a subdirectory named figures
    - Make a call to plot_pollution_data
    """
    work_dir = Path(work_dir)
    if not isinstance(work_dir, (str, Path)):
        raise TypeError("Expected a path-like object, but did not receive that")
    if not work_dir.exists():
        raise NotADirectoryError("Expected an existing directory, but did not get that")
    
    # Create pollution_data_restructured in work_dir
    pollution_dir = work_dir / "pollution_data"
    
    results = get_diagnostics(pollution_dir)
    display_diagnostics(pollution_dir, results)
    display_directory_tree(pollution_dir)
    
    # restructured_dir = work_dir + os.sep + "pollution_data_restructured"
    restructured_dir = work_dir / "pollution_data_restructured"
    restructured_dir.mkdir(parents=True, exist_ok=True)
    
    # Populate it with a by_gas sub-folder
    by_gas_dir = restructured_dir / "by_gas"
    by_gas_dir.mkdir(parents=True, exist_ok=True)

    # Make a call to restructure_pollution_data
    restructure_pollution_data(pollution_dir, by_gas_dir)

    # Populate pollution_data_restructured with a sub folder named figures
    figures_dir = restructured_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Make a call to plot_pollution_data
    plot_pollution_data(by_gas_dir, figures_dir)


def analyze_pollution_data_tmp(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data in a temporary directory and create the figures
       showing emissions of each gas as function of all the corresponding
       sources. The new figures are saved in a real directory under work_dir.

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the figures will be saved

    Returns:
    None

    Pseudocode:
    - Create a temporary directory and copy pollution_data directory to it
    - Perform the same operations as in analyze_pollution_data
    - Copy (or directly save) the figures to a directory named `figures` under the original working directory pointed to by `work_dir`
    """  
    
    work_dir = Path(work_dir)
    # error handling
    if not isinstance(work_dir, (str, Path)):
        raise TypeError("Expected a path to a path or str like object, but did not recieve that")
    if not work_dir.exists():
        raise NotADirectoryError("Expected an existing directory, but did not het that")
    
    # create a temp_dir and copy contents of pollution_data into this temp_dir
    temp_dir = work_dir / "temp_analysis"
    pollution_dir = work_dir / "pollution_data"
    shutil.copytree(pollution_dir, temp_dir)
    
    # do the same as in analyze_pollution_data
    restructured_dir = temp_dir / "pollution_data_restructured"
    restructured_dir.mkdir(parents=True, exist_ok=True)
    
    # Populate it with a by_gas sub-folder
    by_gas_dir = restructured_dir / "by_gas"
    by_gas_dir.mkdir(parents=True, exist_ok=True)

    # Make a call to restructure_pollution_data
    restructure_pollution_data(pollution_dir, by_gas_dir)
    
    # create a figures_dir
    figures_dir = work_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    plot_pollution_data(by_gas_dir, figures_dir)
    
    # removing temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"Deleted '{temp_dir}'")
    
    
if __name__ == "__main__":
    work_dir = "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment2/"
    analyze_pollution_data(work_dir)
    analyze_pollution_data_tmp(work_dir)
    utilities.delete_directories([work_dir + os.sep + "figures"])
    utilities.delete_directories([work_dir + os.sep + "pollution_data_restructured"])
