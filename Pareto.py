"""
For Pareto plots generation.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cKGD_AOI_map as AOImap
import heat_res as heat_res
import max_r_vari as MR
import Ppi
import IL_PDL
import ER
import screen as scr
from supp_fun import master_folder_to_data, final_pareto, optical_pareto
from plotting import bar_plot


# YTEC folder to paths
ytec_master_folder_path = "C:\\Users\\YidingLin\\YTEC"
ytec_df_lists, lot_ids, wafer_ids = master_folder_to_data(ytec_master_folder_path)
print(len(lot_ids))
print(wafer_ids)

# AOI folder to paths
aoi_master_folder_path = "C:\\Users\\YidingLin\\AOI"
aoi_df_lists, _, _ = master_folder_to_data(aoi_master_folder_path)

#screen folder to paths
scr_master_folder_path = "C:\\Users\\YidingLin\\Screen"
scr_df_lists, _, _ = master_folder_to_data(scr_master_folder_path)

# folder_path = {"ytec": "C:\\Users\\YidingLin\\LX_TB004A_FPGF2_04.csv",
#              "AOI": "C:\\Users\\YidingLin\\TB004A_FPGF2_04.txt",
#              "scr_delta": ['C:\\Users\\YidingLin\\Downloads\\screening delta 20251017.xlsx']
#             }

## Final Pareto
labels = ['AOI Fail', 'Heater Fail', 'Optical Fail', 'Optical Fail aft. Screen', 'FVI Fail', 'Chipping Fail']
for ii in range(len(lot_ids)):
    final_pareto_aoi, final_pareto_heater, final_pareto_optical, final_pareto_screen, final_pareto_aft_scr, _, _, indvl_screen = final_pareto(ytec_df_lists[ii], aoi_df_lists[ii], scr_df_lists[ii], lot_ids[ii], wafer_ids[ii])
    # print(final_pareto_aoi, final_pareto_optical, final_pareto_screen, final_pareto_aft_scr, indvl_screen)
    for jj in range(len(wafer_ids[ii])):
        values = [int(final_pareto_aoi[jj]), final_pareto_heater[jj], final_pareto_optical[jj], len(final_pareto_aft_scr[jj]), indvl_screen['FVI'][jj][-1], indvl_screen['Chipping'][jj][-1]]
        # print(values[4][-1])
        sorted_pairs = sorted(zip(values, labels), reverse=True)
        sorted_values, sorted_labels = zip(*sorted_pairs)
        bar_plot(sorted_labels, sorted_values, ['TB004A', lot_ids[ii][jj], wafer_ids[ii][jj]], 'Final Pareto')


# ## Optical Fail Pareto
# labels = ['IL Fail', 'PDL Fail', 'ER Fail']
# for ii in range(len(lot_ids)):
#     _, count_opt = optical_pareto(ytec_df_lists[ii], lot_ids[ii], wafer_ids[ii])
#     for jj in range(len(wafer_ids[ii])):
#         values = [count_opt["f_il"][jj], count_opt["f_pdl"][jj], count_opt["f_er"][jj]]
#         sorted_pairs = sorted(zip(values, labels), reverse=True)
#         sorted_values, sorted_labels = zip(*sorted_pairs)
#         bar_plot(sorted_labels, sorted_values, [lot_ids[ii][jj], wafer_ids[ii][jj]], 'Optical Fail Pareto')

# ## Load screening delta excel
# for pat in file_path["scr_delta"]:
#     df = pd.read_excel(pat,sheet_name = 'Delta', header=6)
#     screen_f, idx, opt_fail, screen_no = scr.screen(df, lot_id, int(wafer_id))

# ## Obtain the failed numbers of dies
# fail_AOI = AOImap.AOI_map(file_path["AOI"])
# fail_heatres, hetres_idx = heat_res.heat_res(df_ytec, lot_id, wafer_id)
# fail_maxRvari, maxR_idx = MR.max_r_vari(df_ytec, lot_id, wafer_id)
# fail_PPi, ppi_idx = Ppi.Ppi(df_ytec, lot_id, wafer_id)
# _, res_maxR_ppi_fail = merge_unique(maxR_idx, hetres_idx, ppi_idx)
# # print(res_maxR_ppi_fail)


# fail_il_pdl, il_fail, pdl_fail, index_il_pdl = IL_PDL.IL_PDL(df_ytec, lot_id, wafer_id)
# fail_er, index_er = ER.ER(df_ytec, lot_id, wafer_id)
# _, er_il_pdl_fail = merge_unique(index_il_pdl, index_er)


# ### Final Pareto
# labels = ['AOI Fail', 'Heater Fail', 'Optical Fail', 'Optical Fail aft. Screen', 'FVI Fail', 'Chipping Fail']
# values = [fail_AOI, res_maxR_ppi_fail, er_il_pdl_fail, len(opt_fail), screen_f['FVI'], screen_f['Chipping']]
# sorted_pairs = sorted(zip(values, labels), reverse=True)
# sorted_values, sorted_labels = zip(*sorted_pairs)

# bar_plot(sorted_labels, sorted_values, id_list, 'Final Pareto')

# ### Optical Fail Pareto

# values = [il_fail, pdl_fail, fail_er]
# sorted_pairs = sorted(zip(values, labels), reverse=True)
# sorted_values, sorted_labels = zip(*sorted_pairs)

# bar_plot(sorted_labels, sorted_values, id_list, 'Optical Fail Pareto')



