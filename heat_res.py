#####
# This .py file works for T2 DPIQ products and extracts the number of heater resistance fail from the YTEC LaserX cKGD testing results (.csv).
#####

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def heat_res(df: pd.DataFrame, 
             lot_id: str, 
             wafer_id: str
             ) -> tuple[int, list[int]]:
    """
    This function analyzes the heater resistance from the thermal-optic phase shifters for 12 channels, detects failures, generates histograms,
    and returns the numbers of failure as well as their indices.

    The indices are used to compare the failure indices from max_r_vari.py and p_pi.py to determine the total number of performance failure for 
    the thermo-optic phase shifters.

    The function works as the following:
        1. Locate the columns with the heater resistance measurements for the 12 channels across all dies;
        2. Plot the resistance distribution in histograms;
        2. Decide out-of-spec failures (resistance < 450 Ohm or > 520 Ohm), indicate the failures in histograms;
        3. Save .png figure, return the number of failure and the indices.

    Args:
        df (DataFrame):
            Input Pandas DataFrame containing the heater resistance results (columns 39-50, AN-AY for the 12 channels)
            Source file - LX_Productnumber_lotid_waferid.csv from YTEC database
        lot_id (str): input lot ID for the processing
        wafer_id (str): input wafer ID for the processing

    Returns:
        Tuple[int, List[int]]:
            - The total number of dies that fail based on out-of-spec data.
            - A sorted list of die indices where failures occur.
    """
    
    # Select columns AN to AY by position (Excel columns AN = index 39, AY = index 50)
    cols = df.columns[39:51]

    data = df[cols]   # extract data

    cols_SN = [col[2:5] for col in cols] # create shortened column name for plotting

    index = [] # Define the failure index list

    # --- Create histograms for each column ---
    fig, axes = plt.subplots(1, 12, figsize=(16, 8), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, col in enumerate(cols):
        col_data = data[col].dropna()
        
        normal = col_data[(col_data >= 450) & (col_data <= 520)]  ## Collect data within spec
        custom_outliers = col_data[(col_data < 450) | (col_data > 520)] ## Collect data out of spec
        
        axes[i].hist(normal, bins=50, color='steelblue', alpha=0.9, orientation='horizontal')
        axes[i].set_title(cols_SN[i])
        axes[i].set_ylim(400,570)
        axes[i].set_yticks(np.arange(400, 571, 10))
        axes[i].set_xticks(np.arange(0, 11, 5))
        axes[i].axhline(y=450, color='grey', linestyle='--', linewidth=2)
        axes[i].axhline(y=520, color='grey', linestyle='--', linewidth=2)
        axes[i].grid(True)

        try:
            if len(custom_outliers) > 0:
                axes[i].scatter(
                    np.full(len(custom_outliers), i + 1),  # x positions
                    custom_outliers,
                    color='red',
                    s=25,
                    zorder=3,
                    alpha=0.6,
                    label=cols_SN if i == 0 else None  # label only once
                )

            for idx, _ in custom_outliers.items():
                if idx not in index:
                    index.append(idx)
        except Exception as e:
            print("There is no outlier for heater resistance")


    fig.supylabel("Resistance (Ohm)")
    fig.supxlabel("Count")
    plt.tight_layout()
    plt.savefig(f"{lot_id}_{wafer_id}_heater_res.png", dpi=300, bbox_inches="tight")

    num_fail = len(set(index))
    index = sorted(index)
    return num_fail, index

def main():
    # Load the CSV file
    # path = "C:\\Users\\YidingLin\\LX_TB004A_F0280_08.csv"
    # df = pd.read_csv(path)
    # _, lot_id, wafer_id = wafer_lot_id(path)
    # num_fail, _ = heat_res(df, lot_id, wafer_id)
    # print("Number of Heater Resistance Fails:", num_fail)
    return True

if __name__ == "__main__":
    main()
