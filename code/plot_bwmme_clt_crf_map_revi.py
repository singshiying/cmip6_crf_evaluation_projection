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
##based on time variability
bmme=['CESM2-WACCM','BCC-CSM2-MR','CMCC-CM2-SR5','MPI-ESM1-2-HR']
wmme=['INM-CM4-8','FGOALS-g3','INM-CM5-0','IPSL-CM6A-LR']
##base on csr
# bmme=['GFDL-ESM4','MRI-ESM2-0','MPI-ESM1-2-HR','CESM2-WACCM']
# wmme=['INM-CM4-8','CAS-ESM2-0','INM-CM5-0','KIOST-ESM']


def calc_significance_p(bmme_data,wmme_data,obs):
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
    bmme_bias = bmme_data - obs  # 自动广播obs到模型维度
    # WMME各模型偏差：(lat, lon, n_wmme)
    wmme_bias = wmme_data - obs
    
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
    
    valid_mask = ~np.isnan(obs.values.flatten())
    sig_field = np.full_like(obs.values.flatten(), np.nan)
    # 显著条件：|平均差异| > 1.96×合并标准误（95%置信水平）
    sig_field[valid_mask] = np.where(
        mean_diff[valid_mask] > 1.943 * pooled_se[valid_mask],
        1,  # 差异显著
        0   # 差异不显著
    )
    
    return sig_field.reshape((180,360))


toanet_p = calc_significance_p(bmme_data=data_out_xr.sel(vars=[0,1], models=bmme).sum('vars'),wmme_data=data_out_xr.sel(vars=[0,1], models=wmme).sum('vars'),obs=data_out_xr.sel(vars=[0,1], models='OBS').sum('vars'))
atmnet_p = calc_significance_p(bmme_data=data_out_xr.sel(vars=[2,3], models=bmme).sum('vars'),wmme_data=data_out_xr.sel(vars=[0,1], models=wmme).sum('vars'),obs=data_out_xr.sel(vars=[2,3], models='OBS').sum('vars'))
sfcnet_p = calc_significance_p(bmme_data=data_out_xr.sel(vars=[0,1], models=bmme).sum('vars')-data_out_xr.sel(vars=[2,3], models=bmme).sum('vars'),wmme_data=data_out_xr.sel(vars=[0,1], models=wmme).sum('vars')-data_out_xr.sel(vars=[2,3], models=wmme).sum('vars'),obs=data_out_xr.sel(vars=[0,1], models='OBS').sum('vars')-data_out_xr.sel(vars=[2,3], models='OBS').sum('vars'))

def draw(fig,axe,num,label,clev,data,p_field=None):
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
    axe.set_title(label,loc='left',fontsize=7)
    axe.set_aspect('auto')
    # 新增：绘制显著性等值线（p<0.05的区域边界）
    if p_field is not None:
        # 处理p值场的循环点（避免经度0°缺口）
        pdata_cyclic, _ = add_cyclic_point(p_field, coord=olon)
        sig_overlay = np.where(pdata_cyclic < 0.05, np.nan, 1)
        
        # 2.3 绘制显著性色块
        cs=axe.contourf(
            plon, olat, sig_overlay,  # 显著性掩码（仅显著区域有值）
            levels=[0.5, 1.5],        # 仅绘制“1”对应的区域（0.5~1.5包含1）
            colors='none',          # 填充色：先设为透明（用于后续设置edgecolor）
            hatches=['...'],          # 可选：添加斜线纹理（增强视觉区分，无纹理可删）
            transform=ccrs.PlateCarree(),
            zorder=3,                 # 图层优先级：介于填色图（1）和海岸线（5）之间
        )
        # cs.collections[0].set_edgecolor('yellow')
        # cs.collections[0].set_linewidth(0.1)

    return c




t1=data_out_xr.loc[0,:,:,list(set(bmme))].mean('models')+data_out_xr.loc[1,:,:,list(set(bmme))].mean('models')-(data_out_xr.loc[0,:,:,'OBS']+data_out_xr.loc[1,:,:,'OBS'])
t2=data_out_xr.loc[0,:,:,list(set(wmme))].mean('models')+data_out_xr.loc[1,:,:,list(set(wmme))].mean('models')-(data_out_xr.loc[0,:,:,'OBS']+data_out_xr.loc[1,:,:,'OBS'])
t3=data_out_xr.loc[2,:,:,list(set(bmme))].mean('models')+data_out_xr.loc[3,:,:,list(set(bmme))].mean('models')-(data_out_xr.loc[3,:,:,'OBS']+data_out_xr.loc[2,:,:,'OBS'])
t4=data_out_xr.loc[2,:,:,list(set(wmme))].mean('models')+data_out_xr.loc[3,:,:,list(set(wmme))].mean('models')-(data_out_xr.loc[3,:,:,'OBS']+data_out_xr.loc[2,:,:,'OBS'])
t5=t1-t3
t6=t2-t4

fig,axes=plt.subplots(3,3,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})

fig.subplots_adjust(wspace=0.05,hspace=0.17,right=0.9,top=0.9,bottom=0.1)
fig.set_figheight(6)
fig.set_figwidth(7.75)
fig.set_dpi(300)
clev=np.arange(-50,51,5)
c1=draw(fig,axes[0][0],1,'(a) TOA NETCRF,BMME Bias',clev,t1)
c2=draw(fig,axes[0][1],2,'(b) TOA NETCRF,WMME Bias',clev,t2)
c3=draw(fig,axes[0][2],2,'(c) TOA NETCRF,WMME Bias-BMME Bias',clev,t2-t1,toanet_p)
c3=draw(fig,axes[1][0],3,'(d) ATM NETCRF,BMME Bias',clev,t3)
c4=draw(fig,axes[1][1],4,'(e) ATM NETCRF,WMME Bias',clev,t4)
c4=draw(fig,axes[1][2],2,'(f) ATM NETCRF,WMME Bias-BMME Bias',clev,t4-t3,atmnet_p)
c5=draw(fig,axes[2][0],5,'(g) SFC NETCRF,BMME Bias',clev,t5)
c6=draw(fig,axes[2][1],6,'(h) SFC NETCRF,WMME Bias',clev,t6)
c2=draw(fig,axes[2][2],6,'(i) SFC NETCRF,WMME Bias-BMME Bias',clev,t6-t5,sfcnet_p)
position = fig.add_axes([0.92, 0.1, 0.010, 0.8])#位置[左,下,宽,高]
cb=fig.colorbar(c2,shrink=0.8,cax=position,fraction=0.03, format='% 1.0f')
cb.ax.tick_params(labelsize=9)
cb.set_label('W m$^{-2}$', fontsize=9,rotation=270)
plt.savefig('../fig/bwmme_crf_map.svg',bbox_inches='tight')