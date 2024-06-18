"""Module containing the functions used to plot the resulting data.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def create_plot(src_dir: str | Path, dest_dir: str | Path) -> None:
    """Read all the .csv files within src_dir and display the data in one plot.
        Store the plot at dest_dir, named as gas_[formula].png.
        This function assumes that src_dir contains original gas .csv files only and no other files and subdirectories

    Parameters:
        - src_dir (str or pathlib.Path) : Absolute path to gas_[gas_formula] directory containing .csv files with data
        - dest_dir (str or pathlib.Path) : Absolute path to the directory to save the plot in

    """
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)

    if not src_dir.is_dir():
        raise NotADirectoryError(
            f"Expected an existing directory for src_dir, but received {src_dir}"
        )
    elif not dest_dir.is_dir():
        raise NotADirectoryError(
            f"Expected an existing directory for dest_dir, but received {dest_dir}"
        )

    plt.figure(1, figsize=(10, 8))

    # Create labels with correct syntax
    name_dict = {
        "CH4": r"$\mathrm{CH_4}$",
        "CO2": r"$\mathrm{CO_2}$",
        "N2O": r"$\mathrm{N_2O}$",
    }
    label = str(src_dir)[-3:]
    gas_name = name_dict.get(label, label)
    plt.title(
        r"Air pollution of "
        + gas_name
        + r" from five different sources as function of year"
    )
    for file in src_dir.iterdir():
        if not file.is_file():
            # Invalid argument, cannot read it as a file
            raise FileNotFoundError(f"Object pointed to by {file} is not a file")
        elif not file.suffix == ".csv":
            # Invalid file type, must be .csv
            raise TypeError(f"Object pointed to by {file} is not a .csv file")
        # Create a label for the plot
        label_parts = str(file.name).split("_")
        label = ""
        for i in range(1, len(label_parts) - 1):
            label += label_parts[i] + " "
        # Plotting
        data = np.loadtxt(file, delimiter=",", skiprows=1)
        plt.plot(data[:, 0], data[:, 1], label=label)

    plt.legend()
    plt.xlabel("Year")
    plt.ylabel(r"1000 tonn $\mathrm{CO_2}$-equivalents AR5")
    # Create a name for the plot to store in dest_dir
    figname = src_dir.name + ".png"
    figpath = dest_dir / figname
    plt.savefig(figpath, dpi=200)
    plt.close()


def plot_pollution_data(by_gas_dir: str | Path, fig_dir: str | Path) -> None:
    """This function traverses the subdirectories of directory pointed to by by_gas_dir, which should be pollution_data_restructured/by_gas,
      and creates plots for each of them.
      It assumes that pollution_data_restructured/by_gas has only subdirectories of type gas_[gas_formula] as its contents,
      and that each of these subdirectories contains only original gas .csv files filtered by gas type.
      Each plot is saved as .png file in fig_dir directory.

    Parameters:
        - by_gas_dir (str or pathlib.Path) : Absolute path to the pollution_data_restructured/by_gas directory containing gas_[gas_formula] subdirectories
        - fig_dir (str or pathlib.Path) : Absolute path to the pollution_data_restructured/figures directory where the plots are to be stored

    Returns:
    None
    """
    by_gas_dir = Path(by_gas_dir)
    fig_dir = Path(fig_dir)

    if not by_gas_dir.exists():
        raise NotADirectoryError(f"Object pointed to by {by_gas_dir} does not exist")
    elif not fig_dir.exists():
        raise NotADirectoryError(f"Object pointed to by {fig_dir} does not exist")

    for gas_subdir in by_gas_dir.iterdir():
        if not gas_subdir.is_dir():
            # Invalid structure of by_gas_dir
            raise NotADirectoryError(
                f"Object pointed to by {gas_subdir} is not a directory"
            )
        else:
            create_plot(gas_subdir, fig_dir)
