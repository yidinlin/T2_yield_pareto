#####
# This .py file works for T2 DPIQ products and extracts the number of ER fail from the YTEC LaserX cKGD testing results (.csv).
#####

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def ER(df: pd.DataFrame,
           lot_id: str,
           wafer_id: str,
        ) -> tuple[int, list[int]]:
    """
    This function analyzes the ER performance from the TFLN EO modulators, detects failures, generates histograms,
    and returns the numbers of failure as well as their indices.

    The indices are used to compile with that from IL_PDL.py to determine the total number of performance failure for 
    the EO modulators.

    The function works as the following:
        1. Locate the columns with ER measurements across all dies;
        2. Plot the ER distribution in histograms;
        2. Decide out-of-spec failures (ER < 25 dB for parent or ER < 26 dB for child), indicate the failures in histograms;
        3. Save .png figure, return the number of failures and the indices.


    Args:
        df (pd.DataFrame): 
            Input Pandas DataFrame containing the ER results
            Source file - LX_Productnumber_lotid_waferid.csv from YTEC database
        lot_id (str): input lot ID for the processing
        wafer_id (str): input wafer ID for the processing

    Returns:
        tuple[int, int, int, list[int]]:
            - The total number of dies that fail based on out-of-spec data.
            - The total number of dies that fail based on ER.
            - A sorted list of die indices where failures occur.
    """
    # Select columns
    cols_1524 = df.columns[81:87]   # XI, XQ, XP, YI, YQ, YP at 1524 nm
    cols_1550 = df.columns[118:124]   # XI, XQ, XP, YI, YQ, YP at 1550 nm
    cols_1580 = df.columns[155:161]   # XI, XQ, XP, YI, YQ, YP at 1580 nm

    data_1524 = df[cols_1524]
    data_1550 = df[cols_1550]
    data_1580 = df[cols_1580]

    # Extract data
    cols_SN = [col[3:5] for col in cols_1524]
    # print(cols_SN)

    ##combine into one column for the same channel but at different wavelengths
    df_1524 = pd.DataFrame()
    df_1550 = pd.DataFrame()
    df_1580 = pd.DataFrame()

    for i in range(len(cols_SN)):
        df_1524[f"{cols_SN[i]}"] = data_1524.iloc[:,i].dropna()
        df_1550[f"{cols_SN[i]}"] = data_1550.iloc[:,i].dropna()
        df_1580[f"{cols_SN[i]}"] = data_1580.iloc[:,i].dropna()

    df_list = [df_1524, df_1550, df_1580]

    fig, axes = plt.subplots(1, 6, figsize=(12, 8), sharex=True, sharey=True)
    axes = axes.flatten()

    index = []
    bins = np.arange(0, 66, 0.5)

    for i in range(len(df_list)):       
        for j, col in enumerate(df_list[i].columns):
            col_data = df_list[i][col]

            # custom outliers:
            # < 25
            if (col == 'XP') or (col == 'YP'):
                outlier = col_data[(col_data < 25)]
                axes[j].hist(col_data, bins=bins, color='steelblue', orientation='horizontal')
                axes[j].axhline(y=25, color='grey', linestyle='--', linewidth=2)

            else:
                outlier = col_data[(col_data < 26)]
                axes[j].hist(col_data, bins=bins, color='steelblue', orientation='horizontal')
                axes[j].axhline(y=26, color='grey', linestyle='--', linewidth=2)
                
            axes[j].set_title(cols_SN[j])
            axes[j].set_ylim(10,50)
            axes[j].set_yticks(np.arange(0, 66, 5))
            axes[j].set_xticks(np.arange(0, 21, 5))
            axes[j].grid(True)

            if len(outlier) > 0:
                axes[j].scatter(
                    np.full(len(outlier), j + 15),  # x positions
                    outlier,
                    color='red',
                    s=25,
                    zorder=5,
                    alpha=0.3,
                    label=col if j == 0 else None  # label only once
                )

            for idx, _ in outlier.items():
                if idx not in index:
                    index.append(idx)

    num_fail = len(set(index))
    # print(num_fail)
    index = sorted(index)
    print(sorted(index))

    fig.supylabel("ER (dB)")
    fig.supxlabel("Count")
    plt.tight_layout()
    plt.savefig(f"{lot_id}_{wafer_id}_ER.png", dpi=300, bbox_inches="tight")

    return num_fail, index


def main():
    # Load the CSV file
    # path = "C:\\Users\\YidingLin\\LX_TB004A_FPGF2_04.csv"
    # df = pd.read_csv(path)
    # _, lot_id, wafer_id = wafer_lot_id(path)
    # fail_er, _ = ER(df, lot_id, wafer_id)
    # print(f"Number of failing devices for ER: {fail_er}")
    return True

if __name__ == "__main__":
    main()