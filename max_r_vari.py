#####
# This .py file works for T2 DPIQ products and extracts the number of heater resistance max variation fail from the YTEC LaserX cKGD testing results (.csv).
#####

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def max_r_vari(df: pd.DataFrame,
             lot_id: str,
             wafer_id: str,
             ) -> tuple[int, list[int]]:
    """
    This function analyzes the heater resistance max variation from the thermal-optic phase shifters among 12 channels (max - min), detects failures, generates histograms,
    and returns the numbers of failure as well as their indices.

    The indices are used to compare the failure indices from max_r_vari.py and p_pi.py to determine the total number of performance failure for 
    the thermo-optic phase shifters.

    The function works as the following:
        1. Locate the columns with the heater resistance max variation across all dies;
        2. Plot the distribution in histograms;
        2. Decide out-of-spec failures (max variation > 10 Ohm), indicate the failures in histograms;
        3. Save .png figure, return the number of failure and the indices.

    Args:
        df (DataFrame):
            Input Pandas DataFrame containing the max variation results
            Source file - LX_Productnumber_lotid_waferid.csv from YTEC database
        lot_id (str): input lot ID for the processing
        wafer_id (str): input wafer ID for the processing

    Returns:
        tuple[int, list[int]]: _description_
    """

    # Select columns AN to AY by position (Excel columns AN = index 39, AY = index 50)
    # Adjust if needed after checking your CSV
    cols = df.columns[53]   # AN = col 39, AY = col 50

    # Extract data
    data = df[cols]

    index = []

    fig, axes = plt.subplots(1, 1, figsize=(8, 6))
    axes = [axes]

    col_data = data.dropna()

    custom_outliers = col_data[(col_data > 10)]

    axes[0].hist(col_data, bins=80, color='steelblue', alpha=0.9)
    axes[0].set_title(cols)
    axes[0].set_xlim(0,50)
    axes[0].set_xticks(np.arange(0, 51, 5))
    axes[0].set_yticks(np.arange(0, 31, 5))
    axes[0].axvline(x=10, color='grey', linestyle='--', linewidth=2)
    axes[0].grid(True)

    if len(custom_outliers) > 0:
        axes[0].scatter(
            custom_outliers,
            np.full(len(custom_outliers), 1), # x positions
            color='red',
            s=25,
            zorder=3,
            alpha=0.6,
            label=cols  # label only once
                )

    for idx, _ in custom_outliers.items():
        index.append(idx)

    num_fail = len(set(index))
    index = sorted(index)
    plt.tight_layout()
    plt.savefig(f"{lot_id}_{wafer_id}_maxi_r_vari.png", dpi=300, bbox_inches="tight")
    
    return num_fail, index 

def main():
    # # Load the CSV file
    # path = "C:\\Users\\YidingLin\\LX_TB004A_F0280_08.csv"
    # df = pd.read_csv(path)
    # _, lot_id, wafer_id = wafer_lot_id(path)
    # num_fail, _ = max_r_vari(df, lot_id, wafer_id)
    # print(num_fail)
    return True

if __name__ == "__main__":
    main()  