import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import GridSpec

font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()
plt.rcParams['figure.figsize']=(5.5,2)

data_out=np.load('../fig1.npy')#5x180x360x21(20models,obs)
model_mean=np.mean(data_out[:,:,:,0:20],3)
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)

# 创建图形和网格
fig = plt.figure(figsize=(5.5, 2), dpi=400)
gs = GridSpec(2, 3, height_ratios=[0.5, 0.05], width_ratios=[1, 1, 1])

# 创建三个子图
axes = []
axes.append(fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(central_longitude=180)))
axes.append(fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree(central_longitude=180)))
axes.append(fig.add_subplot(gs[0, 2], projection=ccrs.PlateCarree(central_longitude=180)))

# 设置所有子图的长宽比
for ax in axes:
    ax.set_aspect('auto')

fig.subplots_adjust(wspace=0.05, hspace=0.25, right=0.9, top=0.9, bottom=0.1)

clev=np.arange(0,101,10)
pdata1, plon1 = add_cyclic_point(model_mean[4,:,:], coord=olon)
c1 = axes[0].contourf(plon1, olat, pdata1, clev, transform=ccrs.PlateCarree(central_longitude=0), cmap='Greens', extend='both')
axes[0].set_extent([-180, 180, -60, 60])
axes[0].set_xlim(-180,180)
axes[0].coastlines(resolution='110m', linewidth=0.75)
axes[0].set_yticks([-60,-30,0,30,60])
axes[0].set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=9)
axes[0].set_xticks([-90,0,90])
axes[0].set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=9)
axes[0].set_title('(a) CLT,AMME ', loc='left', fontsize=9)

# 第二个子图
pdata2, plon2 = add_cyclic_point(data_out[4,:,:,20], coord=olon)
c2 = axes[1].contourf(plon2, olat, pdata2, clev, transform=ccrs.PlateCarree(central_longitude=0), cmap='Greens', extend='both')
axes[1].set_extent([-180, 180, -60, 60])
axes[1].set_xlim(-180,180)
axes[1].coastlines(resolution='110m', linewidth=0.75)
# axes[1].set_yticks([-60,-30,0,30,60])
# axes[1].set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=9)
axes[1].set_xticks([-90,0,90])
axes[1].set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=9)
axes[1].set_title('(b) CLT,ISCCP-H ', loc='left', fontsize=9)

# 第二个子图的colorbar
cax2 = fig.add_axes([0.15, 0.1, 0.46, 0.02])  # [left, bottom, width, height]
cb2 = plt.colorbar(c2, cax=cax2, orientation='horizontal')
cb2.ax.tick_params(labelsize=9)
cb2.set_ticks([0,10,20,30,40,50,60,70,80,90,100])
cb2.set_label('%', fontsize=9)

# 第三个子图
clev=np.arange(-40,41,5)
pdata3, plon3 = add_cyclic_point(model_mean[4,:,:]-data_out[4,:,:,20], coord=olon)
c3 = axes[2].contourf(plon3, olat, pdata3, clev, transform=ccrs.PlateCarree(central_longitude=0), cmap='BrBG', extend='both')
axes[2].set_extent([-180, 180, -60, 60])
axes[2].set_xlim(-180,180)
axes[2].coastlines(resolution='110m', linewidth=0.75)
# axes[2].set_yticks([-60,-30,0,30,60])
# axes[2].set_yticklabels(['60$^\circ$S','30$^\circ$S','0','30$^\circ$N','60$^\circ$N'],fontsize=9)
axes[2].set_xticks([-90,0,90])
axes[2].set_xticklabels(['90$^\circ$E','0','90$^\circ$W'],fontsize=9)
axes[2].set_title('(c) CLT,Bias', loc='left', fontsize=9)
c3.set_clim(vmin=-40,vmax=40)

# 第三个子图的colorbar
cax3 = fig.add_axes([0.66, 0.1, 0.24, 0.02])  # [left, bottom, width, height]
cb3 = plt.colorbar(c3, cax=cax3, orientation='horizontal')
cb3.ax.tick_params(labelsize=9)
cb3.set_ticks([-40,-20,0,20,40])
cb3.set_label('%', fontsize=9)

plt.savefig('../fig/cloud_map.svg',bbox_inches='tight')