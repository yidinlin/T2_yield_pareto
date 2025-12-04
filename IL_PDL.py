#####
# This .py file works for T2 DPIQ products and extracts the number of IL & PDL fail from the YTEC LaserX cKGD testing results (.csv).
#####

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def IL_PDL(df: pd.DataFrame,
           lot_id: str,
           wafer_id: str,
           ) -> tuple[int, int, int, list[int]]:
    """
    This function analyzes the IL & PDL from the TFLN EO modulators, detects failures, generates histograms,
    and returns the numbers of failure as well as their indices.

    The indices are used to compile with that from ER.py to determine the total number of performance failure for 
    the EO modulators.

    The function works as the following:
        1. Locate the columns with IL & PDL measurements across all dies;
        2. Plot the IL & PDL distribution in histograms;
        2. Decide out-of-spec failures (IL > 8.64 dB or |PDL| > 1.0 dB), indicate the failures in histograms;
        3. Save .png figure, return the number of failures and the indices.

    Args:
        df (pd.DataFrame):
            Input Pandas DataFrame containing the IL & PDL results
            Source file - LX_Productnumber_lotid_waferid.csv from YTEC database
        lot_id (str): input lot ID for the processing
        wafer_id (str): input wafer ID for the processing

    Returns:
        tuple[int, int, int, list[int]]:
            - The total number of dies that fail based on out-of-spec data.
            - The total number of dies that fail based on IL.
            - The total number of dies that fail based on PDL.
            - A sorted list of die indices where failures occur.
    """
    
    cols_SN = ['IL', 'PDL']

    # FOR IL, Select columns
    data_1524 = df.iloc[:, [87, 90]]   # IL_true & PDL at 1524 nm
    data_1550 = df.iloc[:, [124, 127]]   # IL_true & PDL at 1550 nm
    data_1580 = df.iloc[:, [161, 164]]   # IL_true & PDL at 1580 nm

    ### assign the database with short names (SN)
    sn_1524 = pd.DataFrame()
    sn_1550 = pd.DataFrame()    
    sn_1580 = pd.DataFrame()
    for i in range(len(cols_SN)):
        sn_1524[f"{cols_SN[i]}"] = data_1524.iloc[:, i].dropna()
        sn_1550[f"{cols_SN[i]}"] = data_1550.iloc[:, i].dropna()
        sn_1580[f"{cols_SN[i]}"] = data_1580.iloc[:, i].dropna()
    
    df_list = [sn_1524, sn_1550, sn_1580] ## combine into list for easy processing

    ## Plot the histograms
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    axes = axes.flatten()

    index_tot, index_il, index_pdl = [], [], []  ## store the total, il and PDL FX die index numbers
    bins = np.arange(0, 30.1, 0.1)   ### bins for the histogram

    #### Obtain the number of failures and indices 
    for i in range(len(df_list)):
        for j, col in enumerate(df_list[i].columns):
            fx, il_FX, pdl_FX = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
            col_data = df_list[i][col]
            
            if col == 'IL':
                il_FX = col_data[(col_data > 8.64)]
                axes[j].axvline(x=8.64, color='grey', linestyle='--', linewidth=2)
                axes[j].set_xlim(0,40)
                axes[j].set_xticks(np.arange(0, 41, 5))
                axes[j].hist(col_data, bins=bins, color='steelblue', alpha=0.9)
                axes[j].set_yticks(np.arange(0, 41, 5))

            if col == 'PDL':
                col_data = col_data.abs()
                pdl_FX = col_data[(col_data > 1.0)]
                axes[j].set_xlim(0,30)
                axes[j].set_xticks(np.arange(0, 31, 1))
                axes[j].axvline(x=1.0, color='grey', linestyle='--', linewidth=2)
                axes[j].hist(col_data, bins=bins, color='steelblue', alpha=0.9)
                axes[j].set_yticks(np.arange(0, 61, 5))

            axes[j].set_xlabel(f"{col} (dB)")
            axes[j].grid(True)

            try:
                for fx in [il_FX, pdl_FX]:
                    if len(fx) > 0:
                        axes[j].scatter(
                            fx,
                            np.full(len(fx), j + 13),  # y positions
                            color='red',
                            s=25,
                            zorder=5,
                            alpha=0.3,
                            label=col if j == 0 else None  # label only once
                        )

                    ### Extract the total number of fail due to IL or PDL
                    for idx, _ in fx.items():
                        if idx not in index_tot:
                            index_tot.append(idx)

            except Exception as e:
                print(f"There is no outlier in IL or PDL in column {j}")
            
            ### Extract the total fail due to IL
            for idx, _ in il_FX.items():
                if idx not in index_il:
                    index_il.append(idx)

            ### Extract the total fail due to PDL
            for idx, _ in pdl_FX.items():
                if idx not in index_pdl:
                    index_pdl.append(idx)

    tot_fail = len(set(index_tot))
    il_fail = len(set(index_il))
    pdl_fail = len(set(index_pdl))
    index_out = sorted(index_tot)

    fig.supylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{lot_id}_{wafer_id}_IL_PDL.png", dpi=300, bbox_inches="tight")

    return tot_fail, il_fail, pdl_fail, index_out

def main():
    # Load the CSV file
    # path = "C:\\Users\\YidingLin\\LX_TB004A_FPGF2_04.csv"
    # df = pd.read_csv(path)
    # _, lot_id,wafer_id = wafer_lot_id(path)
    # tot_fail, il_fail, pdl_fail, _ = IL_PDL(df, lot_id, wafer_id)
    # print(f"Number of failing devices for IL and PDL: {tot_fail} {il_fail} {pdl_fail}")
    return True

if __name__ == "__main__":
    main()