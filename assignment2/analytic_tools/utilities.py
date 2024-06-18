"""Module containing functions used to achieve the desired restructuring of the pollution_data directory
"""
# Include the necessary packages here
import os
from pathlib import Path
import shutil
from typing import Dict, List


def get_diagnostics(dir: str | Path) -> Dict[str, int]:
    """Get diagnostics for the directory tree, with root directory pointed to by dir.
       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md and other files in the whole directory tree.

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest

    Returns:
        res (Dict[str, int]) : a dictionary of the findings with following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    """
    
    # Dictionary to return
    res = {
        "files": 0,
        "subdirectories": 0,
        ".csv files": 0,
        ".txt files": 0,
        ".npy files": 0,
        ".md files": 0,
        "other files": 0,
    }

    # Remember error handling
    if not isinstance(dir, (str, Path)):
        raise TypeError("Expected a path or str but received another type")
    if not Path(dir).is_dir():
        raise NotADirectoryError("Input must be a path to a directory")
    if not Path(dir).exists():
        raise NotADirectoryError("This directory path does not exists")

    # Traverse the directory and find its contents
    contents = Path(dir).rglob("*")

    # Count folders and total num. of files
    for path in contents:
        if path.is_file():
            res["files"] += 1
            suffix = path.suffix.lower()
            if suffix == ".csv":
                res[".csv files"] += 1
            elif suffix == ".txt":
                res[".txt files"] += 1
            elif suffix == ".npy":
                res[".npy files"] += 1
            elif suffix == ".md":
                res[".md files"] += 1
            else:
                res["other files"] += 1
        elif path != dir:
            res["subdirectories"] += 1

    return res


def display_diagnostics(dir: str | Path, contents: Dict[str, int]) -> None:
    """Display diagnostics for the directory tree, with root directory pointed to by dir.
        Objects to display: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    Parameters:
        dir (str or pathlib.Path) : Absolute path the directory of interest
        contents (Dict[str, int]) : a dictionary of the same type as return type of get_diagnostics, has the form:

            .. highlight:: python
            .. code-block:: python

                {
                    "files": 0,
                    "subdirectories": 0,
                    ".csv files": 0,
                    ".txt files": 0,
                    ".npy files": 0,
                    ".md files": 0,
                    "other files": 0,
                }

    Returns:
        None
    """
    
    # error handling
    if not isinstance(dir, (str, Path)):
        raise TypeError("Expected a path or str but received another type")
    if not Path(dir).is_dir:
        raise NotADirectoryError("Input must be a path to a directory")
    if not Path(dir).exists:
        raise NotADirectoryError("This directory path does not exists")
    if not isinstance(contents, dict):
        raise TypeError("Expected a dictionary but received another type")

    # Print the summary to the terminal
    print(f"\nDiagnostics for {dir}")
    print("==============================")
    print(f"Number of files: {contents['files']}")
    print(f"Number of folders: {contents['subdirectories']}")
    print(f"Number of .csv files: {contents['.csv files']}")
    print(f"Number of .txt files: {contents['.txt files']}")
    print(f"Number of .npy files: {contents['.npy files']}")
    print(f"Number of .md files: {contents['.md files']}")
    print(f"Number of other files: {contents['other files']}")
    print("==============================\n")


def display_directory_tree(dir: str | Path, maxfiles: int = 3) -> None:
    """Display a directory tree, with root directory pointed to by dir.
       Limit the number of files to be displayed for convenience to maxfiles.
       This tree is built with inspiration from the code written by "Flimm" at https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest
        maxfiles (int) : Maximum number of files to be displayed at each level in the tree, default to three.

    Returns:
        None

    """
        
    # error handling
    if not isinstance(dir, (str, Path)):
        raise TypeError("Expected a path or str but received another type")
    if not Path(dir).is_dir:
        raise NotADirectoryError("Input must be a path to a directory")
    if not Path(dir).exists:
        raise NotADirectoryError("This directory path does not exists")
    if not isinstance(maxfiles, int):
        raise TypeError("Expected an int but received another type")
    if maxfiles != 3:
        raise ValueError("Got another error than expected")

    dir = Path(dir)
    if not dir.is_dir():
        print("Invalid directory path")
        return
    
    stack = [(dir, 0)]

    while stack:
        current_dir, depth = stack.pop()
        indent = "  " * depth

        if not current_dir.is_dir():
            continue

        print(f"{indent}+ {current_dir.name}")

        files = list(current_dir.iterdir())
        count = 0

        for item in files:
            if item.is_file():
                count += 1
                if count <= maxfiles:
                    print(f"{indent}  - {item.name}")
                else:
                    print(f"{indent}  - ...")
                    break
            elif item.is_dir():
                stack.append((item, depth + 1))
    
    print("\n")
        

def is_gas_csv(path: str | Path) -> bool:
    """Checks if a csv file pointed to by path is an original gas statistics file.
        An original file must be called '[gas_formula].csv' where [gas_formula] is
        in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
         - path (str of pathlib.Path) : Absolute path to .csv file that will be checked

    Returns
         - (bool) : Truth value of whether the file is an original gas file
    """
    
    path = Path(path)
    # Do correct error handling first
    # Extract the filename from the .csv file and check if it is a valid greenhouse gas
    if not isinstance(path, (str, Path)):
        raise TypeError("Expected a path or str but received another type")
    if path.suffix != ".csv":
        raise ValueError("Received another suffix than expected")

    # List of greenhouse gasses, correct filenames in front of a .csv ending
    gasses = ["CO2", "CH4", "N2O", "SF6", "H2"]
    if path.stem in gasses:
        return True

    return False


def get_dest_dir_from_csv_file(dest_parent: str | Path, file_path: str | Path) -> Path:
    """Given a file pointed to by file_path, derive the correct gas_[gas_formula] directory name.
        Checks if a directory "gas_[gas_formula]", exists and if not, it creates one as a subdirectory under dest_parent.

        The file pointed to by file_path must be a valid file. A valid file must be called '[gas_formula].csv' where [gas_formula]
        is in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
        - dest_parent (str or pathlib.Path) : Absolute path to parent directory where gas_[gas_formula] should/will exist
        - file_path (str or pathlib.Path) : Absolute path to file that gas_[gas_formula] directory will be derived from

    Returns:
        - (pathlib.Path) : Absolute path to the derived directory

    """
    
    # Do correct error handling first
    if not isinstance(dest_parent, (str, Path)):
        raise TypeError("Expected a path or str but received another type")
    if not isinstance(file_path, (str, Path)):
        raise TypeError("Expected a path or str but received another type")
    if not Path(file_path).is_file():
        raise ValueError("Expected a path to a file but got something else")
    if not is_gas_csv(file_path):
        raise ValueError("Expected a original .csv file but got another file")
    if not Path(dest_parent).exists():
        raise NotADirectoryError("Expected an existing direcory but did not get that")

    # If the input file is valid:
    # Derive the name of the directory, pattern: gas_[gas_formula] directory
    dest_name = "gas_" + str(Path(file_path).stem)
    # Derive its absolute path
    dest_path = str(dest_parent) + "/" + str(dest_name)

    # Check if the directory already exists, and create one of not
    dest_path = Path(dest_path)
    if not dest_path.exists():
        dest_path.mkdir(parents=True)
    
    return dest_path
        

def merge_parent_and_basename(path: str | Path) -> str:
    """This function merges the basename and the parent-name of a path into one, uniting them with "_" character.
       It then returns the basename of the resulting path.

    Parameters:
        - path (str or pathlib.Path) : Absolute path to modify

    Returns:
        - new_base (str) : New basename of the path
    """

    path = Path(path)
    if not isinstance(path, (str, Path)):
        raise TypeError("Expected a path or str but got something else")
    if not path.parent.name:
        raise ValueError("Expected a path with a parent but did not receive that")
    if not path.name:
        raise ValueError("Expected a path with a file-name but did not receive that")
    
    parent_name = path.parent.name
    base_name = path.name
    # New, merged, basename of the path, which will be the new filename
    new_base = (parent_name + "_" +  base_name).replace(os.sep, "_")
    return new_base


def delete_directories(path_list: List[str | Path]) -> None:
    """Prompt the user for permission and delete the objects pointed to by the paths in path_list if
    permission is given. If the object is a directory, its whole directory tree is removed.

    Parameters:
        - path_list (List[str | Path]) : a list of absolute paths to all the objects to be removed.


    Returns:
    None
    """
    
    path = Path(path_list[0])
    user_input = input(f"Do you want to delete '{path}'? (yes/no): ").strip().lower()

    if user_input == "yes":
        shutil.rmtree(path, ignore_errors=True)
        print(f"Deleted '{path}'")
    else:
        print(f"'{path}' was not deleted.")   
