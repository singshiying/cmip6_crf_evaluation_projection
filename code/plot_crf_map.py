import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()
plt.rcParams['figure.figsize']=(5.5,4)

data_out=np.load('../fig1.npy')#5x180x360x21(20models,obs)
model_mean=np.mean(data_out[:,:,:,0:20],3)
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)

def draw(fig,axe,num,label,clev,data):
    pdata, plon = add_cyclic_point(data, coord=olon)
    c=axe.contourf(plon,olat,pdata,clev,transform=ccrs.PlateCarree(central_longitude=0),cmap='bwr', extend='both')
    # 地图以180°为中心显示
    axe.set_global()
    # print("数据经度范围:", plon.min(), plon.max())
    # print("地图显示范围:", axe.get_extent(crs=ccrs.PlateCarree()))
    axe.coastlines(resolution='110m', linewidth=0.75)
    if num==1 or num==4 or num==7:
        axe.set_yticks([-60,-30,0,30,60])
        axe.set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=9)
    else:
        axe.set_yticks([])
    if num==7 or num==8 or num==9:
        axe.set_xticks([-90,0,90])
        axe.set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=9)
    else:
        axe.set_xticks([])
    axe.set_title(label,loc='left',fontsize=9)
    return c

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
# 设置所有子图的长宽比
for ax in axes.flat:
    ax.set_aspect('auto')
fig.subplots_adjust(wspace=0.05,hspace=0.27,right=0.9,top=0.9,bottom=0.1)
fig.set_dpi(600)
clev=np.arange(-100,101,10)
c1=draw(fig,axes[0][0],1,'(a) TOA SWCRF,CERES ',clev,data_out[0,:,:,20])
c2=draw(fig,axes[0][1],2,'(b) TOA LWCRF,CERES ',clev,data_out[1,:,:,20])
c3=draw(fig,axes[0][2],3,'(c) TOA NETCRF,CERES',clev,data_out[0,:,:,20]+data_out[1,:,:,20])
c4=draw(fig,axes[1][0],4,'(d) ATM SWCRF,CERES ',clev,data_out[0,:,:,20]-data_out[2,:,:,20])
c5=draw(fig,axes[1][1],5,'(e) ATM LWCRF,CERES ',clev,data_out[1,:,:,20]-data_out[3,:,:,20])
c6=draw(fig,axes[1][2],6,'(f) ATM NETCRF,CERES ',clev,data_out[0,:,:,20]+data_out[1,:,:,20]-data_out[2,:,:,20]-data_out[3,:,:,20])
c7=draw(fig,axes[2][0],7,'(h) SFC SWCRF,CERES ',clev,data_out[2,:,:,20])
c8=draw(fig,axes[2][1],8,'(i) SFC LWCRF,CERES ',clev,data_out[3,:,:,20])
c9=draw(fig,axes[2][2],9,'(j) SFC NETCRF,CERES ',clev,data_out[2,:,:,20]+data_out[3,:,:,20])
position = fig.add_axes([0.92, 0.1, 0.010, 0.8])
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=9)
cb.set_label('W m$^{-2}$', fontsize=9,rotation=270)
cb.set_ticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
plt.savefig('../fig/crf_obs_map.svg',bbox_inches='tight')

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
for ax in axes.flat:
    ax.set_aspect('auto')
fig.subplots_adjust(wspace=0.05,hspace=0.27,right=0.9,top=0.9,bottom=0.1)
fig.set_dpi(600)
clev=np.arange(-20,21,5)
c1=draw(fig,axes[0][0],1,'(a) TOA SWCRF,Bias ',clev,model_mean[0,:,:]-data_out[0,:,:,20])
c2=draw(fig,axes[0][1],2,'(b) TOA LWCRF,Bias ',clev,model_mean[1,:,:]-data_out[1,:,:,20])
c3=draw(fig,axes[0][2],3,'(c) TOA NETCRF,Bias',clev,model_mean[0,:,:]-data_out[0,:,:,20]+model_mean[1,:,:]-data_out[1,:,:,20])
c4=draw(fig,axes[1][0],4,'(d) ATM SWCRF,Bias ',clev,model_mean[0,:,:]-data_out[0,:,:,20]-model_mean[2,:,:]+data_out[2,:,:,20])
c5=draw(fig,axes[1][1],5,'(e) ATM LWCRF,Bias ',clev,model_mean[1,:,:]-data_out[1,:,:,20]-model_mean[3,:,:]+data_out[3,:,:,20])
c6=draw(fig,axes[1][2],6,'(f) ATM NETCRF,Bias ',clev,model_mean[0,:,:]-data_out[0,:,:,20]-model_mean[2,:,:]+data_out[2,:,:,20]+model_mean[1,:,:]-data_out[1,:,:,20]-model_mean[3,:,:]+data_out[3,:,:,20])
c7=draw(fig,axes[2][0],7,'(h) SFC SWCRF,Bias ',clev,model_mean[2,:,:]-data_out[2,:,:,20])
c8=draw(fig,axes[2][1],8,'(i) SFC LWCRF,Bias ',clev,model_mean[3,:,:]-data_out[3,:,:,20])
c9=draw(fig,axes[2][2],9,'(j) SFC NETCRF,Bias ',clev,model_mean[2,:,:]-data_out[2,:,:,20]+model_mean[3,:,:]-data_out[3,:,:,20])
position = fig.add_axes([0.92, 0.1, 0.010, 0.8])
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=9)
cb.set_label('W m$^{-2}$', fontsize=9,rotation=270)
plt.savefig('../fig/crf_bias_map.svg',bbox_inches='tight')

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
# 设置所有子图的长宽比
for ax in axes.flat:
    ax.set_aspect('auto')
fig.subplots_adjust(wspace=0.05,hspace=0.27,right=0.9,top=0.9,bottom=0.1)
fig.set_dpi(600)
clev=np.arange(-100,101,10)
c1=draw(fig,axes[0][0],1,'(a) TOA SWCRF,AMME ',clev,model_mean[0,:,:])
c2=draw(fig,axes[0][1],2,'(b) TOA LWCRF,AMME ',clev,model_mean[1,:,:])
c3=draw(fig,axes[0][2],3,'(c) TOA NETCRF,AMME ',clev,model_mean[0,:,:]+model_mean[1,:,:])
c4=draw(fig,axes[1][0],4,'(d) ATM SWCRF,AMME ',clev,model_mean[0,:,:]-model_mean[2,:,:])
c5=draw(fig,axes[1][1],5,'(e) ATM LWCRF,AMME ',clev,model_mean[1,:,:]-model_mean[3,:,:])
c6=draw(fig,axes[1][2],6,'(f) ATM NETCRF,AMME ',clev,model_mean[0,:,:]+model_mean[1,:,:]-model_mean[2,:,:]-model_mean[3,:,:])
c7=draw(fig,axes[2][0],7,'(h) SFC SWCRF,AMME ',clev,model_mean[2,:,:])
c8=draw(fig,axes[2][1],8,'(i) SFC LWCRF,AMME ',clev,model_mean[3,:,:])
c9=draw(fig,axes[2][2],9,'(j) SFC NETCRF,AMME ',clev,model_mean[2,:,:]+model_mean[3,:,:])
position = fig.add_axes([0.92, 0.1, 0.010, 0.8])# [left, bottom, width, height]
cb=fig.colorbar(c3,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=9)
cb.set_label('W m$^{-2}$', fontsize=9,rotation=270)
cb.set_ticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
plt.savefig('../fig/crf_amme_map.svg',bbox_inches='tight')