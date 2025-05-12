#画所有模式的60s-90s区域平均的toa sw crf的std
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
import matplotlib.path as mpath
from cartopy.util import add_cyclic_point
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import cartopy.mpl.ticker as cticker
import cartopy.io.shapereader as shpreader
import seaborn as sns

season=np.std(np.load('fig9_1.npy'),0)#12x30x360x21
annual=np.std(np.load('fig9_2.npy'),0)#14x30x360x21
print(annual.shape)
#models=['ACCESS-CM2','BCC-CSM2-MR','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3','CAS-ESM2-0','obs']
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','Obs']
olon=np.arange(0.5,360,1)
lat=np.arange(-89.5,-60,1)
st=np.arange(0,12,1)
at=np.arange(0,14,1)
mn=np.arange(0,21,1)
sp=xr.DataArray(np.load('fig9_1.npy'), coords=[st,lat,olon,mn], dims=['snum','lat','lon','modelnum'])
ap=xr.DataArray(np.load('fig9_2.npy'), coords=[at,lat,olon,mn], dims=['anum','lat','lon','modelnum'])
wlat=xr.DataArray(lat,coords=[lat],dims=['lat'])
weights=np.cos(np.deg2rad(wlat))
sp_mean=sp.weighted(weights).mean(('lon','lat'))
ap_mean=ap.weighted(weights).mean(('lon','lat'))
print(lat.shape)
s_x=np.arange(1,13,1)
a_x=np.arange(2001,2015,1)
s_y=np.arange(-110,10,20)
a_y=np.arange(-90,41,10)
colors=plt.cm.nipy_spectral(np.linspace(1,0,21))
fig=plt.figure(figsize=(14,8),dpi=300)
fig.subplots_adjust(wspace=0.15,hspace=0.25,right=0.9,top=0.8,bottom=0.1)
ax=fig.add_subplot(211)
for m in range(21):
    ax.plot(s_x,sp_mean[:,m],label=models[m],color=colors[m])
    ax.set_xticks(s_x)
    ax.set_yticks(s_y)
    ax.set_xlim(1,12)
    ax.set_ylim(-105,10)
    ax.set_xticklabels(s_x,fontsize=18)
    ax.set_yticklabels(s_y,fontsize=18)
    ax.set_title('a) Seasonal Toa sw crf(W m$^2$)',loc='left',fontsize=18)
# ax.legend()
ax2=fig.add_subplot(212)
for m in range(21):
    ax2.plot(a_x,ap_mean[:,m],label=models[m],color=colors[m])
    ax2.set_xticks(a_x)
    ax2.set_yticks(a_y)
    ax2.set_xlim(2001,2014)
    ax2.set_ylim(-45,-8)
    ax2.set_xticklabels(a_x,fontsize=18)
    ax2.set_yticklabels(a_y,fontsize=18)
    ax2.set_title('b) Annual Toa sw crf(W m$^2$)',loc='left',fontsize=18)
ax.legend(loc=7,bbox_to_anchor=(1.23,-0.1),fontsize=13)
plt.savefig('fig9.png',bbox_inches='tight')


def drawc(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    # pdata[:,256]=data[:,254]
    # pdata[:,255]=data[:,254]
    # pdata[:,0]=data[:,1]
    #######以下为网格线的参数######
    leftlon, rightlon, lowerlat, upperlat = (-180,180,-60,-90)
    img_extent = [leftlon, rightlon, lowerlat, upperlat]
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    axe.set_boundary(circle, transform=axe.transAxes)
    axe.set_extent(img_extent, ccrs.PlateCarree())
    c=axe.contourf(plon,lat,pdata,clev,transform=ccrs.PlateCarree(),cmap='Reds', extend='both')
    axe.coastlines(resolution='110m', linewidth=0.75)
    axe.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')
    c.ylocator = mticker.FixedLocator([-70, -80])
    axe.text(60,-55,r'60$^\circ$E',fontsize=14, horizontalalignment='center',transform=ccrs.PlateCarree(),verticalalignment='center')
    axe.text(-60,-55,r'-60$^\circ$W',fontsize=14, horizontalalignment='center',transform=ccrs.PlateCarree(),verticalalignment='center')
    axe.text(120,-55,r'120$^\circ$E',fontsize=14, horizontalalignment='center',transform=ccrs.PlateCarree(),verticalalignment='center')
    axe.text(-120,-55,r'-120$^\circ$W',fontsize=14, horizontalalignment='center',transform=ccrs.PlateCarree(),verticalalignment='center')
    # if num in [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41]:
    #     axe.set_yticks([-90,-60])
    #     axe.set_yticklabels(['90$^\circ$S','60$^\circ$S'],fontsize=18)
    # else:
    #     axe.set_yticks([])
    # if num in [41,42]:
    #     axe.set_xticks([-90,0,90])
    #     axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=18)
    # else:
    #     axe.set_xticks([])
    axe.set_title(label,loc='center',fontsize=18)
    # fig.colorbar(c,ax=axe)
    return c

fig,axes=plt.subplots(4,2,subplot_kw={'projection':ccrs.SouthPolarStereo()})
fig.subplots_adjust(wspace=0.15,hspace=0.1,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(22)
fig.set_figwidth(14)
fig.set_dpi(300)
clev1=np.arange(0,2.41,0.2)
clev2=np.arange(0,10.1,0.5)

s=0
t=0
for i in [0,8,9,20]:
    c1=drawc(fig,axes[t][0],s+1,' annual std,'+models[i],clev1,annual[:,:,i])
    c2=drawc(fig,axes[t][1],s+2,' seasonal std,'+models[i],clev2,season[:,:,i])
    s=s+2
    t=t+1
position = fig.add_axes([0.5, 0.12, 0.015, 0.68])#位置[左,下,宽,高]
cb=fig.colorbar(c1,shrink=0.8,cax=position,fraction=0.03, format='% 1.1f')
cb.ax.tick_params(labelsize=18)
cb.set_ticks(clev1.tolist(),clev1.tolist())
position = fig.add_axes([0.92, 0.12, 0.015, 0.68])#位置[左,下,宽,高]
cb=fig.colorbar(c2,shrink=0.8,cax=position,fraction=0.03, format='% 1.1f')
cb.ax.tick_params(labelsize=18)
cb.set_ticks(clev2.tolist(),clev2.tolist())
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
plt.savefig('fig9ss.png',bbox_inches='tight')