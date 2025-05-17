#求五个变量的空间场ranking与时间场ranking的kendall执相关系数
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kendalltau
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,FixedLocator
import mpl_toolkits.axisartist as axisartist
from matplotlib.font_manager import FontProperties
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()

models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
csr_rank=xr.open_dataarray('../data/csr_vi_rank_score_21x35.nc')
print(csr_rank)
# sp_rank=np.zeros([5,5])
# sp_p=np.zeros([5,5])
# tm_rank=np.zeros([5,5])
# tm_p=np.zeros([5,5])
all_rank=np.zeros([5,5])
all_p=np.zeros([5,5])

all_rank=np.zeros([5,5])
_p=np.zeros([5,5])
for v1 in range(5):
    for v2 in range(5):
        a=csr_rank[:,5*v1+3]+csr_rank[:,5*v1+6]#csr+vi
        b=csr_rank[:,5*v2+3]+csr_rank[:,5*v2+6]#csr+vi
        all_rank[v1,v2],all_p[v1,v2] = kendalltau(a,b)
print('-----')
print(all_rank)
print(all_p<0.05)
varsname=['TOA SWCRF','TOA LWCRF','SFC SWCRF','SFC LWCRF','CLT']
####draw##################
fig = plt.figure(figsize=(3,3),dpi=400)
ax = sns.heatmap(all_rank, vmin=0,vmax=1,annot=all_rank,annot_kws={"fontsize":9},fmt='.2f',cmap='Greens',linewidths=0.5)
ax.set_adjustable('box')
ax.set_xticklabels(varsname,fontsize=9,rotation=90)
ax.set_yticklabels(varsname,fontsize=9,rotation=0)

# Add rectangles for cells where p < 0.05
for i in range(5):
    for j in range(5):
        if all_p[i,j] < 0.05:
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color="red", fill=False, linewidth=1))

plt.savefig('../fig/rank_kendall.png',bbox_inches='tight')