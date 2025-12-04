import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Ppi(df, lot_id, wafer_id):
    index = []
    custom_outliers = pd.DataFrame()
    num_fail = 0
    
    # Select columns
    cols_1524 = df.columns[69:75]   # XI, XQ, XP, YI, YQ, YP at 1524 nm
    cols_1550 = df.columns[106:112]   # XI, XQ, XP, YI, YQ, YP at 1550 nm
    cols_1580 = df.columns[143:149]   # XI, XQ, XP, YI, YQ, YP at 1580 nm

    data_1524 = df[cols_1524]
    data_1550 = df[cols_1550]
    data_1580 = df[cols_1580]

    # Extract data
    cols_SN = [col[4:6] for col in cols_1524]
    # print(cols_SN)

    df_1524 = pd.DataFrame()
    df_1550 = pd.DataFrame()
    df_1580 = pd.DataFrame()

    for i in range(len(cols_SN)):
        df_1524[f"{cols_SN[i]}"] = data_1524.iloc[:,i].dropna()
        df_1550[f"{cols_SN[i]}"] = data_1550.iloc[:,i].dropna()
        df_1580[f"{cols_SN[i]}"] = data_1580.iloc[:,i].dropna()

    df_list = [df_1524, df_1550, df_1580]

    fig, axes = plt.subplots(1, 6, figsize=(10, 8), sharex=True, sharey=True)
    axes = axes.flatten()

    bins = np.arange(15, 56, 0.1)

    for i in range(len(df_list)):
        for j, col in enumerate(df_list[i].columns):
            col_data = df_list[i][col].dropna()
            
            # custom outliers:
            # ≤ 19 or ≥ 35
            normal = col_data[(col_data <= 35) & (col_data >= 19)]
            custom_outliers = col_data[(col_data < 19) | (col_data > 35)]

            axes[j].hist(normal, bins=bins, color='steelblue', alpha=0.9, orientation='horizontal')
            axes[j].set_title(cols_SN[j])
            axes[j].set_ylim(15,40)
            axes[j].set_yticks(np.arange(15, 41, 5))
            axes[j].set_xticks(np.arange(0, 21, 5))
            axes[j].axhline(y=35, color='grey', linestyle='--', linewidth=2)
            axes[j].axhline(y=19, color='grey', linestyle='--', linewidth=2)
            axes[j].grid(True)

            try:
                if len(custom_outliers) > 0:
                    axes[j].scatter(
                        np.full(len(custom_outliers), j + 1), # x positions
                        custom_outliers,
                        color='red',
                        s=25,
                        zorder=3,
                        alpha=0.6,
                        label=col  # label only once
                            )
                
                    for idx, _ in custom_outliers.items():
                        index.append(idx)
            
            except Exception as e:
                print(f"no outliers for {col}: {e}")

        try:
            num_fail = len(set(index))
            index = sorted(index)
        except Exception as e:
            num_fail = 0

        fig.supylabel("Ppi (mW)")
        fig.supxlabel("Count")
        plt.tight_layout()
        plt.savefig(f"{lot_id}_{wafer_id}_Ppi.png", dpi=300, bbox_inches="tight")

    return num_fail, index

def main():
    # # Load the CSV file
    # path = "C:\\Users\\YidingLin\\LX_TB004A_FPGF2_12.csv"
    # df = pd.read_csv(path)
    # _, lot_id, wafer_id = wafer_lot_id(path)
    # num_fail, _ = Ppi(df, lot_id, wafer_id)
    # print("Number of Heater Resistance Fails:", num_fail)
    return True

if __name__ == "__main__":
    main()