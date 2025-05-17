import numpy as np
import xarray as xr
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
print(len(models))
# csr_rank=xr.open_dataarray('./../data/csr_vi_rank_score_21x35.nc')
csr_rank=xr.open_dataarray('./../data/csr_vi_rank_score_21x35_60NS.nc')
rank=np.zeros((21,3))#21model csr\vi\csr_vi
##all
rank[:,0]=np.mean(csr_rank[:,[3,10,17,24,31]],1)
rank[:,1]=np.mean(csr_rank[:,[6,13,20,27,34]],1)
rank[:,2]=np.mean(csr_rank[:,[3,6,10,13,17,20,24,27,31,34]],1)

##crf
# rank[:,0]=np.mean(csr_rank[:,[3,10,17,24]],1)
# rank[:,1]=np.mean(csr_rank[:,[6,13,20,27]],1)
# rank[:,2]=np.mean(csr_rank[:,[3,6,10,13,17,20,24,27]],1)
##clt
# rank[:,0]=np.mean(csr_rank[:,[31]],1)
# rank[:,1]=np.mean(csr_rank[:,[34]],1)
# rank[:,2]=np.mean(csr_rank[:,[31,34]],1)


index1=np.argsort(rank,0)
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