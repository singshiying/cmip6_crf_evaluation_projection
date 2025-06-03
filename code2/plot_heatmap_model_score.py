#计算csrAiSirank并画热力图
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,FixedLocator
import mpl_toolkits.axisartist as axisartist
from matplotlib.font_manager import FontProperties
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()
# models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']#20models
csr_rank=xr.open_dataarray('./csr_vi_rank_score_21x28.nc').values
index1=np.argsort(np.mean(csr_rank[:,[3,6,10,13,17,20,24,27]],1))
models_p1=np.array(models)[index1]
csr_rank_temp=csr_rank.copy()
csr_rank_p1=csr_rank_temp[index1,:]
# print(csr_rank_p1[0,3::])
####画图
# colors=plt.cm.nipy_spectral(np.linspace(0,1,25))
fig = plt.figure(figsize=(14,8),dpi=300)
# fig.subplots_adjust(wspace=0.25,hspace=0.05,right=0.9,top=0.8,bottom=0.1)

ax=fig.add_subplot(111)
ax = sns.heatmap(csr_rank_p1, annot=True,fmt='.0f',cmap='RdYlGn',linewidths=0.5,cbar=True,cbar_kws={"format": "%.0f","ticks":[0,2,4,6,8,10,12,14,16,18,20]})#,linewidths=0.5,line
ax.set_adjustable('box')
ax.set_xticks(np.arange(0,28,1))
ax.set_yticks(np.linspace(0,20,21))
ax.tick_params(axis="both", which="major", direction="in")
ax.tick_params(axis="both", which="minor", direction="in")
ax.xaxis.set_major_locator(FixedLocator(np.arange(0,28,7)))#设置y主坐标间隔 1
ax.xaxis.set_minor_locator(FixedLocator(np.arange(0,28,1)))
ax.yaxis.set_major_locator(FixedLocator(np.linspace(0,21,22)))#设置y主坐标间隔 1
ax.xaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
# ax.xaxis.grid(True,which='minor',color='black',linestyle='--')#major,color='black'
ax.yaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
ax.tick_params(bottom=False,top=False,left=False,right=False)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['top'].set_visible(True)
ax.spines['left'].set_linewidth(1.5)
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['right'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_color('black')
ax.set_yticks(np.arange(0.5,21,1),minor=True)
ax.set_yticklabels(models_p1,minor=True,fontsize=16)
ax.tick_params(axis='y',labelrotation=0)
xlabel=['c','s','r','csr','avi','svi','vi']*4
ax.set_xticks(np.arange(0.5,28,1),minor=True)
ax.set_xticklabels(xlabel,minor=True,fontsize=14)
# ax.set_title("a) Toa net crf",loc='left',pad=10)
ax.text(3.5, 26.5-4,"TOA SWCRF",ha='center',va='center',fontsize=16,rotation=0)
ax.text(10.5, 26.5-4,"TOA LWCRF",ha='center',va='center',fontsize=16,rotation=0)
ax.text(17.5, 26.5-4,"ATM SWCRF",ha='center',va='center',fontsize=16,rotation=0)
ax.text(24.5, 26.5-4,"ATM LWCRF",ha='center',va='center',fontsize=16,rotation=0)
# ax.text(31.5, 26.5-4,"CLT",ha='center',va='center',fontsize=16,rotation=0)

# Set colorbar tick font size and position
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=16)
plt.tight_layout(rect=[0, 0, 0.98, 1]) # Adjust layout to bring colorbar even closer

plt.savefig('../fig2/heatmap_model_score.svg',bbox_inches='tight')
