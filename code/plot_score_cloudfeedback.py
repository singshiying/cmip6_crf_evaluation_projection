import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
import json
from scipy import stats
from matplotlib.font_manager import FontProperties
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()
plt.rcParams['figure.figsize']=(3*2,3*2)

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
csri_rank_60NS=xr.open_dataarray('../data/csr_vi_rank_score_21x35_60NS.nc')
csri_rank_modis=xr.open_dataarray('../data/csr_vi_rank_score_21x35_modis.nc')
csri_rank_60NS_modis=xr.open_dataarray('../data/csr_vi_rank_score_21x35_60NS_modis.nc')

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
############################################
####60s-60N
csr2_60NS=np.mean(csri_rank_60NS[:20,[3,10,17,24,31]],1)
vi2_60NS=np.mean(csri_rank_60NS[:20,[6,13,20,27,34]],1)
svi2_60NS=np.mean(csri_rank_60NS[:20,[5,12,19,26,33]],1)
csr_vi2_60NS=np.mean(csri_rank_60NS[:20,[3,6,10,13,17,20,24,27,31,34]],1)
###based on crf
csr_60NS=np.mean(csri_rank_60NS[:20,[3,10,17,24]],1)
vi_60NS=np.mean(csri_rank_60NS[:20,[6,13,20,27]],1)
svi_60NS=np.mean(csri_rank_60NS[:20,[5,12,19,26]],1)
csr_vi_60NS=np.mean(csri_rank_60NS[:20,[3,6,10,13,17,20,24,27]],1)
###based on clt
csr1_60NS=np.mean(csri_rank_60NS[:20,[31]],1)
vi1_60NS=np.mean(csri_rank_60NS[:20,[34]],1)
svi1_60NS=np.mean(csri_rank_60NS[:20,[33]],1)
csr_vi1_60NS=np.mean(csri_rank_60NS[:20,[31,34]],1)
####################################################
###clt is not from isccp but from modis
csr2_modis=np.mean(csri_rank_modis[:20,[3,10,17,24,31]],1)
vi2_modis=np.mean(csri_rank_modis[:20,[6,13,20,27,34]],1)
svi2_modis=np.mean(csri_rank_modis[:20,[5,12,19,26,33]],1)
csr_vi2_modis=np.mean(csri_rank_modis[:20,[3,6,10,13,17,20,24,27,31,34]],1)
###based on crf
csr_modis=np.mean(csri_rank_modis[:20,[3,10,17,24]],1)
vi_modis=np.mean(csri_rank_modis[:20,[6,13,20,27]],1)
svi_modis=np.mean(csri_rank_modis[:20,[5,12,19,26]],1)
csr_vi_modis=np.mean(csri_rank_modis[:20,[3,6,10,13,17,20,24,27]],1)
###based on clt
csr1_modis=np.mean(csri_rank_modis[:20,[31]],1)
vi1_modis=np.mean(csri_rank_modis[:20,[34]],1)
svi1_modis=np.mean(csri_rank_modis[:20,[33]],1)
csr_vi1_modis=np.mean(csri_rank_modis[:20,[31,34]],1)
############################################
####60s-60N and clt from modis not ISCCP
csr2_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[3,10,17,24,31]],1)
vi2_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[6,13,20,27,34]],1)
svi2_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[5,12,19,26,33]],1)
csr_vi2_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[3,6,10,13,17,20,24,27,31,34]],1)
###based on crf
csr_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[3,10,17,24]],1)
vi_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[6,13,20,27]],1)
svi_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[5,12,19,26]],1)
csr_vi_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[3,6,10,13,17,20,24,27]],1)
###based on clt
csr1_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[31]],1)
vi1_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[34]],1)
svi1_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[33]],1)
csr_vi1_60NS_modis=np.mean(csri_rank_60NS_modis[:20,[31,34]],1)

print('++++++based on global crf+++++++')
print('csr,cf',np.corrcoef(csr,CF)[0,1])
print('vi,cf',np.corrcoef(vi,CF)[0,1])
print('svi,cf',np.corrcoef(svi,CF)[0,1])
print('csr_vi,cf',np.corrcoef(csr_vi,CF)[0,1])
print('++++++based on global clt+++++++')
print('csr1,cf',np.corrcoef(csr1,CF)[0,1])
print('vi1,cf',np.corrcoef(vi1,CF)[0,1])
print('svi1,cf',np.corrcoef(svi1,CF)[0,1])
print('csr_vi1,cf',np.corrcoef(csr_vi1,CF)[0,1])
print('++++++based on global clt and crf+++++++')
print('csr2,cf',np.corrcoef(csr2,CF)[0,1])
print('vi2,cf',np.corrcoef(vi2,CF)[0,1])
print('svi2,cf',np.corrcoef(svi2,CF)[0,1])
print('csr_vi2,cf',np.corrcoef(csr_vi2,CF)[0,1])
print('--------------------------------')
print('csr_60NS,cf',np.corrcoef(csr_60NS,CF)[0,1])
print('vi_60NS,cf',np.corrcoef(vi_60NS,CF)[0,1])
print('svi_60NS,cf',np.corrcoef(svi_60NS,CF)[0,1])
print('csr_vi_60NS,cf',np.corrcoef(csr_vi_60NS,CF)[0,1])

print('csr1_60NS,cf',np.corrcoef(csr1_60NS,CF)[0,1])
print('vi1_60NS,cf',np.corrcoef(vi1_60NS,CF)[0,1])
print('svi1_60NS,cf',np.corrcoef(svi1_60NS,CF)[0,1])
print('csr_vi1_60NS,cf',np.corrcoef(csr_vi1_60NS,CF)[0,1])

print('csr2_60NS,cf',np.corrcoef(csr2_60NS,CF)[0,1])
print('vi2_60NS,cf',np.corrcoef(vi2_60NS,CF)[0,1])
print('svi2_60NS,cf',np.corrcoef(svi2_60NS,CF)[0,1])
print('csr_vi2_60NS,cf',np.corrcoef(csr_vi2_60NS,CF)[0,1])

print('--------------------------------')
print('csr_modis,cf',np.corrcoef(csr_modis,CF)[0,1])
print('vi_modis,cf',np.corrcoef(vi_modis,CF)[0,1])
print('svi_modis,cf',np.corrcoef(svi_modis,CF)[0,1])
print('csr_vi_modis,cf',np.corrcoef(csr_vi_modis,CF)[0,1])

print('csr1_modis,cf',np.corrcoef(csr1_modis,CF)[0,1])
print('vi1_modis,cf',np.corrcoef(vi1_modis,CF)[0,1])
print('svi1_modis,cf',np.corrcoef(svi1_modis,CF)[0,1])
print('csr_vi1_modis,cf',np.corrcoef(csr_vi1_modis,CF)[0,1])

print('csr2_modis,cf',np.corrcoef(csr2_modis,CF)[0,1])
print('vi2_modis,cf',np.corrcoef(vi2_modis,CF)[0,1])
print('svi2_modis,cf',np.corrcoef(svi2_modis,CF)[0,1])
print('csr_vi2_modis,cf',np.corrcoef(csr_vi2_modis,CF)[0,1])
print('--------------------------------')
print('csr_60NS_modis,cf',np.corrcoef(csr_60NS_modis,CF)[0,1])
print('vi_60NS_modis,cf',np.corrcoef(vi_60NS_modis,CF)[0,1])
print('svi_60NS_modis,cf',np.corrcoef(svi_60NS_modis,CF)[0,1])
print('csr_vi_60NS_modis,cf',np.corrcoef(csr_vi_60NS_modis,CF)[0,1])

print('csr1_60NS_modis,cf',np.corrcoef(csr1_60NS_modis,CF)[0,1])
print('vi1_60NS_modis,cf',np.corrcoef(vi1_60NS_modis,CF)[0,1])
print('svi1_60NS_modis,cf',np.corrcoef(svi1_60NS_modis,CF)[0,1])
print('csr_vi1_60NS_modis,cf',np.corrcoef(csr_vi1_60NS_modis,CF)[0,1])

print('csr2_60NS_modis,cf',np.corrcoef(csr2_60NS_modis,CF)[0,1])
print('vi2_60NS_modis,cf',np.corrcoef(vi2_60NS_modis,CF)[0,1])
print('svi2_60NS_modis,cf',np.corrcoef(svi2_60NS_modis,CF)[0,1])
print('csr_vi2_60NS_modis,cf',np.corrcoef(csr_vi2_60NS_modis,CF)[0,1])
csr_rank_combined = np.concatenate((csri_rank[:,[3,6,10,13,17,20,24,27,34]], csri_rank_60NS[:,[31]]), axis=1)
# index1=np.argsort(np.mean(csr_rank_combined, axis=1))
# models_p1=np.array(models)[index1]
# csr_rank_temp=csri_rank.copy()
# csr_rank_temp[:,28:31]=csri_rank_60NS[:,28:31]
# csr_rank_p1=csr_rank_temp[index1,:]


# 计算置信区间


# 计算置信区间
def confidence_interval(x, y_pred, x_new):
    n = len(x)
    x_mean = np.mean(x)
    # 计算预测标准误差
    sum_sq = np.sum((y - (slope * x + intercept)) ** 2)
    std_err = np.sqrt(sum_sq / (n-2))
    # 计算置信区间
    x_new_mean = np.mean(x_new)
    std_interval = std_err * np.sqrt(1/n + (x_new - x_new_mean)**2 / 
                                   np.sum((x - x_mean)**2))
    return y_pred, y_pred - 1.96*std_interval, y_pred + 1.96*std_interval

avg_rank=np.mean(csr_rank_combined,1)
print(avg_rank.shape)
# 计算回归线
slope, intercept, r_value, p_value, std_err = stats.linregress( avg_rank[0:20],ECS)
# 创建预测值
x = np.linspace(avg_rank.min(), avg_rank.max(),20)
y = slope * x + intercept
# 添加置信区间
_, lower, upper = confidence_interval(avg_rank[0:20], y, x)

# 计算回归线
slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress( avg_rank[0:20],CF)
# 创建预测值
x2 = np.linspace(avg_rank.min(), avg_rank.max(),20)
y2 = slope2 * x2 + intercept2
# 添加置信区间
_, lower2, upper2 = confidence_interval(avg_rank[0:20], y2, x2)

colors=plt.cm.tab20(np.linspace(0,1,20))
fig,ax=plt.subplots(1,2,figsize=(6,3.5),dpi=300)
plt.subplots_adjust(wspace=0.4) # Adjust spacing between subplots
for m,mo in enumerate(models):
    ax[0].scatter(avg_rank[m],ECS[m],color=colors[m])
    ax[1].scatter(avg_rank[m],CF[m],color=colors[m],label=models[m])
ax[0].plot(x, y, '-')
ax[1].plot(x2, y2, '-')
ax[0].fill_between(x, lower,upper, alpha=0.2,label='95% confidence interval')
ax[1].fill_between(x2, lower2,upper2, alpha=0.2,label='95% confidence interval')
ax[0].set_xlabel('average ranking scores',fontsize=9)
ax[1].set_xlabel('average ranking scores',fontsize=9)
ax[0].set_ylabel('ECS (K)',fontsize=9)
ax[1].set_ylabel('cloud feedback (W/m$^{2}$)',fontsize=9)
ax[0].set_title(f'correlation coefficient:{np.corrcoef(avg_rank[0:20],ECS)[0,1]:.2f}',fontsize=9)
ax[1].set_title(f'correlation coefficient:{np.corrcoef(avg_rank[0:20],CF)[0,1]:.2f}',fontsize=9)
ax[1].legend(bbox_to_anchor=(1,1.01),fontsize=7)
plt.savefig('../fig/score_cloudfeedback.svg',bbox_inches='tight')