#画出toaswlwnet,sfcswlwnet,clt好模式与坏模式相对于obs的偏差
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
data_out=np.load('fig5.npy')#5x128x256x3good worse obs
time_len=168
olat=np.linspace(-90,90,128)
olon=np.linspace(0,358.6,256)
lon_len=len(olon)
lat_len=len(olat)
toa_net=data_out[0,:,:,:]+data_out[1,:,:,:]
sfc_net=data_out[2,:,:,:]+data_out[3,:,:,:]
def draw(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    # pdata[:,256]=data[:,254]
    # pdata[:,255]=data[:,254]
    # pdata[:,0]=data[:,1]
    if num==5 or num==6:
        c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(central_longitude=0),cmap='BrBG', extend='both')
    else:
        c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(central_longitude=0),cmap='bwr', extend='both')
    axe.set_global()
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1 or num==3 or num==5:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=18)
    else:
        axe.set_yticks([])
    if num==5 or num==6 or num==9:
        axe.set_xticks([-90,0,90])
        axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=18)
    else:
        axe.set_xticks([])
    axe.set_title(label,loc='left',fontsize=24)
    return c

fig,axes=plt.subplots(3,2,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.17,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(11)
fig.set_figwidth(13)
fig.set_dpi(300)
clev=np.arange(-50,51,5)
c1=draw(fig,axes[0][0],1,'(a) Toa net crf,BMME ',clev,toa_net[:,:,0]-toa_net[:,:,2])
c2=draw(fig,axes[0][1],2,'(b) Toa net crf,WMME         W m$^{-2}$',clev,toa_net[:,:,1]-toa_net[:,:,2])
c3=draw(fig,axes[1][0],3,'(c) Sfc net crf,BMME ',clev,sfc_net[:,:,0]-sfc_net[:,:,2])
c4=draw(fig,axes[1][1],4,'(d) Sfc net crf,WMME ',clev,sfc_net[:,:,1]-sfc_net[:,:,2])
clev=np.arange(-40,41,5)
c5=draw(fig,axes[2][0],5,'(e) TCF,BMME ',clev,data_out[4,:,:,0]-data_out[4,:,:,2])
c6=draw(fig,axes[2][1],6,'(f) TCF,WMME                          %',clev,data_out[4,:,:,1]-data_out[4,:,:,2])
position = fig.add_axes([0.92, 0.35, 0.010, 0.45])#位置[左,下,宽,高]
cb=fig.colorbar(c2,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
# cb.set_ticks([-100,0,100],[-100,0,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
position = fig.add_axes([0.92, 0.1, 0.010, 0.2])#位置[左,下,宽,高]
cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# position = fig.add_axes([0.92, 0.11, 0.010, 0.2])#位置[左,下,宽,高]
# cb.ax.tick_params(labelsize=18)
# cb=fig.colorbar(c9,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# cb.ax.tick_params(labelsize=18)
plt.savefig('fig5.png',bbox_inches='tight')