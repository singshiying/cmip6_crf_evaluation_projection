import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
import json

#读取feedback and forcing data
f = open('/data04/shiy/code_cloud/feedback_cmip6/zk_cmip56/cmip56_forcing_feedback_ecs-master/cmip56_forcing_feedback_ecs.json','r')
data = json.load(f)

models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
print(len(models))
#20个模式
ECS=np.zeros(len(models))
CF=np.zeros(len(models))
for m in range(len(models)):
    if models[m]=='CAS-ESM2-0':
        ECS[m]=3.45
        CF[m]=0.47
    elif models[m]=='KIOST-ESM':
        ECS[m]=3.36
        CF[m]=0
    else:
        ECS[m]=data['CMIP6'][models[m]]['r1i1p1f1']['ECS']
        CF[m]=data['CMIP6'][models[m]]['r1i1p1f1']['CLD']


#某变量的rank score与cloud feedback是否具有相关性
csri_rank=xr.open_dataarray('../data/csr_vi_rank_score_21x35.nc')

csr2=np.mean(csri_rank[:20,[3,10,17,24,31]],1)
vi2=np.mean(csri_rank[:20,[6,13,20,27,34]],1)
svi2=np.mean(csri_rank[:20,[5,12,19,26,33]],1)
csr_vi2=np.mean(csri_rank[:20,[3,6,10,13,17,20,24,27,31,34]],1)
###based on crf
csr=np.mean(csri_rank[:20,[3,10,17,24]],1)
vi=np.mean(csri_rank[:20,[6,13,20,27]],1)
svi=np.mean(csri_rank[:20,[5,12,19,26]],1)
csr_vi=np.mean(csri_rank[:20,[3,6,10,13,17,20,24,27]],1)
###based on clt
csr1=np.mean(csri_rank[:20,[31]],1)
vi1=np.mean(csri_rank[:20,[34]],1)
svi1=np.mean(csri_rank[:20,[33]],1)
csr_vi1=np.mean(csri_rank[:20,[31,34]],1)

print('csr,cf',np.corrcoef(csr,CF)[0,1])
print('vi,cf',np.corrcoef(vi,CF)[0,1])
print('svi,cf',np.corrcoef(svi,CF)[0,1])
print('csr_vi,cf',np.corrcoef(csr_vi,CF)[0,1])

print('csr1,cf',np.corrcoef(csr1,CF)[0,1])
print('vi1,cf',np.corrcoef(vi1,CF)[0,1])
print('svi1,cf',np.corrcoef(svi1,CF)[0,1])
print('csr_vi1,cf',np.corrcoef(csr_vi1,CF)[0,1])

print('csr2,cf',np.corrcoef(csr2,CF)[0,1])
print('vi2,cf',np.corrcoef(vi2,CF)[0,1])
print('svi2,cf',np.corrcoef(svi2,CF)[0,1])
print('csr_vi2,cf',np.corrcoef(csr_vi2,CF)[0,1])