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
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, PathPatch
from matplotlib.path import Path
import mpl_toolkits.axisartist as axisartist
from matplotlib.font_manager import FontProperties

font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()
# models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']#20models
csri2=xr.open_dataarray('/data04/shiy/code_cloud/code_paper_7.13/code2/csr_vi_rank_score_21x28_revi.nc').values
print(csri2)
def cal_index(arr):
    index=np.argsort(-arr)#从大到小排序的索引
    return index

def cal_rank(arr):
    rank=np.zeros(arr.shape[0])
    index=np.argsort(-arr)#从大到小排序的索引
    rank[index]=np.arange(1,arr.shape[0]+1)#小的得分高，大的得分低
    return rank

# index1=(cal_index(np.mean(csri2[0:len(models),[3,10,17,24]],1))).astype('int')
# models_p1=np.array(models)[index1]

index2=(cal_index(np.mean(csri2[0:len(models),[6,13,20,27]],1))).astype('int')#based on VI
models_p2=np.array(models)[index2]
print(index2,models_p2)

csr_rank=np.zeros([21,28])
for j in range(csri2.shape[1]):
    csr_rank[:,j]=cal_rank(csri2[:,j])
csr_rank_temp=csr_rank.copy()
print(csr_rank)

# print(csr_rank_temp[:,[0,1,2,3,7,8,9,10,14,15,16,17,21,22,23,24]][index1,:])
# print(csr_rank_p1[0,3::])
####画图
# colors=plt.cm.nipy_spectral(np.linspace(0,1,25))
# fig.subplots_adjust(wspace=0.25,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig,ax=plt.subplots(1,1,figsize=(8,8),dpi=300)
def draw(ax,csr_rank_p1,xlabel,models_p,num):
    if num==0:
        sns.heatmap(csr_rank_p1, annot=True,fmt='.0f',cmap='RdYlGn',linewidths=0.5,ax=ax,cbar=False,cbar_kws={"format": "%.0f","ticks":[0,2,4,6,8,10,12,14,16,18,20]})#,linewidths=0.5,line
    else:
        sns.heatmap(csr_rank_p1, annot=True,fmt='.0f',cmap='RdYlGn',linewidths=0.5,ax=ax,cbar=True,cbar_kws={"format": "%.0f","ticks":[0,2,4,6,8,10,12,14,16,18,20]})#,linewidths=0.5,line
    xlen=csr_rank_p1.shape[1]
    ilen=len(xlabel)
    ax.set_adjustable('box')
    ax.set_xticks(np.arange(0,xlen,1))
    ax.set_yticks(np.linspace(0,20,21))
    ax.tick_params(axis="both", which="major", direction="in")
    ax.tick_params(axis="both", which="minor", direction="in")
    ax.xaxis.set_major_locator(FixedLocator(np.arange(0,xlen,3)))#设置y主坐标间隔 1
    ax.xaxis.set_minor_locator(FixedLocator(np.arange(0,xlen,1)))
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
    ax.set_yticklabels(models_p,minor=True,fontsize=16)
    ax.tick_params(axis='y',labelrotation=0)
    ax.set_xticks(np.arange(0.5,xlen,1),minor=True)
    ax.set_xticklabels(xlabel,minor=True,fontsize=14)
    # ax.set_title("a) Toa net crf",loc='left',pad=10)
    ax.text(ilen/8, 26.5-4.3,"TOA SWCRF",ha='center',va='center',fontsize=13,rotation=0)
    ax.text(ilen/8+ilen/4, 26.5-4.3,"TOA LWCRF",ha='center',va='center',fontsize=13,rotation=0)
    ax.text(ilen/8+2*ilen/4, 26.5-4.3,"ATM SWCRF",ha='center',va='center',fontsize=13,rotation=0)
    ax.text(ilen/8+3*ilen/4, 26.5-4.3,"ATM LWCRF",ha='center',va='center',fontsize=13,rotation=0)
    # ax.text(31.5, 26.5-4,"CLT",ha='center',va='center',fontsize=16,rotation=0)
    ## 图形坐标范围是 [0,1]（左到右，下到上）
    arrow_x = 0.0001  # 距离左侧2%的位置（整个图的左侧）
    arrow_start_y = 0.05  # 箭头底部在图形的10%高度处
    arrow_end_y = 0.95    # 箭头顶部在图形的90%高度处
    cmap = LinearSegmentedColormap.from_list('gradient', ['green', 'yellow', 'red'])

    # 绘制箭头（使用图形坐标转换）
    arrow = FancyArrowPatch(
        (arrow_x, arrow_end_y),  # 起点（图形坐标）
        (arrow_x, arrow_start_y),    # 终点（图形坐标）
        arrowstyle='simple,tail_width=8,head_width=14,head_length=40',
        color='grey',
        linewidth=2,
        zorder=10,
        transform=fig.transFigure  # 使用图形坐标系统
    )
    fig.add_artist(arrow)  # 添加到fig而不是ax

    # 添加箭头文字标注（同样使用图形坐标）
    fig.text(
        arrow_x - 0.09,  # 文字在箭头左侧
        arrow_start_y+0.1,
        'Better',
        ha='center',
        va='center',
        fontsize=25,
        fontweight='bold',
        transform=fig.transFigure
    )

    fig.text(
        arrow_x - 0.09,
        arrow_end_y-0.1,
        'Worse',
        ha='center',
        va='center',
        fontsize=25,
        fontweight='bold',
        transform=fig.transFigure
    )

# draw(ax[0],csr_rank_temp[:,[0,1,2,3,7,8,9,10,14,15,16,17,21,22,23,24]][index1,:],xlabel=['c','s','r','csr']*4,models_p=models_p1,num=0)
draw(ax,csr_rank_temp[index2][:,[4,5,6,11,12,13,18,19,20,25,26,27]],xlabel=['avi','svi','vi']*4,models_p=np.array(models)[index2],num=1)#[index2,:]
# Set colorbar tick font size and position
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=16)
plt.tight_layout(rect=[0, 0, 0.98, 1]) # Adjust layout to bring colorbar even closer

plt.savefig('../fig/heatmap_model_score.pdf',bbox_inches='tight')
