#计算南北纬60度之间的csrvi rank score
#只有clt取60NS crf取全球
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re

models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']#20models
###############读取气候态
data_out=np.load('../fig1.npy')#.reshape(5,180*360,21,order='A')
#20models+obs
###################读取SVI AVI
season1=np.load('../fig4_s2_v2.npy')#.reshape(5,180*360,21,order='A')#5var,latxlon,20model+AMMME
annual1=np.load('../fig4_s3_v2.npy')#.reshape(5,180*360,21,order='A')
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
varnum=np.arange(0,5,1)
modelnum=np.arange(0,21,1)
data_out_xr=xr.DataArray(data_out,coords=[varnum,olat,olon,modelnum],dims=['varnum','lat','lon','modelnum']).loc[:,-60:60,:,:]
axr = xr.DataArray(annual1, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])#.loc[:,-60:60,:,:]
sxr = xr.DataArray(season1, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])#.loc[:,-60:60,:,:]
weights1=xr.DataArray(np.cos(np.deg2rad(olat[(olat<60) & (olat>-60)])),coords=[olat[(olat<60) & (olat>-60)]],dims='lat')
weights=xr.DataArray(np.cos(np.deg2rad(olat)),coords=[olat],dims='lat')
annual=axr.weighted(weights).mean(('lat','lon')).values
season=sxr.weighted(weights).mean(('lat','lon')).values

annual1=axr.loc[:,-60:60,:,:].weighted(weights1).mean(('lat','lon')).values
season1=sxr.loc[:,-60:60,:,:].weighted(weights1).mean(('lat','lon')).values

#####################气候态normlize
###crf
data_out2=np.zeros((4,180*360,21))
data_out2_t=data_out.reshape(5,180*360,21,order='A')

for i in range(4):
        for k in range(21):
            data_out2[i,:,k]=(data_out2_t[i,:,k]-np.nanmean(data_out2_t[i,:,20]))/np.nanstd(data_out2_t[i,:,20])
###clt
data_out3=np.zeros((120*360,21))##只有clt取60NS
data_out_3t=data_out_xr.values.reshape(5,120*360,21,order='A')
for k in range(21):
    data_out3[:,k]=(data_out_3t[4,:,k]-np.nanmean(data_out_3t[4,:,20]))/np.nanstd(data_out_3t[4,:,20])

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
    if v==4:
        csri[:,v,3]=annual1[v,:]
        csri[:,v,4]=season1[v,:]
        for m in range(21):
            csri[m,v,0:3]=cal_csr(data_out3[:,20],data_out3[:,m])
        csri[20,v,0:3]=cal_csr(data_out3[:,20],np.mean(data_out3[:,0:21],1))
    else:
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

index1=np.argsort(np.mean(csr_rank[:,[3,4,5,10,11,12,17,18,19,24,25,26,31,32,33]],1))
models_p1=models
models_p1=np.array(models)[index1]
csr_rank_p1=csr_rank[index1,:]
csr_rank_xr=xr.DataArray(csr_rank,coords=[models,np.arange(0,35,1)],dims=['models','5varx7metric'])
csr_rank_xr.to_netcdf('../data/csr_vi_rank_score_21x35_60NS.nc')