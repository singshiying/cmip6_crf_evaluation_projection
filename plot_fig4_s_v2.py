#读取(5,180,360,24)的inter annual index
####################################
##画图，全球平均的AVI SVI
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
season=np.load('fig4_s2_v2.npy')#.reshape(5,180*360,21,order='A')#5var,latxlon,20model+AMMME
annual=np.load('fig4_s3_v2.npy')#.reshape(5,180*360,21,order='A')
#models=['ACCESS-CM2','BCC-CSM2-MR','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3','CAS-ESM2-0','obs']
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
varnum=np.arange(0,5,1)
modelnum=np.arange(0,21,1)
axr = xr.DataArray(annual, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])
sxr = xr.DataArray(season, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])
weights=xr.DataArray(np.cos(np.deg2rad(olat)),coords=[olat],dims='lat')
axr=axr.weighted(weights)
sxr=sxr.weighted(weights)
# print(np.isnan(annual[0,:,24]).sum())
# print(annual[0,:,24])
a=axr.mean(('lat','lon')).values
s=sxr.mean(('lat','lon')).values
print(s[0,:])
# s=np.nanmean(season,1)
print(a.shape)
# print(a)
# print(s)
x=np.arange(0,21)
fig=plt.figure()
fig.set_figheight(10)
fig.set_figwidth(14)
fig.set_dpi(300)

ax=fig.add_subplot(211)
def draw_bar(ax,a,title,num):
    width=0.15
    rects1 = ax.bar(x - 2*width, a[0,:], width, label='Toa sw crf',color='aqua')
    rects2 = ax.bar(x - width, a[1,:], width, label='Toa lw crf',color='salmon')
    rects3 = ax.bar(x , a[2,:], width,label='Sfc sw crf',color='darkblue')
    rects4 = ax.bar(x+ width , a[3,:], width,label='Sfc lw crf',color='darkred')
    rects3 = ax.bar(x+2*width , a[4,:], width,label='CLT',color='g')
    if num==1:
        ax.set_ylabel('Annual Variablility Index',fontsize=14)
    else:
        ax.set_ylabel('Seasonal Variablility Index',fontsize=14)
    # ax.set_title(title,loc='left')
    ax.set_xlim(-1,21)
    # ax.set_ylim(0,15)
    if num==1:
        ax.set_xticks([])
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(models,rotation=-270,ha='center',va='center_baseline',fontsize=14)
    # ax.bar_label(rects2, padding=3,fmt='%0.1f')
    ax.legend(fontsize=12,loc=2)
titles=['a) Top of atmoshpere shortwave radiative forcing','b) Top of atmoshpere longwave radiative forcing','c) Surface shortwave radiative forcing','d) Surface longwave radiative forcing','e) Total cloud amount']
draw_bar(ax,a,titles,1)
ax2=fig.add_subplot(212)
titles=['a) Top of atmoshpere shortwave radiative forcing','b) Top of atmoshpere longwave radiative forcing','c) Surface shortwave radiative forcing','d) Surface longwave radiative forcing','e) Total cloud amount']
draw_bar(ax2,s,titles,2)
fig.subplots_adjust(wspace=0.05,hspace=0.02,right=0.9,top=0.8,bottom=0.3)
plt.savefig('fig4_s_v2.png',bbox_inches='tight')