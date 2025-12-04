import pandas as pd

def process(df, lot_id, wafer_id, cols_f, col_shipment):

    # Filter only Lot_ID = FPGF2
    df_fpg = df[(df['Lot_ID'] == lot_id) & (df['Wafer_ID'] == wafer_id)]

    # Count “f” across AE–AI
    count = []
    index = []
    for col in cols_f:
        f_count = (df_fpg[col] == 0).sum()
        zero_indices = df_fpg.index[df_fpg[col] == 0].tolist()
        count.append(int(f_count))
        index.append(zero_indices)

    # Count Optical Fail
    opt_fail = sorted(list(set(index[2]+index[3])))
    # Count “no” in SHIP?
    no_count = (df_fpg[col_shipment] == 0).sum()


    return count, index, opt_fail, no_count


def screen(df, lot_id, wafer_id):
    
    # AE–AI columns (after renaming using row 7)
    cols_f = ['IL', 'PDL', 'dIL', 'dPDL', 'ER_iq', 'ER_xy', 'R', 'Rspread', 'Pπ', 'FVI', 'Chipping']

    # AJ column = SHIP?
    col_shipment = 'SHIP?'

    f1, idx, opt_fail, no1 = process(df, lot_id, wafer_id, cols_f, col_shipment)
    # f2, no2 = process(df2, lot_id, wafer_id, cols_f, col_shipment)

    # total_f = []
    # for i in range(len(f1)):
    #     total_f.append(f1[i] + f2[i])
    
    f_dict = dict(zip(cols_f, f1))
    total_no = no1

    return f_dict, idx, opt_fail, total_no


if __name__ == "__main__":
    
    # Read files using row 7 (0-indexed → header=6) as column names
    # df1 = pd.read_excel('C:\\Users\\YidingLin\\Downloads\\screening delta 20251107.xlsx', header=6)
    df = pd.read_excel('C:\\Users\\YidingLin\\Downloads\\screening delta 20251107.xlsx', sheet_name = "Delta", header=6)
    lot_id = 'FPGF2'
    wafer_id = 8

    total_f, idx, opt_fail, total_no = screen(df, lot_id, wafer_id)

    print(idx)
    print(opt_fail)

    print("Total f_count across both files:", total_f)
    print("Total no_count across both files:", total_no)

