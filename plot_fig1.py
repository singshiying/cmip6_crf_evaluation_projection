import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
data_out=np.load('fig1.npy')#5x180x360x21(20models,obs)
model_mean=np.mean(data_out[:,:,:,0:20],3)
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)

def draw(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    # print(plon)
    # pdata[:,256]=data[:,254]
    # pdata[:,255]=data[:,254]
    # pdata[:,0]=data[:,1]
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(central_longitude=0),cmap='bwr', extend='both')
    # 地图以180°为中心显示
    axe.set_global()
    # print("数据经度范围:", plon.min(), plon.max())
    # print("地图显示范围:", axe.get_extent(crs=ccrs.PlateCarree()))
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1 or num==4 or num==7:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=18)
    else:
        axe.set_yticks([])
    if num==7 or num==8 or num==9:
        axe.set_xticks([-90,0,90])
        axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=18)
    else:
        axe.set_xticks([])
    axe.set_title(label,loc='left',fontsize=24)
    return c
    

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(10)
fig.set_figwidth(16)
fig.set_dpi(300)
clev=np.arange(-100,101,10)
c1=draw(fig,axes[0][0],1,'(a) Toa sw crf,AMME ',clev,model_mean[0,:,:])
c2=draw(fig,axes[0][1],2,'(b) Toa lw crf,AMME ',clev,model_mean[1,:,:])
c3=draw(fig,axes[0][2],3,'(c) Toa net crf,AMME    W m$^{-2}$',clev,model_mean[0,:,:]+model_mean[1,:,:])
c4=draw(fig,axes[1][0],4,'(d) Toa sw crf,CERES ',clev,data_out[0,:,:,20])
c5=draw(fig,axes[1][1],5,'(e) Toa lw crf,CERES ',clev,data_out[1,:,:,20])
c6=draw(fig,axes[1][2],6,'(f) Toa net crf,CERES ',clev,data_out[0,:,:,20]+data_out[1,:,:,20])
clev=np.arange(-20,21,5)
c7=draw(fig,axes[2][0],7,'(h) Toa sw crf,Bias ',clev,model_mean[0,:,:]-data_out[0,:,:,20])
c8=draw(fig,axes[2][1],8,'(i) Toa lw crf,Bias ',clev,model_mean[1,:,:]-data_out[1,:,:,20])
c9=draw(fig,axes[2][2],9,'(j) Toa net crf,Bias ',clev,model_mean[0,:,:]+model_mean[1,:,:]-data_out[0,:,:,20]-data_out[1,:,:,20])
position = fig.add_axes([0.92, 0.59, 0.010, 0.2])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
# cb.set_ticks([-100,0,100],[-100,0,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
position = fig.add_axes([0.92, 0.35, 0.010, 0.2])#位置[左,下,宽,高]
cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
position = fig.add_axes([0.92, 0.11, 0.010, 0.2])#位置[左,下,宽,高]
cb.ax.tick_params(labelsize=18)
cb=fig.colorbar(c9,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
plt.savefig('fig1.1.png',bbox_inches='tight')

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(10)
fig.set_figwidth(16)
fig.set_dpi(300)
clev=np.arange(-100,101,10)
c1=draw(fig,axes[0][0],1,'(a) Sfc sw crf,AMME ',clev,model_mean[2,:,:])
c2=draw(fig,axes[0][1],2,'(b) Sfc lw crf,AMME ',clev,model_mean[3,:,:])
c3=draw(fig,axes[0][2],3,'(c) Sfc net crf,AMME    W m$^{-2}$',clev,model_mean[2,:,:]+model_mean[3,:,:])
c4=draw(fig,axes[1][0],4,'(d) Sfc sw crf,CERES ',clev,data_out[2,:,:,20])
c5=draw(fig,axes[1][1],5,'(e) Sfc lw crf,CERES ',clev,data_out[3,:,:,20])
c6=draw(fig,axes[1][2],6,'(f) Sfc net crf,CERES ',clev,data_out[2,:,:,20]+data_out[3,:,:,20])
clev=np.arange(-20,21,5)
c7=draw(fig,axes[2][0],7,'(h) Sfc sw crf,Bias ',clev,model_mean[2,:,:]-data_out[2,:,:,20])
c8=draw(fig,axes[2][1],8,'(i) Sfc lw crf,Bias ',clev,model_mean[3,:,:]-data_out[3,:,:,20])
c9=draw(fig,axes[2][2],9,'(j) Sfc net crf,Bias ',clev,model_mean[2,:,:]+model_mean[3,:,:]-data_out[2,:,:,20]-data_out[3,:,:,20])
position = fig.add_axes([0.92, 0.59, 0.010, 0.2])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
# cb.set_ticks([-100,0,100],[-100,0,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
position = fig.add_axes([0.92, 0.35, 0.010, 0.2])#位置[左,下,宽,高]
cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
position = fig.add_axes([0.92, 0.11, 0.010, 0.2])#位置[左,下,宽,高]
cb.ax.tick_params(labelsize=18)
cb=fig.colorbar(c9,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
plt.savefig('fig1.2.png',bbox_inches='tight')


fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(10)
fig.set_figwidth(16)
fig.set_dpi(300)
clev=np.arange(-100,101,10)
c1=draw(fig,axes[0][0],1,'(a) Atm sw crf,AMME ',clev,model_mean[0,:,:]-model_mean[2,:,:])#toa-sfc
c2=draw(fig,axes[0][1],2,'(b) Atm lw crf,AMME ',clev,model_mean[1,:,:]-model_mean[3,:,:])
c3=draw(fig,axes[0][2],3,'(c) Atm net crf,AMME    W m$^{-2}$',clev,model_mean[0,:,:]-model_mean[2,:,:]+model_mean[1,:,:]-model_mean[3,:,:])
c4=draw(fig,axes[1][0],4,'(d) Atm sw crf,CERES ',clev,data_out[0,:,:,20]-data_out[2,:,:,20])
c5=draw(fig,axes[1][1],5,'(e) Atm lw crf,CERES ',clev,data_out[1,:,:,20]-data_out[3,:,:,20])
c6=draw(fig,axes[1][2],6,'(f) Atm net crf,CERES ',clev,data_out[0,:,:,20]-data_out[2,:,:,20]+data_out[1,:,:,20]-data_out[3,:,:,20])
clev=np.arange(-20,21,5)
c7=draw(fig,axes[2][0],7,'(h) Atm sw crf,Bias ',clev,model_mean[0,:,:]-model_mean[2,:,:]-data_out[0,:,:,20]+data_out[2,:,:,20])
c8=draw(fig,axes[2][1],8,'(i) Atm lw crf,Bias ',clev,model_mean[1,:,:]-model_mean[3,:,:]-data_out[1,:,:,20]+data_out[3,:,:,20])
c9=draw(fig,axes[2][2],9,'(j) Atm net crf,Bias ',clev,model_mean[0,:,:]-model_mean[2,:,:]+model_mean[1,:,:]-model_mean[3,:,:]-data_out[0,:,:,20]+data_out[2,:,:,20]-data_out[1,:,:,20]+data_out[3,:,:,20])
position = fig.add_axes([0.92, 0.59, 0.010, 0.2])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
# cb.set_ticks([-100,0,100],[-100,0,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
position = fig.add_axes([0.92, 0.35, 0.010, 0.2])#位置[左,下,宽,高]
cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
position = fig.add_axes([0.92, 0.11, 0.010, 0.2])#位置[左,下,宽,高]
cb.ax.tick_params(labelsize=18)
cb=fig.colorbar(c9,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
plt.savefig('fig1.3.png',bbox_inches='tight')


def drawc(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    pdata[:,256]=data[:,254]
    pdata[:,255]=data[:,254]
    pdata[:,0]=data[:,1]
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(central_longitude=0),cmap='BrBG', extend='both')
    # 地图以180°为中心显示
    axe.set_global()
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=18)
    else:
        axe.set_yticks([])
    axe.set_xticks([-90,0,90])
    axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=18)
    axe.set_title(label,loc='left',fontsize=24)
    return c

fig,axes=plt.subplots(1,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(4)
fig.set_figwidth(16)
fig.set_dpi(300)
clev=np.arange(-100,101,10)
c1=drawc(fig,axes[0],1,'(a) CLT,AMME ',clev,model_mean[4,:,:])
c2=drawc(fig,axes[1],2,'(b) CLT,ISCCP-H ',clev,data_out[4,:,:,20])
clev=np.arange(-40,41,5)
c3=drawc(fig,axes[2],3,'(c) CLT,Bias                      %',clev,model_mean[4,:,:]-data_out[4,:,:,20])
position = fig.add_axes([0.92, 0.2, 0.010, 0.5])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
cb.set_ticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
# cb.set_ticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],[-100,-80,-60,-40,-20,0,20,40,60,80,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
plt.savefig('fig1.4.png',bbox_inches='tight')


fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(10)
fig.set_figwidth(16)
fig.set_dpi(300)
clev=np.arange(-100,101,10)
c1=draw(fig,axes[0][0],1,'(a) Toa sw crf,CERES ',clev,data_out[0,:,:,20])
c2=draw(fig,axes[0][1],2,'(b) Toa lw crf,CERES ',clev,data_out[1,:,:,20])
c3=draw(fig,axes[0][2],3,'(c) Toa net crf,CERES     W m$^{-2}$',clev,data_out[0,:,:,20]+data_out[1,:,:,20])
c4=draw(fig,axes[1][0],4,'(d) Atm sw crf,CERES ',clev,data_out[0,:,:,20]-data_out[2,:,:,20])
c5=draw(fig,axes[1][1],5,'(e) Atm lw crf,CERES ',clev,data_out[1,:,:,20]-data_out[3,:,:,20])
c6=draw(fig,axes[1][2],6,'(f) Atm net crf,CERES ',clev,data_out[0,:,:,20]+data_out[1,:,:,20]-data_out[2,:,:,20]-data_out[3,:,:,20])
# clev=np.arange(-20,21,5)
c7=draw(fig,axes[2][0],7,'(h) Sfc sw crf,CERES ',clev,data_out[2,:,:,20])
c8=draw(fig,axes[2][1],8,'(i) Sfc lw crf,CERES ',clev,data_out[3,:,:,20])
c9=draw(fig,axes[2][2],9,'(j) Sfc net crf,CERES ',clev,data_out[2,:,:,20]+data_out[3,:,:,20])
position = fig.add_axes([0.92, 0.1, 0.010, 0.68])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
cb.set_ticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
# cb.set_ticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],[-100,-80,-60,-40,-20,0,20,40,60,80,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
# position = fig.add_axes([0.92, 0.35, 0.010, 0.2])#位置[左,下,宽,高]
# cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# position = fig.add_axes([0.92, 0.11, 0.010, 0.2])#位置[左,下,宽,高]
# cb.ax.tick_params(labelsize=18)
# cb=fig.colorbar(c9,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# cb.ax.tick_params(labelsize=18)
plt.savefig('fig1.obs.png',bbox_inches='tight')

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(10)
fig.set_figwidth(16)
fig.set_dpi(300)
clev=np.arange(-20,21,5)
c1=draw(fig,axes[0][0],1,'(a) Toa sw crf,Bias ',clev,model_mean[0,:,:]-data_out[0,:,:,20])
c2=draw(fig,axes[0][1],2,'(b) Toa lw crf,Bias ',clev,model_mean[1,:,:]-data_out[1,:,:,20])
c3=draw(fig,axes[0][2],3,'(c) Toa net crf,Bias        W m$^{-2}$',clev,model_mean[0,:,:]-data_out[0,:,:,20]+model_mean[1,:,:]-data_out[1,:,:,20])
c4=draw(fig,axes[1][0],4,'(d) Atm sw crf,Bias ',clev,model_mean[0,:,:]-data_out[0,:,:,20]-model_mean[2,:,:]+data_out[2,:,:,20])
c5=draw(fig,axes[1][1],5,'(e) Atm lw crf,Bias ',clev,model_mean[1,:,:]-data_out[1,:,:,20]-model_mean[3,:,:]+data_out[3,:,:,20])
c6=draw(fig,axes[1][2],6,'(f) Atm net crf,Bias ',clev,model_mean[0,:,:]-data_out[0,:,:,20]-model_mean[2,:,:]+data_out[2,:,:,20]+model_mean[1,:,:]-data_out[1,:,:,20]-model_mean[3,:,:]+data_out[3,:,:,20])
# clev=np.arange(-20,21,5)
c7=draw(fig,axes[2][0],7,'(h) Sfc sw crf,Bias ',clev,model_mean[2,:,:]-data_out[2,:,:,20])
c8=draw(fig,axes[2][1],8,'(i) Sfc lw crf,Bias ',clev,model_mean[3,:,:]-data_out[3,:,:,20])
c9=draw(fig,axes[2][2],9,'(j) Sfc net crf,Bias ',clev,model_mean[2,:,:]-data_out[2,:,:,20]+model_mean[3,:,:]-data_out[3,:,:,20])
position = fig.add_axes([0.92, 0.1, 0.010, 0.68])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
plt.savefig('fig1.bias.png',bbox_inches='tight')

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
fig.subplots_adjust(wspace=0.05,hspace=0.05,right=0.9,top=0.8,bottom=0.1)
fig.set_figheight(10)
fig.set_figwidth(16)
fig.set_dpi(300)
clev=np.arange(-100,101,10)
c1=draw(fig,axes[0][0],1,'(a) Toa sw crf,AMME ',clev,model_mean[0,:,:])
c2=draw(fig,axes[0][1],2,'(b) Toa lw crf,AMME ',clev,model_mean[1,:,:])
c3=draw(fig,axes[0][2],3,'(c) Toa net crf,AMME      W m$^{-2}$',clev,model_mean[0,:,:]+model_mean[1,:,:])
c4=draw(fig,axes[1][0],4,'(d) Atm sw crf,AMME ',clev,model_mean[0,:,:]-model_mean[2,:,:])
c5=draw(fig,axes[1][1],5,'(e) Atm lw crf,AMME ',clev,model_mean[1,:,:]-model_mean[3,:,:])
c6=draw(fig,axes[1][2],6,'(f) Atm net crf,AMME ',clev,model_mean[0,:,:]+model_mean[1,:,:]-model_mean[2,:,:]-model_mean[3,:,:])
# clev=np.arange(-20,21,5)
c7=draw(fig,axes[2][0],7,'(h) Sfc sw crf,AMME ',clev,model_mean[2,:,:])
c8=draw(fig,axes[2][1],8,'(i) Sfc lw crf,AMME ',clev,model_mean[3,:,:])
c9=draw(fig,axes[2][2],9,'(j) Sfc net crf,AMME ',clev,model_mean[2,:,:]+model_mean[3,:,:])
position = fig.add_axes([0.92, 0.1, 0.010, 0.68])#位置[左,下,宽,高]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=18)
cb.set_ticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
# cb.set_ticks([-100,-80,-60,-40,-20,0,20,40,60,80,100],[-100,-80,-60,-40,-20,0,20,40,60,80,100])
# cb.set_label('W m$^{-2}$',rotation='horizontal',fontsize=18,position=(0.5,1.13))
# position = fig.add_axes([0.92, 0.35, 0.010, 0.2])#位置[左,下,宽,高]
# cb=fig.colorbar(c6,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# position = fig.add_axes([0.92, 0.11, 0.010, 0.2])#位置[左,下,宽,高]
# cb.ax.tick_params(labelsize=18)
# cb=fig.colorbar(c9,cax=position,shrink=0.8,fraction=0.03, format='% 1.0f')
# cb.ax.tick_params(labelsize=18)
plt.savefig('fig1.amme.png',bbox_inches='tight')