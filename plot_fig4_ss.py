#读取inter annual index和seasonal index
#################################
# ###########画出时间变率的全球分布
import os
from xml.etree.ElementTree import C14NWriterTarget
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
season=np.load('fig4_s2_v2.npy')#.reshape(5,180*360,21,order='A')#5var,latxlon,20model+AMMME
annual=np.load('fig4_s3_v2.npy')#.reshape(5,180*360,21,order='A')
#models=['ACCESS-CM2','BCC-CSM2-MR','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3','CAS-ESM2-0','obs']
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)

def drawc(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    # pdata[:,256]=data[:,254]
    # pdata[:,255]=data[:,254]
    # pdata[:,0]=data[:,1]
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(central_longitude=0),cmap='Reds', extend='both')
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1 or num==3 or num==5 or num==7 or num==9:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=18)
    else:
        axe.set_yticks([])
    if num==9 or num==10:
        axe.set_xticks([-90,0,90])
        axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=18)
    else:
        axe.set_xticks([])
    axe.set_title(label,loc='left',fontsize=24)
    return c

fig,axes=plt.subplots(5,2,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(22)
fig.set_figwidth(14)
fig.set_dpi(300)
clev=np.arange(0,21,2)
c1=drawc(fig,axes[0][0],1,'(a) Annual VI of Toa sw crf',clev,np.mean(annual[0,:,:,0:20],2))
c2=drawc(fig,axes[0][1],2,'(b) Seasonal VI of Toa sw crf ',clev,season[0,:,:,20])
c3=drawc(fig,axes[1][0],3,'(c) Annual VI of Toa lw crf',clev,np.mean(annual[0,:,:,0:20],2))
c4=drawc(fig,axes[1][1],4,'(d) Seasonal VI of Toa lw crf ',clev,season[1,:,:,20])
c5=drawc(fig,axes[2][0],5,'(e) Annual VI of Sfc sw crf',clev,np.mean(annual[0,:,:,0:20],2))
c6=drawc(fig,axes[2][1],6,'(f) Seasonal VI of Sfc sw crf ',clev,season[2,:,:,20])
c7=drawc(fig,axes[3][0],7,'(g) Annual VI of Sfc lw crf',clev,np.mean(annual[0,:,:,0:20],2))
c8=drawc(fig,axes[3][1],8,'(h) Seasonal VI of Sfc lw crf ',clev,season[3,:,:,20])
c9=drawc(fig,axes[4][0],9,'(i) Annual VI of CLT',clev,np.mean(annual[0,:,:,0:20],2))
c10=drawc(fig,axes[4][1],10,'(j) Seasonal VI of CLT ',clev,season[4,:,:,20])

position = fig.add_axes([0.92, 0.1, 0.015, 0.7])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
cb.set_ticks([0,2,4,6,8,10,12,14,16,18,20])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
plt.savefig('fig4_ss.png',bbox_inches='tight')