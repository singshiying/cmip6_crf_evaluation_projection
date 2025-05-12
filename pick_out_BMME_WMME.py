import numpy as np
import xarray as xr
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
print(len(models))
csr_rank=xr.open_dataarray('./csr_svi_rank_score_21x25.nc')
csri_rank=np.zeros((21,5))
for v in range(5):
    csri_rank[:,v]=csr_rank[:,5*v+3]+csr_rank[:,5*v+4]
index1=np.argsort(csri_rank,0)
# 将索引矩阵转换为字符串矩阵（用模式名字替换索引）
models_matrix = []
for row in index1:
    string_row = [models[index] for index in row]
    models_matrix.append(string_row)
print(models_matrix)

with open("BMME_WMME.txt", "w") as file:
    for row in models_matrix:
        # 自定义格式：去掉方括号和引号
        line = " ".join(row)  # 用空格分隔
        # 或者 line = ", ".join(row)  # 用逗号和空格分隔
        file.write(line + "\n")