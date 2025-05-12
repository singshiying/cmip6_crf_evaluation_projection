#%%
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
#%%
data_out3=np.load('/data04/shiy/code_cloud/code_paper_7.13/fig7_3.npy')#5areax5varx1020timex24models
data_out1=np.load('/data04/shiy/code_cloud/code_paper_7.13/fig7_1.npy')#5areax5varx1980timex24models
data_out2=np.load('/data04/shiy/code_cloud/code_paper_7.13/fig7_2.npy')
data_out=np.concatenate((data_out1,data_out2),axis = 2)
data_outt=np.concatenate((data_out1,data_out3),axis = 2)
areanum=np.arange(5)
varnum=np.arange(5)
time=pd.date_range('18500101','20991231',freq='M')
gwnum=np.arange(6)
modelnum=np.arange(23)
data2xr=xr.DataArray(data_out[:,:,:,:], coords=[areanum,varnum, time,modelnum], dims=['areanum','varnum', 'time','modelnum'])
data22xr=xr.DataArray(data_outt[:,:,:,:], coords=[areanum,varnum, time,modelnum], dims=['areanum','varnum', 'time','modelnum'])
datay2=data2xr.loc[:,:,'1850-01-01':'2099-12-31',:].groupby('time.year').mean()#.values#变成年平均
datay22=data22xr.loc[:,:,'1850-01-01':'2099-12-31',:].groupby('time.year').mean()#.values#变成年平均

#%%
# os.system("pwd")
fig,ax=plt.subplots(3,1)
datay2[0,0,:,0].plot(ax=ax[0])
datay2[0,1,:,0].plot(ax=ax[1])
(datay2[0,0,:,0]+datay2[0,1,:,0]).plot(ax=ax[2])

#%%
ceres_path='/data04/shiy/observation/CERES_EBAF_Edition4.1_200003-202011.nc'
fc=xr.open_dataset(ceres_path)
lw_crf=fc['toa_cre_lw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
weights=np.cos(np.deg2rad(lw_crf.coords['lat']))
lw_crf.weighted(weights).mean(('lon','lat')).groupby('time.year').mean().plot()
