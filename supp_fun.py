"""
Providing functions to support data analysis
"""

import os
import glob
import pandas as pd
import cKGD_AOI_map as AOImap
import heat_res as heat_res
import max_r_vari as MR
import Ppi
import IL_PDL
import ER
import screen as scr

def folder_to_file(folders_path):
    """_summary_

    Args:
        ytec_path (_type_): Input local folder path for ytec measurements
        AOI_path (_type_): Input local folder path for AOI measurements
        screen_path (_type_): Input local folder path for screening test results

    Returns:
        _type_: 
    """
    ## Grab the file names from all the files in the folders
    files_path = []

    for folder in folders_path:
        files = glob.glob(folder + "/*")
        files_path.append(files)
    
    return files_path
    
def find_subfolder(master_folder_path):
    """

    Args:
        master_folder (_type_): _description_

    Returns:
        _type_: _description_
    """
    sub_folders_path = [
        os.path.join(master_folder_path, name)
        for name in os.listdir(master_folder_path)
        if os.path.isdir(os.path.join(master_folder_path, name))
        ]

    return sub_folders_path

def file_input(ytec_filepaths, AOI_filepaths, screen_filepaths):

    file_dict = {"ytec": ytec_filepaths,
                "AOI": AOI_filepaths,
                "scr_delta": screen_filepaths,
                }
    return file_dict

def read_data_from_file(path_list):
    df_list = []
    lot_id = []
    wafer_id = []
    for path in path_list:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            df_list.append(pd.read_csv(path))
            _, lot, wafer = wafer_lot_id(path)
            lot_id.append(lot)
            wafer_id.append(wafer)
        
        if ext == ".xlsx":
            df_list.append(pd.read_excel(path,sheet_name = 'Delta', header=6))

        if ext == ".txt":
            with open(path, "r") as f:
                df_list.append(f.readlines())
 
    return df_list, lot_id, wafer_id

def master_folder_to_data(master_folder_path):
    sub_folder_path = find_subfolder(master_folder_path)
    files_path = folder_to_file(sub_folder_path)
    df_lists, lot_ids, wafer_ids = [], [], []
    for file in files_path:
        df_list, lot_id, wafer_id = read_data_from_file(file)
        df_lists.append(df_list)
        lot_ids.append(lot_id)
        wafer_ids.append(wafer_id)
    return df_lists, lot_ids, wafer_ids

def aoi_map_calc(lines_list, lot_id, wafer_id):
    count_F = []
    for ii in range(len(lines_list)):
        count_f = AOImap.AOI_map(lines_list[ii], lot_id[ii], wafer_id[ii])
        count_F.append(count_f)
    return count_F

def heater_pareto(df_list, lot_ids, wafer_ids):
    count_F_tot = []
    count_indvl = {"f_res": [], "f_max_vari": [], "f_ppi": []}   ### within one lot
    for ii in range(len(df_list)):
        count_f_res, idx_res = heat_res.heat_res(df_list[ii], lot_ids[ii], wafer_ids[ii])
        count_f_vari, idx_vari = MR.max_r_vari(df_list[ii], lot_ids[ii], wafer_ids[ii])
        count_f_ppi, idx_ppi = Ppi.Ppi(df_list[ii], lot_ids[ii], wafer_ids[ii])
        _, count_f_res_maxR_ppi = merge_unique(idx_res, idx_vari, idx_ppi)
        
        count_F_tot.append(count_f_res_maxR_ppi)
        count_indvl["f_res"].append(count_f_res)
        count_indvl["f_max_vari"].append(count_f_vari)
        count_indvl["f_ppi"].append(count_f_ppi)

    return count_F_tot, count_indvl

def optical_pareto(df_list, lot_ids, wafer_ids):
    count_F_tot = []
    count_indvl = {"f_il": [], "f_pdl": [], "f_er": []}  ### within one lot
    for ii in range(len(df_list)):
        _, count_f_il, count_f_pdl, index_il_pdl = IL_PDL.IL_PDL(df_list[ii], lot_ids[ii], wafer_ids[ii])
        count_f_er, index_er = ER.ER(df_list[ii], lot_ids[ii], wafer_ids[ii])
        _, count_f_er_il_pdl = merge_unique(index_il_pdl, index_er)

        count_F_tot.append(count_f_er_il_pdl)
        count_indvl["f_il"].append(count_f_il)
        count_indvl["f_pdl"].append(count_f_pdl)
        count_indvl["f_er"].append(count_f_er)

    return count_F_tot, count_indvl

def screen_pareto(df_list, lot_ids, wafer_ids):
    count_F_tot = []
    count_F_opt = []
    count_indvl = {}
    
    for df in df_list:
        for jj in range(len(wafer_ids)):
            f_dict_screen, _, count_f_opt, tot_f = scr.screen(df, lot_ids[0], int(wafer_ids[jj]))
            print(f_dict_screen)
            # print(df)
            print(len(lot_ids))
            if jj == 0 and (df is df_list[0]):
                count_indvl = f_dict_screen
                for key in count_indvl:
                    count_indvl[key] = []
                    count_indvl[key].append(f_dict_screen[key]) 
            count_F_tot.append(tot_f)
            count_F_opt.append(count_f_opt)
            for key in count_indvl:
                count_indvl[key].append(f_dict_screen[key])

    return count_F_tot, count_F_opt, count_indvl

def final_pareto(ytec_df_list, aoi_df_list, scr_df_list, lot_id, wafer_id):  ##For single lot
    count_f_aoi = aoi_map_calc(aoi_df_list, lot_id, wafer_id)
    count_f_heater, idx_heater = heater_pareto(ytec_df_list, lot_id, wafer_id)
    count_f_optical, idx_optical = optical_pareto(ytec_df_list, lot_id, wafer_id)
    count_f_screen, count_f_opt_scr, indvl_screen = screen_pareto(scr_df_list, lot_id, wafer_id)

    return count_f_aoi, count_f_heater, count_f_optical, count_f_screen, count_f_opt_scr, idx_heater, idx_optical, indvl_screen

def merge_unique(list_a: list[int],
                 list_b: list[int],
                 list_c=None,
                 ) -> tuple[list[int], int]:
    """
    This function is to merge two to three lists of integers and remove the duplicates.
    list_c by default is None.

    Args:
        a (list[int]): input list a
        b (list[int]): input list b
        c (list[int]): input list c

    Returns:
        tuple[list[int], int]: output list and the length of the list
    """
    if list_c is None:
        list_c = []
    merged = sorted(set(list_a + list_b + list_c))

    return merged, len(merged)


def wafer_lot_id(file_path: str) -> tuple[str, str, str]:
    """
    This function inputs a path to a file and extracts the product ID, lot ID, and wafer ID. 

    Args:
        file_path (str): input file path

    Returns:
        tuple [str, str, str]: product ID, lot ID and wafer ID
    """
    base_name = os.path.basename(file_path)
    parts = base_name.split('_')
    prod_id = parts[1]
    lot_id = parts[2]
    wafer_id = parts[3].replace('.csv', '')

    return prod_id, lot_id, wafer_id