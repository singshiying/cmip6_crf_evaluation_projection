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

data_out2=np.load('./fig4_s2_v2.npy')#5x180x360x21  sVI指数
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
data_out_xr2=xr.DataArray(data_out2,coords=[np.arange(0,5,1),olat,olon,models],dims=['vars','lat','lon','models'])

data_out3=np.load('./fig4_s3_v2.npy')#5x180x360x21  aVI指数
data_out_xr3=xr.DataArray(data_out3,coords=[np.arange(0,5,1),olat,olon,models],dims=['vars','lat','lon','models'])
bmme=['EC-Earth3-CC','CMCC-CM2-SR5','CESM2-WACCM','GFDL-ESM4']
wmme=['FGOALS-g3','CAS-ESM2-0','NESM3','INM-CM4-8']


tt1=data_out_xr2.loc[0,:,:,list(set(bmme))].mean('models')+data_out_xr2.loc[1,:,:,list(set(bmme))].mean('models')
tt2=data_out_xr2.loc[0,:,:,list(set(wmme))].mean('models')+data_out_xr2.loc[1,:,:,list(set(wmme))].mean('models')
tt3=data_out_xr2.loc[2,:,:,list(set(bmme))].mean('models')+data_out_xr2.loc[3,:,:,list(set(bmme))].mean('models')
tt4=data_out_xr2.loc[2,:,:,list(set(wmme))].mean('models')+data_out_xr2.loc[3,:,:,list(set(wmme))].mean('models')
# tt5=data_out_xr2.loc[4,:,:,bmme].mean('models')
# tt6=data_out_xr2.loc[4,:,:,wmme].mean('models')

ttt1=data_out_xr3.loc[0,:,:,list(set(bmme))].mean('models')+data_out_xr3.loc[1,:,:,list(set(bmme))].mean('models')
ttt2=data_out_xr3.loc[0,:,:,list(set(wmme))].mean('models')+data_out_xr3.loc[1,:,:,list(set(wmme))].mean('models')
ttt3=data_out_xr3.loc[2,:,:,list(set(bmme))].mean('models')+data_out_xr3.loc[3,:,:,list(set(bmme))].mean('models')
ttt4=data_out_xr3.loc[2,:,:,list(set(wmme))].mean('models')+data_out_xr3.loc[3,:,:,list(set(wmme))].mean('models')
# ttt5=data_out_xr3.loc[4,:,:,bmme].mean('models')
# ttt6=data_out_xr3.loc[4,:,:,wmme].mean('models')

def draw_s(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    # pdata[:,256]=data[:,254]
    # pdata[:,255]=data[:,254]
    # pdata[:,0]=data[:,1]
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(),cmap='Reds', extend='both')
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(),cmap='Reds', extend='both')
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1 or num==3 or num==5 or num==7:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=9)
    else:
        axe.set_yticks([])
    if num==7 or num==8:
        axe.set_xticks([-90,0,90])
        axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=9)
    else:
        axe.set_xticks([])
    axe.set_title(label,loc='left',fontsize=9)
    return c

fig,axes=plt.subplots(4,2,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.17,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(7)
fig.set_figwidth(5.5)
fig.set_dpi(300)
clev=np.arange(0,20,2)
c1=draw_s(fig,axes[0][0],1,'(a) TOA NETCRF SVI,BMME ',clev,tt1)
c2=draw_s(fig,axes[0][1],2,'(b) TOA NETCRF SVI,WMME',clev,tt2)
c3=draw_s(fig,axes[1][0],3,'(c) ATM NETCRF SVI,BMME ',clev,tt3)
c4=draw_s(fig,axes[1][1],4,'(d) ATM NETCRF SVI,WMME ',clev,tt4)
c5=draw_s(fig,axes[2][0],5,'(e) TOA NETCRF AVI,BMME ',clev,ttt1)
c6=draw_s(fig,axes[2][1],6,'(f) TOA NETCRF AVI,WMME',clev,ttt2)
c7=draw_s(fig,axes[3][0],7,'(g) ATM NETCRF AVI,BMME ',clev,ttt3)
c8=draw_s(fig,axes[3][1],8,'(h) ATM NETCRF AVI,WMME',clev,ttt4)
position = fig.add_axes([0.92, 0.1, 0.010, 0.7])#位置[左,下,宽,高]
cb=fig.colorbar(c2,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=9)
# position = fig.add_axes([0.92, 0.1, 0.010, 0.2])#位置[左,下,宽,高]
# cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
plt.savefig('../fig2/bwmme_svi_avi.svg',bbox_inches='tight')

