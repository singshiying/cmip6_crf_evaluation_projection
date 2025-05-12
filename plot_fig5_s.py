#读取fig3_s的(5,180,360,len(models)+1)
#选出好模式与坏模式的平均并画出
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
data_out=np.load('fig3_s.npy')#(5,180,360,len(models)+1)
print(data_out.shape)
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
# wmodels=np.array([['FGOALS-g3', 'MRI-ESM2-0', 'ACCESS-ESM1-5'],['CAS-ESM2-0', 'KIOST-ESM', 'FGOALS-g3'],['INM-CM4-8', 'KIOST-ESM', 'CAS-ESM2-0'],['FGOALS-g3', 'IPSL-CM6A-LR', 'INM-CM4-8'],['ACCESS-CM2', 'CESM2-WACCM' ,'CAS-ESM2-0']])
# bmodels=np.array([['CMCC-CM2-SR5', 'CESM2-WACCM' ,'ACCESS-CM2'],['CESM2-WACCM', 'GFDL-ESM4', 'ACCESS-ESM1-5'],[ 'MPI-ESM1-2-HR', 'KACE-1-0-G', 'ACCESS-CM2'],[  'GFDL-ESM4', 'MPI-ESM1-2-LR', 'MPI-ESM1-2-HR'],['MPI-ESM1-2-HR', 'MIROC6', 'MPI-ESM1-2-LR']])
wmodels=np.array([['FGOALS-g3', 'INM-CM4-8', 'NESM3'],['FGOALS-g3', 'INM-CM4-8', 'NESM3'],['INM-CM4-8', 'IPSL-CM6A-LR', 'CAS-ESM2-0'],['INM-CM4-8', 'IPSL-CM6A-LR' ,'CAS-ESM2-0'],['ACCESS-CM2', 'CESM2-WACCM' ,'CAS-ESM2-0']])
bmodels=np.array([[ 'CESM2-WACCM', 'CMCC-CM2-SR5', 'ACCESS-CM2'],[ 'CESM2-WACCM', 'CMCC-CM2-SR5', 'ACCESS-CM2'],[ 'MPI-ESM1-2-HR' ,'CESM2-WACCM' ,'GFDL-ESM4'],[ 'MPI-ESM1-2-HR', 'CESM2-WACCM', 'GFDL-ESM4'],['MPI-ESM1-2-HR', 'MIROC6', 'MPI-ESM1-2-LR']])


wm=np.zeros([5,3])
bm=np.zeros([5,3])
wmdata=np.zeros([5,180,360])
bmdata=np.zeros([5,180,360])
for i in range(5):
    for j in range(3):
        wm[i,j]=models.index(wmodels[i,j])
        bm[i,j]=models.index(bmodels[i,j])
    wmdata[i,:,:]=np.mean(data_out[i,:,:,:].take(wm[i,:].astype(int),axis=2),2)
    bmdata[i,:,:]=np.mean(data_out[i,:,:,:].take(bm[i,:].astype(int),axis=2),2)

def draw(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    # pdata[:,256]=data[:,254]
    # pdata[:,255]=data[:,254]
    # pdata[:,0]=data[:,1]
    if num==5 or num==6:
        c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(),cmap='BrBG', extend='both')
    else:
        c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(),cmap='bwr', extend='both')
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

def draw2(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    # pdata[:,256]=data[:,254]
    # pdata[:,255]=data[:,254]
    # pdata[:,0]=data[:,1]
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(),cmap='bwr', extend='both')
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1 or num==3 or num==5 or num==7:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=18)
    else:
        axe.set_yticks([])
    if num==7 or num==8 :
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
c1=draw(fig,axes[0][0],1,'(a) Toa net crf,BMME ',clev,bmdata[0,:,:]+bmdata[1,:,:]-data_out[0,:,:,24]-data_out[1,:,:,24])
c2=draw(fig,axes[0][1],2,'(b) Toa net crf,WMME         W m$^{-2}$',clev,wmdata[0,:,:]+wmdata[1,:,:]-data_out[0,:,:,24]-data_out[1,:,:,24])
c3=draw(fig,axes[1][0],3,'(c) Sfc net crf,BMME ',clev,bmdata[2,:,:]+bmdata[3,:,:]-data_out[2,:,:,24]-data_out[3,:,:,24])
c4=draw(fig,axes[1][1],4,'(d) Sfc net crf,WMME ',clev,wmdata[2,:,:]+wmdata[3,:,:]-data_out[2,:,:,24]-data_out[3,:,:,24])
clev=np.arange(-40,41,5)
c5=draw(fig,axes[2][0],5,'(e) CLT,BMME ',clev,bmdata[4,:,:]-data_out[4,:,:,24])
c6=draw(fig,axes[2][1],6,'(f) CLT,WMME                          %',clev,wmdata[4,:,:]-data_out[4,:,:,24])
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
plt.savefig('fig5_s.png',bbox_inches='tight')

fig,axes=plt.subplots(4,2,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.17,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(14)
fig.set_figwidth(13)
fig.set_dpi(300)
clev=np.arange(-50,51,5)
c1=draw2(fig,axes[0][0],1,'(a) Toa swcrf,BMME ',clev,bmdata[0,:,:]-data_out[0,:,:,24])
c2=draw2(fig,axes[0][1],2,'(b) Toa swcrf,WMME         W m$^{-2}$',clev,wmdata[0,:,:]-data_out[0,:,:,24])
c3=draw2(fig,axes[1][0],3,'(c) Toa lwcrf,BMME ',clev,bmdata[1,:,:]-data_out[1,:,:,24])
c4=draw2(fig,axes[1][1],4,'(d) Toa lwcrf,WMME ',clev,wmdata[1,:,:]-data_out[1,:,:,24])
c5=draw2(fig,axes[2][0],5,'(e) Sfc swcrf,BMME ',clev,bmdata[2,:,:]-data_out[2,:,:,24])
c6=draw2(fig,axes[2][1],6,'(f) Sfc swcrf,WMME ',clev,wmdata[2,:,:]-data_out[2,:,:,24])
c7=draw2(fig,axes[3][0],7,'(g) Sfc lwcrf,BMME ',clev,bmdata[3,:,:]-data_out[3,:,:,24])
c8=draw2(fig,axes[3][1],8,'(h) Sfc lwcrf,WMME ',clev,wmdata[3,:,:]-data_out[3,:,:,24])
position = fig.add_axes([0.92, 0.1, 0.010, 0.7])#位置[左,下,宽,高]
cb=fig.colorbar(c2,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
# cb.set_ticks([-100,0,100],[-100,0,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
# position = fig.add_axes([0.92, 0.1, 0.010, 0.2])#位置[左,下,宽,高]
# cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# position = fig.add_axes([0.92, 0.11, 0.010, 0.2])#位置[左,下,宽,高]
# cb.ax.tick_params(labelsize=18)
# cb=fig.colorbar(c9,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# cb.ax.tick_params(labelsize=18)
plt.savefig('fig5_s2.png',bbox_inches='tight')