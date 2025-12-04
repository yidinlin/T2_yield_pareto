import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from supp_func import wafer_lot_id

def AOI_map(lines, lot_id, wafer_id):

    # Parse only measurement lines (start with a number)
    data = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():     
            parts = line.split(",")
            if len(parts) >= 3:
                row = int(parts[0])
                col = int(parts[1])
                val = parts[2].strip()
                data.append((row, col, val))

    # Convert into DataFrame
    df = pd.DataFrame(data, columns=["row", "col", "val"])

    # ===== 2. Count T and F =====
    count_T = (df["val"] == "T").sum()
    count_F = (df["val"] == "F").sum()-32  # subtract 28 known blank F

    print("Total T:", count_T)
    print("Total F:", count_F)

    # ===== 3. Create heatmap array =====
    # Map: T = 1, F = -1, _ = 0
    max_row = (df["row"].max())
    max_col = (df["col"].max())

    heat = np.zeros((max_row + 1, max_col + 1), dtype=int)

    for _, r in df.iterrows():
        if r["val"] == "T":
            heat[r["row"], r["col"]] = 1
        elif r["val"] == "F":
            heat[r["row"], r["col"]] = -1
        else:
            heat[r["row"], r["col"]] = 0

    # ===== 4. Plot heatmap =====
    plt.figure(figsize=(8, 6))
    # plt.imshow(heat, aspect="auto", cmap ="RdYlGn")
    plt.pcolormesh(heat, edgecolors='black', linewidth=0.5, cmap= "RdYlGn")
    cbar = plt.colorbar()
    cbar.set_ticks([-1, 0, 1])
    cbar.ax.set_yticklabels(["Fail", "Out of Range", "Pass"])
    plt.title("AOI Pass/Fail Heatmap")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.yticks(np.arange(0.5, max_row + 0.5, 5), np.arange(1, max_row + 1, 5))
    plt.xticks(np.arange(0.5, max_col + 0.5, 1), np.arange(1, max_col + 1))
    plt.tight_layout()
    # plt.grid()
    plt.savefig(f"{lot_id}_{wafer_id}_AOI_map.png", dpi=300, bbox_inches="tight")

    return count_F

def main():
    #  # Load the CSV file
    # path = "C:\\Users\\YidingLin\\TB004A_FPGF2_12.txt"

    #  # Generate AOI map and get count of F
    # count_F = AOI_map(path)
    # print(count_F)

    return True

if __name__ == "__main__":
    main()
