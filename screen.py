import pandas as pd

def process(df, lot_id, wafer_id, cols_f, col_shipment):

    # Filter only Lot_ID = FPGF2
    df_fpg = df[(df['Lot_ID'] == lot_id) & (df['Wafer_ID'] == wafer_id)]

    # Count “f” across AE–AI
    count = []
    index = []
    for col in cols_f:
        f_count = (df_fpg[col] == 'f').sum()
        zero_indices = df_fpg.index[df_fpg[col] == 'f'].tolist()
        count.append(int(f_count))
        index.append(zero_indices)

    # Count Optical Fail
    opt_fail = sorted(list(set(index[2])))

    # Count “no” in SHIP?
    no_count = (df_fpg[col_shipment] == 'no').sum()

    return count, index, opt_fail, no_count


def screen(df, lot_id, wafer_id):
    
    # AE–AI columns (after renaming using row 7)
    cols_f = ['IL', 'PDL', 'IL&PDL', 'FVI', 'Chipping']

    # AJ column = SHIP?
    col_shipment = 'SHIP?'

    f1, idx, opt_fail, no1 = process(df, lot_id, wafer_id, cols_f, col_shipment)

    f_dict = dict(zip(cols_f, f1))

    return f_dict, idx, opt_fail, no1


if __name__ == "__main__":
    
    # Read files using row 7 (0-indexed → header=6) as column names
    df1 = pd.read_excel('C:\\Users\\YidingLin\\Downloads\\screening delta 20251015.xlsx', header=6)
    df2 = pd.read_excel('C:\\Users\\YidingLin\\Downloads\\screening delta 20251017.xlsx', header=6)
    lot_id = "FPGF2"
    wafer_id = 6

    total_f, _, _, total_no = screen(df1, lot_id, wafer_id)

    print("Total f_count across both files:", total_f)
    print("Total no_count across both files:", total_no)

