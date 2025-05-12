#输出3个变量模拟的好的三个模式与三个坏模式
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
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
data_out=np.load('fig3_s.npy').reshape(5,180*360,25,order='A')#5var,180lat,360lon,25models+obs
#去掉'E3SM-1-0'  9，'FGOALS-f3-L'  10，CIESM  7' AWI-CM-1-1-MR'2
data_outt=np.zeros((5,180*360,21))
data_outt[:,:,0:2]=data_out[:,:,0:2]
data_outt[:,:,2:6]=data_out[:,:,3:7]
data_outt[:,:,6:7]=data_out[:,:,8:9]
data_outt[:,:,7:21]=data_out[:,:,11:25]
# print(len(data_out[4,:,24][np.isnan(data_out[4,:,24])]))#有1076个缺测
# print(len(data_out[0,:,24][np.isnan(data_out[0,:,24])]))#有0个缺测
season1=np.load('fig4_s2s.npy')#.reshape(5,180*360,21,order='A')#5var,latxlon,20model+AMMME
annual1=np.load('fig4_s3s.npy')#.reshape(5,180*360,21,order='A')
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
varnum=np.arange(0,3,1)
modelnum=np.arange(0,21,1)
axr = xr.DataArray(annual1, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])
sxr = xr.DataArray(season1, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])
weights=xr.DataArray(np.cos(np.deg2rad(olat)),coords=[olat],dims='lat')
axr=axr.weighted(weights)
sxr=sxr.weighted(weights)
annual=axr.mean(('lat','lon')).values
season=sxr.mean(('lat','lon')).values

data_out3=np.zeros((3,180*360,21))#我只需三个变量
data_out3[0,:,:]=data_outt[0,:,:]+data_outt[1,:,:]
data_out3[1,:,:]=data_outt[2,:,:]+data_outt[3,:,:]
data_out3[2,:,:]=data_outt[4,:,:]

data_out2=np.zeros((3,180*360,21))
for i in range(3):
        for k in range(21):
            data_out2[i,:,k]=(data_out3[i,:,k]-np.nanmean(data_out3[i,:,20]))/np.nanstd(data_out3[i,:,20])

def cal_csr(refsample1,sample1):
    df=pd.DataFrame({'ref':refsample1,'samp':sample1})
    corr = 1-df.corr().values#越小越好
    theta = np.arccos(corr[0,1])
    std = np.square(np.nanstd(sample1)-1)#越小越好
    rmse =np.sqrt(np.nanmean(np.square(np.subtract(refsample1,sample1))))#这样转换以后都是越小越好
    # print(np.sqrt(np.square(np.subtract(refsample,sample)).mean()))
    return corr[0,1],std,rmse

csri=np.zeros((21,3,5))#5varx4metircsx24model+AMME
for v in range(3):
    csri[:,v,3]=annual[v,:]
    csri[:,v,4]=season[v,:]
    for m in range(21):
        csri[m,v,0:3]=cal_csr(data_out2[v,:,20],data_out2[v,:,m])
    csri[20,v,0:3]=cal_csr(data_out2[v,:,20],np.mean(data_out2[v,:,0:21],1))
print(csri)
print('----')
csri=csri.reshape(21,15,order='A')
print(csri)
def cal_rank(arr):
    rank=np.zeros(arr.shape[0])
    index=np.argsort(-arr)#从大到小排序的索引
    rank[index]=np.arange(1,arr.shape[0]+1)#小的得分高，大的得分低
    return rank

csr_rank1=np.zeros([21,15])
for j in range(csri.shape[1]):
    csr_rank1[:,j]=cal_rank(csri[:,j])

csr_rank=np.zeros([21,21])
for v in range(3):
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

bm_wm=np.zeros([21,3])
for v in range(3):
    bm_wm[:,v]=csr_rank[:,7*v+3]+csr_rank[:,7*v+6]

print('------')
for v in range(3):
    print(v)
    index1=np.argsort(bm_wm[:,v])
    models_p=models
    models_p=np.array(models)[index1]
    print(models_p)
    print('------')


# ------
# 0
# ['FGOALS-g3' 'INM-CM4-8' 'NESM3' 'CAS-ESM2-0' 'INM-CM5-0' 'MRI-ESM2-0'
#  'MIROC6' 'GFDL-ESM4' 'ACCESS-ESM1-5' 'MPI-ESM1-2-LR' 'MPI-ESM1-2-HR'
#  'IPSL-CM6A-LR' 'BCC-CSM2-MR' 'KIOST-ESM' 'AMME' 'CanESM5' 'KACE-1-0-G'
#  'EC-Earth3-CC' 'CESM2-WACCM' 'CMCC-CM2-SR5' 'ACCESS-CM2']
# ------
# 1
# ['INM-CM4-8' 'IPSL-CM6A-LR' 'CAS-ESM2-0' 'FGOALS-g3' 'ACCESS-CM2'
#  'EC-Earth3-CC' 'KACE-1-0-G' 'INM-CM5-0' 'NESM3' 'CMCC-CM2-SR5'
#  'ACCESS-ESM1-5' 'MIROC6' 'KIOST-ESM' 'MRI-ESM2-0' 'AMME' 'CanESM5'
#  'BCC-CSM2-MR' 'MPI-ESM1-2-LR' 'MPI-ESM1-2-HR' 'CESM2-WACCM' 'GFDL-ESM4']
# ------
# 2
# ['ACCESS-CM2' 'CESM2-WACCM' 'CAS-ESM2-0' 'IPSL-CM6A-LR' 'FGOALS-g3'
#  'KACE-1-0-G' 'INM-CM4-8' 'BCC-CSM2-MR' 'ACCESS-ESM1-5' 'KIOST-ESM'
#  'INM-CM5-0' 'NESM3' 'GFDL-ESM4' 'EC-Earth3-CC' 'MRI-ESM2-0' 'AMME'
#  'CanESM5' 'CMCC-CM2-SR5' 'MPI-ESM1-2-HR' 'MIROC6' 'MPI-ESM1-2-LR']
# ------