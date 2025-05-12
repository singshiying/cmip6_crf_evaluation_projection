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
models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
csr_rank=xr.open_dataarray('./csr_vi_rank_score_21x35.nc')
print(csr_rank)
sp_rank=np.zeros([5,5])
sp_p=np.zeros([5,5])
tm_rank=np.zeros([5,5])
tm_p=np.zeros([5,5])
for v1 in range(5):
    for v2 in range(5):
        a=csr_rank[:,5*v1+3]
        b=csr_rank[:,5*v2+3]
        sp_rank[v1,v2],sp_p[v1,v2] = kendalltau(a,b)
        a=csr_rank[:,5*v1+6]
        b=csr_rank[:,5*v2+6]
        tm_rank[v1,v2],tm_p[v1,v2] = kendalltau(a,b)
print('-----')
print(sp_rank)
print(tm_rank)
varsname=['Toa sw crf','Toa lw crf','Sfc sw crf','Sfc lw crf','CLT']
####画图
# fig = plt.figure(figsize=(14,6))
grid_kws = {"height_ratios": [0.5], "width_ratios": [.45,.45,.05]}
# fig.subplots_adjust(wspace=0.25,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig, [ax1,ax2, cbar_ax] = plt.subplots(1,3, gridspec_kw=grid_kws)
fig.set_figheight(8)
fig.set_figwidth(14)
fig.set_dpi(300)

# clev=[-1,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,1]
ax1 = sns.heatmap(sp_rank, vmin=0,vmax=0.5,annot=sp_rank,annot_kws={"fontsize":14},fmt='.2f',cmap='Greens',linewidths=0.5,ax=ax1,cbar_ax=cbar_ax,cbar=False)#,linewidths=0.5,line
ax1.set_title('a) Spatial KCC',loc='left',fontsize=20,pad=13)
ax1.set_adjustable('box')
ax1.set_xticklabels(varsname,fontsize=20,rotation=90)
ax1.set_yticklabels(varsname,fontsize=20,rotation=0)
# ax1.add_patch(plt.Rectangle((0, 2), 1, 1, color="black", fill=False, linewidth=2))
# ax1.add_patch(plt.Rectangle((1, 2), 1, 1, color="black", fill=False, linewidth=2))
# ax1.add_patch(plt.Rectangle((2, 1), 1, 1, color="black", fill=False, linewidth=2))
# ax1.add_patch(plt.Rectangle((2, 0), 1, 1, color="black", fill=False, linewidth=2))

ax2 = sns.heatmap(tm_rank, vmin=0,vmax=0.5,annot=tm_rank,annot_kws={"fontsize":14},fmt='.2f',cmap='Greens',linewidths=0.5,ax=ax2,cbar_ax=cbar_ax,cbar=True,cbar_kws={'extend': 'max'})#,linewidths=0.5,line
ax2.set_title('b) Temporal KCC',loc='left',fontsize=20,pad=13)
ax2.set_adjustable('box')
ax2.set_yticks([])
ax2.set_xticklabels(varsname,fontsize=20,rotation=90)

# cbar = ax2.collections[0].colorbar
# cbar.set_ticks([-0.1,0,0.1,0.2,0.3,0.4,0.5])
# ax2.add_patch(plt.Rectangle((0, 2), 1, 1, color="black", fill=False, linewidth=2))
# ax2.add_patch(plt.Rectangle((1, 2), 1, 1, color="black", fill=False, linewidth=2))
# ax2.add_patch(plt.Rectangle((2, 1), 1, 1, color="black", fill=False, linewidth=2))
# ax2.add_patch(plt.Rectangle((2, 0), 1, 1, color="black", fill=False, linewidth=2))
# ax2.add_patch(plt.Rectangle((3, 4), 1, 1, color="black", fill=False, linewidth=2))
# ax2.add_patch(plt.Rectangle((4, 3), 1, 1, color="black", fill=False, linewidth=2))
# ax2.set_yticklabels(varsname,fontsize=14,rotation=0)
plt.savefig('fig4_s3_v2.png',bbox_inches='tight')
