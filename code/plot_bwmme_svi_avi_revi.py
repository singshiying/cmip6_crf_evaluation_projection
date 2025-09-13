import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
import matplotlib.gridspec as gridspec
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()

data_out2=np.load('./fig4_s2_v2_add.npy')#3x180x360x21  sVI指数
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','AMME']
data_out_xr2=xr.DataArray(data_out2,coords=[np.arange(0,3,1),olat,olon,models],dims=['vars','lat','lon','models'])

data_out3=np.load('./fig4_s3_v2_add.npy')#53x180x360x21  aVI指数
data_out_xr3=xr.DataArray(data_out3,coords=[np.arange(0,3,1),olat,olon,models],dims=['vars','lat','lon','models'])
##base on vi
# bmme=['CESM2-WACCM','BCC-CSM2-MR','CMCC-CM2-SR5','MPI-ESM1-2-HR']#,'ACCESS-ESM1-5'
# wmme=['INM-CM4-8','FGOALS-g3','INM-CM5-0','IPSL-CM6A-LR']#,'CAS-ESM2-0'
# bmme=['CESM2-WACCM','BCC-CSM2-MR']
# wmme=['INM-CM4-8','FGOALS-g3']
bmme=['CESM2-WACCM','BCC-CSM2-MR','CMCC-CM2-SR5','MPI-ESM1-2-HR']
wmme=['INM-CM4-8','FGOALS-g3','INM-CM5-0','IPSL-CM6A-LR']
##base on csr
# bmme=['GFDL-ESM4','MRI-ESM2-0','MPI-ESM1-2-HR','CESM2-WACCM']
# wmme=['INM-CM4-8','CAS-ESM2-0','INM-CM5-0','KIOST-ESM']

def calc_significance_p(bmme_data,wmme_data):
    """
    计算每个格点的显著性p值：检验「BMME集合平均偏差」与「WMME集合平均偏差」的差异是否显著
    核心修改：
        1. 移除纬度权重逻辑
        2. 基于BMME/WMME各自集合内部的模型偏差计算标准差
        3. 使用合并标准误判断显著性（95%置信水平：1.96倍标准误）
    
    参数：
        vars_idx: 变量索引（0=TOA SW, 1=TOA LW, 2=ATM SW, 3=ATM LW）
    返回：
        sig_field: (lat, lon) 数组，1=差异显著，0=不显著，NaN=数据无效
    """  
    # 计算每个模型相对于OBS的偏差（核心：偏差=模型值-观测值）
    # BMME各模型偏差：(lat, lon, n_bmme)
    bmme_bias = bmme_data 
    # WMME各模型偏差：(lat, lon, n_wmme)
    wmme_bias = wmme_data 
    
    # 计算BMME/WMME的集合平均偏差（用于后续求差异）
    # BMME平均偏差：(lat, lon) → 每个格点的BMME平均偏差
    bmme_mean_bias = bmme_bias.mean(dim='models')
    # WMME平均偏差：(lat, lon) → 每个格点的WMME平均偏差
    wmme_mean_bias = wmme_bias.mean(dim='models')
    # 平均偏差差异的绝对值：|BMME平均 - WMME平均|
    mean_diff = np.abs(bmme_mean_bias.values - wmme_mean_bias.values).flatten()
    
    # 计算BMME/WMME集合内部的标准差（反映集合不确定性）
    # BMME内部标准差：(lat, lon) → 每个格点的BMME模型偏差标准差（ddof=1：无偏估计）
    bmme_std = bmme_bias.std(dim='models', ddof=1).values.flatten()
    # WMME内部标准差：(lat, lon) → 每个格点的WMME模型偏差标准差
    wmme_std = wmme_bias.std(dim='models', ddof=1).values.flatten()
    
    # 计算合并标准误（适用于两个独立样本的显著性检验）
    # n_bmme/WMME：BMME/WMME的模型数量（标量，如4）
    n_bmme = len(bmme)
    n_wmme = len(wmme)
    # 合并方差 = [(n1-1)*s1² + (n2-1)*s2²] / (n1+n2-2)
    pooled_var = ((n_bmme - 1) * bmme_std**2 + (n_wmme - 1) * wmme_std**2) / (n_bmme + n_wmme - 2)
    # 合并标准误 = sqrt(合并方差 * (1/n1 + 1/n2))
    pooled_se = np.sqrt(pooled_var * (1/n_bmme + 1/n_wmme))
    # print((pooled_se))
    
    # 显著条件：|平均差异| > 1.96×合并标准误（95%置信水平）
    sig_field = np.where(
        mean_diff > 1.44 * pooled_se,
        1,  # 差异显著
        0   # 差异不显著
    )
    
    return sig_field.reshape((180,360))


toanet_sp = calc_significance_p(bmme_data=data_out_xr2.sel(vars=0, models=bmme),wmme_data=data_out_xr2.sel(vars=0, models=wmme))
toanet_ap = calc_significance_p(bmme_data=data_out_xr3.sel(vars=0, models=bmme),wmme_data=data_out_xr3.sel(vars=0, models=wmme))
atmnet_sp = calc_significance_p(bmme_data=data_out_xr2.sel(vars=1, models=bmme),wmme_data=data_out_xr2.sel(vars=1, models=wmme))
atmnet_ap = calc_significance_p(bmme_data=data_out_xr3.sel(vars=1, models=bmme),wmme_data=data_out_xr3.sel(vars=1, models=wmme))


tt1s=data_out_xr2.loc[0,:,:,list(set(bmme))].mean('models')
tt2s=data_out_xr2.loc[1,:,:,list(set(bmme))].mean('models')
tt1a=data_out_xr3.loc[0,:,:,list(set(bmme))].mean('models')
tt2a=data_out_xr3.loc[1,:,:,list(set(bmme))].mean('models')
ttt1s=data_out_xr2.loc[0,:,:,list(set(wmme))].mean('models')
ttt2s=data_out_xr2.loc[1,:,:,list(set(wmme))].mean('models')
ttt1a=data_out_xr3.loc[0,:,:,list(set(wmme))].mean('models')
ttt2a=data_out_xr3.loc[1,:,:,list(set(wmme))].mean('models')

def draw_s(fig, axe, num, label, clev, data, p_field=None, cmap='Reds'):
    pdata, plon = add_cyclic_point(data, coord=olon)
    
    c = axe.contourf(plon, olat, pdata, clev, transform=ccrs.PlateCarree(), 
                     cmap=cmap, extend='both')
    axe.coastlines(resolution='110m', linewidth=0.75)
    
    if num == 1 or num == 3 or num == 5 or num == 7:
        axe.set_yticks([-60, -30, 0, 30, 60])
        axe.set_yticklabels(['60$^\circ$S', '30$^\circ$S', '0', '30$^\circ$N', '60$^\circ$N'], fontsize=9)
    else:
        axe.set_yticks([])
    
    if num == 7 or num == 8:
        axe.set_xticks([-90, 0, 90])
        axe.set_xticklabels(['90$^\circ$E', '0', '90$^\circ$W'], fontsize=9)
    else:
        axe.set_xticks([])
    
    axe.set_title(label, loc='left', fontsize=9)
    
    if p_field is not None:
        pdata_cyclic, _ = add_cyclic_point(p_field, coord=olon)
        sig_overlay = np.where(pdata_cyclic < 0.05, np.nan, 1)
        
        cs = axe.contourf(
            plon, olat, sig_overlay,
            levels=[0.5, 1.5],
            colors='none',
            hatches=['...'],
            transform=ccrs.PlateCarree(),
            zorder=3
        )
    
    return c

# 创建图形
fig = plt.figure(figsize=(9.1, 7.1), dpi=300)
fig.subplots_adjust(top=0.8, bottom=0.1, left=0.05, right=0.95)

# 使用gridspec定义布局：4行，5列（前两列是图，第三列是cb1，第四列是第三列图，第五列是cb2）
gs = gridspec.GridSpec(4, 5, figure=fig, 
                       width_ratios=[1, 1, 0.05, 1, 0.05],  # 列宽比例
                       wspace=0.1, hspace=0.17)

# 定义刻度范围
clev = np.arange(0, 20, 2)
clev_diff = np.arange(-3, 3.5, 0.5)  # 第三列图的刻度范围，根据实际数据调整

# 第一行
ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(central_longitude=180))
c1 = draw_s(fig, ax1, 1, '(a) TOA NETCRF SVI,BMME ', clev, tt1s)

ax2 = fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree(central_longitude=180))
c2 = draw_s(fig, ax2, 2, '(b) TOA NETCRF SVI,WMME', clev, ttt1s)

ax3 = fig.add_subplot(gs[0, 3], projection=ccrs.PlateCarree(central_longitude=180))
c3 = draw_s(fig, ax3, 2, '(c) TOA NETCRF SVI,WMME-BMME', clev_diff, ttt1s-tt1s, toanet_sp, cmap='bwr')

# 第二行
ax4 = fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(central_longitude=180))
c4 = draw_s(fig, ax4, 3, '(d) ATM NETCRF SVI,BMME ', clev, tt2s)

ax5 = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree(central_longitude=180))
c5 = draw_s(fig, ax5, 4, '(e) ATM NETCRF SVI,WMME ', clev, ttt2s)

ax6 = fig.add_subplot(gs[1, 3], projection=ccrs.PlateCarree(central_longitude=180))
c6 = draw_s(fig, ax6, 4, '(f) ATM NETCRF SVI,WMME-BMME ', clev_diff, ttt2s-tt2s, atmnet_sp, cmap='bwr')

# 第三行
ax7 = fig.add_subplot(gs[2, 0], projection=ccrs.PlateCarree(central_longitude=180))
c7 = draw_s(fig, ax7, 5, '(g) TOA NETCRF AVI,BMME ', clev, tt1a)

ax8 = fig.add_subplot(gs[2, 1], projection=ccrs.PlateCarree(central_longitude=180))
c8 = draw_s(fig, ax8, 6, '(h) TOA NETCRF AVI,WMME', clev, ttt1a)

ax9 = fig.add_subplot(gs[2, 3], projection=ccrs.PlateCarree(central_longitude=180))
c9 = draw_s(fig, ax9, 6, '(i) TOA NETCRF AVI,WMME-BMME', clev_diff, ttt1a-tt1a, toanet_ap, cmap='bwr')

# 第四行
ax10 = fig.add_subplot(gs[3, 0], projection=ccrs.PlateCarree(central_longitude=180))
c10 = draw_s(fig, ax10, 7, '(j) ATM NETCRF AVI,BMME ', clev, tt2a)

ax11 = fig.add_subplot(gs[3, 1], projection=ccrs.PlateCarree(central_longitude=180))
c11 = draw_s(fig, ax11, 8, '(k) ATM NETCRF AVI,WMME', clev, ttt2a)

ax12 = fig.add_subplot(gs[3, 3], projection=ccrs.PlateCarree(central_longitude=180))
c12 = draw_s(fig, ax12, 8, '(l) ATM NETCRF AVI,WMME-BMME', clev_diff, ttt2a-tt2a, atmnet_ap, cmap='bwr')

# 添加第一个colorbar（前两列图共用）
cb1_ax = fig.add_subplot(gs[:, 2])  # 跨所有行
cb1 = fig.colorbar(c2, cax=cb1_ax, orientation='vertical')
cb1.ax.tick_params(labelsize=9)
# cb1.set_label('Value', fontsize=9)

# 添加第二个colorbar（第三列图共用）
cb2_ax = fig.add_subplot(gs[:, 4])  # 跨所有行
cb2 = fig.colorbar(c3, cax=cb2_ax, orientation='vertical')
# cb2.ax.tick_params(labelsize=9)
# cb2.set_label('Difference', fontsize=9)

plt.savefig('../fig/bwmme_svi_avi_revi.svg', bbox_inches='tight')