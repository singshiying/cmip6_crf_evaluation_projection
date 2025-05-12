#画热力图
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
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
# models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
###############读取气候态
data_out=np.load('fig3_s.npy').reshape(5,180*360,25,order='A')#5var,180lat,360lon,25models+obs
#去掉'E3SM-1-0'  9，'FGOALS-f3-L'  10，CIESM  7' AWI-CM-1-1-MR'2
data_outt=np.zeros((5,180*360,21))
data_outt[:,:,0:2]=data_out[:,:,0:2]
data_outt[:,:,2:6]=data_out[:,:,3:7]
data_outt[:,:,6:7]=data_out[:,:,8:9]
data_outt[:,:,7:21]=data_out[:,:,11:25]
###################读取SVI AVI
# print(len(data_out[4,:,24][np.isnan(data_out[4,:,24])]))#有1076个缺测
# print(len(data_out[0,:,24][np.isnan(data_out[0,:,24])]))#有0个缺测
season1=np.load('fig4_s2_v2.npy')#.reshape(5,180*360,21,order='A')#5var,latxlon,20model+AMMME
annual1=np.load('fig4_s3_v2.npy')#.reshape(5,180*360,21,order='A')
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
varnum=np.arange(0,5,1)
modelnum=np.arange(0,21,1)
axr = xr.DataArray(annual1, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])
sxr = xr.DataArray(season1, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])
weights=xr.DataArray(np.cos(np.deg2rad(olat)),coords=[olat],dims='lat')
axr=axr.weighted(weights)
sxr=sxr.weighted(weights)
annual=axr.mean(('lat','lon')).values
season=sxr.mean(('lat','lon')).values
# annual[:,0:2]=annual2[:,0:2]
# annual[:,2:6]=annual2[:,3:7]
# annual[:,6:7]=annual2[:,8:9]
# annual[:,7:21]=annual2[:,11:25]
#####################气候态normlize
data_out2=np.zeros((5,180*360,21))
for i in range(5):
        for k in range(21):
            data_out2[i,:,k]=(data_outt[i,:,k]-np.nanmean(data_outt[i,:,20]))/np.nanstd(data_outt[i,:,20])

#计算cor，std，rmse
def cal_csr(refsample1,sample1):
    df=pd.DataFrame({'ref':refsample1,'samp':sample1})
    corr = 1-df.corr().values#越小越好
    theta = np.arccos(corr[0,1])
    std = np.square(np.nanstd(sample1)-1)#越小越好
    rmse =np.sqrt(np.nanmean(np.square(np.subtract(refsample1,sample1))))#这样转换以后都是越小越好
    # print(np.sqrt(np.square(np.subtract(refsample,sample)).mean()))
    return corr[0,1],std,rmse

csri=np.zeros((21,5,5))#20model+obsx5varx5metric
for v in range(5):
    csri[:,v,3]=annual[v,:]
    csri[:,v,4]=season[v,:]
    for m in range(21):
        csri[m,v,0:3]=cal_csr(data_out2[v,:,20],data_out2[v,:,m])
    csri[20,v,0:3]=cal_csr(data_out2[v,:,20],np.mean(data_out2[v,:,0:21],1))
print(csri)
print('----')
csri=csri.reshape(21,25,order='A')
print(csri)
def cal_rank(arr):
    rank=np.zeros(arr.shape[0])
    index=np.argsort(-arr)#从大到小排序的索引
    rank[index]=np.arange(1,arr.shape[0]+1)#小的得分高，大的得分低
    return rank

csr_rank1=np.zeros([21,25])
for j in range(csri.shape[1]):
    csr_rank1[:,j]=cal_rank(csri[:,j])
######################################
####csr_rank是最后呈现的结果
csr_rank=np.zeros([21,35])
for v in range(5):
    csr_rank[:,7*v:(7*v+3)]=csr_rank1[:,5*v:(5*v+3)]
    rank=np.zeros(21)
    temp=np.mean(csr_rank1[:,5*v:(5*v+3)],1)
    index=np.argsort(temp)
    rank[index]=np.arange(1,22)
    csr_rank[:,7*v+3]=rank
    csr_rank[:,(7*v+4):(7*v+6)]=csr_rank1[:,(5*v+3):(5*v+5)]
    temp=np.mean(csr_rank1[:,(5*v+3):(5*v+5)],1)
    index=np.argsort(temp)
    rank[index]=np.arange(1,22)
    csr_rank[:,7*v+6]=rank

print('----')
print(np.mean(csr_rank[:,[3,6,10,13,17,20,24,27,31,34]],1))
#####依据总分数从小到大排序
index1=np.argsort(np.mean(csr_rank[:,[3,6,10,13,17,20,24,27,31,34]],1))
models_p1=models
models_p1=np.array(models)[index1]
csr_rank_p1=csr_rank[index1,:]
csr_rank_xr=xr.DataArray(csr_rank,coords=[models,np.arange(0,35,1)],dims=['models','5varx7metric'])
csr_rank_xr.to_netcdf('./csr_vi_rank_score_21x35.nc')
# print(csr_rank_p1[0,3::])
####画图
# colors=plt.cm.nipy_spectral(np.linspace(0,1,25))
fig = plt.figure(figsize=(14,8))
# fig.subplots_adjust(wspace=0.25,hspace=0.05,right=0.9,top=0.8,bottom=0.1)

ax=fig.add_subplot(111)
ax = sns.heatmap(csr_rank_p1, annot=True,fmt='.0f',cmap='RdYlGn',linewidths=0.5,cbar=True,cbar_kws={"format": "%.0f","ticks":[0,2,4,6,8,10,12,14,16,18,20]})#,linewidths=0.5,line
ax.set_adjustable('box')
ax.set_xticks(np.arange(0,35,1))
ax.set_yticks(np.linspace(0,20,21))
ax.tick_params(axis="both", which="major", direction="in")
ax.tick_params(axis="both", which="minor", direction="in")
ax.xaxis.set_major_locator(FixedLocator(np.arange(0,35,7)))#设置y主坐标间隔 1
ax.xaxis.set_minor_locator(FixedLocator(np.arange(0,35,1)))
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
ax.set_yticklabels(models_p1,minor=True,fontsize=14)
ax.tick_params(axis='y',labelrotation=0)
xlabel=['c','s','r','csr','avi','svi','vi']*5
ax.set_xticks(np.arange(0.5,35,1),minor=True)
ax.set_xticklabels(xlabel,minor=True)
# ax.set_title("a) Toa net crf",loc='left',pad=10)
ax.text(3.5, 26.5-4,"TOA SWCRE",ha='center',va='center',fontsize=14,rotation=0)
ax.text(10.5, 26.5-4,"TOA LWCRE",ha='center',va='center',fontsize=14,rotation=0)
ax.text(17.5, 26.5-4,"SFC SWCRE",ha='center',va='center',fontsize=14,rotation=0)
ax.text(24.5, 26.5-4,"SFC LWCRE",ha='center',va='center',fontsize=14,rotation=0)
ax.text(31.5, 26.5-4,"CLT",ha='center',va='center',fontsize=14,rotation=0)

plt.savefig('fig4_s2_v2.png',bbox_inches='tight')

