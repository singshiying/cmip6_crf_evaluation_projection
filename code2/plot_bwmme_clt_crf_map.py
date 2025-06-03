import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
import pandas as pd
from matplotlib.font_manager import FontProperties
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()

data_out=np.load('./fig1.npy')#5x180x360x21(20models,obs) 读取历史实验平均
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','OBS']
data_out_xr=xr.DataArray(data_out,coords=[np.arange(0,5,1),olat,olon,models],dims=['vars','lat','lon','models'])

bmme=['EC-Earth3-CC','CMCC-CM2-SR5','CESM2-WACCM','GFDL-ESM4']
wmme=['FGOALS-g3','CAS-ESM2-0','NESM3','INM-CM4-8']

def draw(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(),cmap='bwr', extend='both')
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1 or num==3 or num==5:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=9)
    else:
        axe.set_yticks([])
    if num==5 or num==6 or num==9:
        axe.set_xticks([-90,0,90])
        axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=9)
    else:
        axe.set_xticks([])
    axe.set_title(label,loc='left',fontsize=9)
    axe.set_aspect('auto')
    return c

t1=data_out_xr.loc[0,:,:,list(set(bmme))].mean('models')+data_out_xr.loc[1,:,:,list(set(bmme))].mean('models')-(data_out_xr.loc[0,:,:,'OBS']+data_out_xr.loc[1,:,:,'OBS'])
t2=data_out_xr.loc[0,:,:,list(set(wmme))].mean('models')+data_out_xr.loc[1,:,:,list(set(wmme))].mean('models')-(data_out_xr.loc[0,:,:,'OBS']+data_out_xr.loc[1,:,:,'OBS'])
t3=data_out_xr.loc[2,:,:,list(set(bmme))].mean('models')+data_out_xr.loc[3,:,:,list(set(bmme))].mean('models')-(data_out_xr.loc[3,:,:,'OBS']+data_out_xr.loc[2,:,:,'OBS'])
t4=data_out_xr.loc[2,:,:,list(set(wmme))].mean('models')+data_out_xr.loc[3,:,:,list(set(wmme))].mean('models')-(data_out_xr.loc[3,:,:,'OBS']+data_out_xr.loc[2,:,:,'OBS'])
t5=t1-t3
t6=t2-t4

fig,axes=plt.subplots(3,2,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})

fig.subplots_adjust(wspace=0.05,hspace=0.17,right=0.9,top=0.9,bottom=0.1)
fig.set_figheight(6)
fig.set_figwidth(5.5)
fig.set_dpi(300)
clev=np.arange(-50,51,5)
c1=draw(fig,axes[0][0],1,'(a) TOA NETCRF,BMME ',clev,t1)
c2=draw(fig,axes[0][1],2,'(b) TOA NETCRF,WMME ',clev,t2)
c3=draw(fig,axes[1][0],3,'(c) ATM NETCRF,BMME ',clev,t3)
c4=draw(fig,axes[1][1],4,'(d) ATM NETCRF,WMME ',clev,t4)
c5=draw(fig,axes[2][0],5,'(e) SFC NETCRF,BMME ',clev,t5)
c6=draw(fig,axes[2][1],6,'(f) SFC NETCRF,WMME ',clev,t6)
position = fig.add_axes([0.92, 0.1, 0.010, 0.8])#位置[左,下,宽,高]
cb=fig.colorbar(c2,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=9)
cb.set_label('W m$^{-2}$', fontsize=9,rotation=270)
plt.savefig('../fig2/bwmme_crf_map.svg',bbox_inches='tight')