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


# bmme=['EC-Earth3-CC','MPI-ESM1-2-HR']
# wmme=['FGOALS-g3','CAS-ESM2-0']
##based on all
# bmme=['CMCC-CM2-SR5','EC-Earth3-CC','MPI-ESM1-2-HR','MPI-ESM1-2-LR']
# wmme=['CAS-ESM2-0','FGOALS-g3','INM-CM4-8','NESM3']
##based on clt
# bmme=['MPI-ESM1-2-LR','MIROC6','EC-Earth3-CC']
# wmme=['ACCESS-CM2','CESM2-WACCM','CAS-ESM2-0']
# #based on crf
# bmme=['EC-Earth3-CC','CESM2-WACCM','ACCESS-CM2']
# wmme=['CAS-ESM2-0','FGOALS-g3','INM-CM4-8']

##clt only 60NS
##based on all
# bmme=['CESM2-WACCM','EC-Earth3-CC','MPI-ESM1-2-HR','ACCESS-CM2']
wmme=['CAS-ESM2-0','FGOALS-g3','INM-CM4-8','NESM3']
bmme=['CESM2-WACCM','EC-Earth3-CC','MPI-ESM1-2-HR','GFDL-ESM4']



##读取ceres的200101-201412数据
obs=np.zeros([6,14])
ceres_path='/data04/shiy/observation/CERES_EBAF_Edition4.1_200003-202011.nc'
fc=xr.open_dataset(ceres_path)
sw_crf=fc['toa_cre_sw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
weights=np.cos(np.deg2rad(sw_crf.coords['lat']))
obs[0,:]=sw_crf.weighted(weights).mean(('lon','lat')).groupby('time.year').mean().values
lw_crf=fc['toa_cre_lw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
weights=np.cos(np.deg2rad(lw_crf.coords['lat']))
obs[1,:]=lw_crf.weighted(weights).mean(('lon','lat')).groupby('time.year').mean().values
sfc_sw_crf=fc['sfc_cre_net_sw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
obs[2,:]=sfc_sw_crf.weighted(weights).mean(('lon','lat')).groupby('time.year').mean().values
sfc_lw_crf=fc['sfc_cre_net_lw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
obs[3,:]=sfc_lw_crf.weighted(weights).mean(('lon','lat')).groupby('time.year').mean().values
#读取ISCCP-h
isccp_path='/data04/shiy/observation/isccph/isccp-basic.HGM.200101-201412.nc'
clt=xr.open_dataset(isccp_path)['cldamt'].loc['2001-01-01':'2014-12-30',-90:90,0:360]
obs[4,:]=clt.weighted(weights).mean(('lon','lat')).groupby('time.year').mean().values
tas_path='/data04/shiy/observation/air.2m.mon.mean.nc'
tas=xr.open_dataset(tas_path)['air'].loc['2001-01-01':'2014-12-30',:,:]
weights=np.cos(np.deg2rad(tas.coords['lat']))
obs[5,:]=tas.weighted(weights).mean(('lon','lat')).groupby('time.year').mean().values
obs2=np.zeros([6,14])
for i in range(14):
    obs2[:,i]=obs[:,i]-np.mean(obs,1)

data_out1=np.load('../fig7_1.npy')[:,:,:]#6areax5varx1980timex24models历史实验
data_out2=np.load('../fig7_2.npy')[:,:,:]#ssp245实验
data_out3=np.load('../fig7_3.npy')[:,:,:]#6areax5varx1020timex24models
ssp245_ts=np.concatenate((data_out1,data_out2),axis = 1)
ssp585_ts=np.concatenate((data_out1,data_out3),axis = 1)
time=pd.date_range('18500101','20991231',freq='M')
models23=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
ssp245_ts_xr=xr.DataArray(ssp245_ts,coords=[np.arange(0,6,1),time,models23],dims=['vars','time','models'])
ssp585_ts_xr=xr.DataArray(ssp585_ts,coords=[np.arange(0,6,1),time,models23],dims=['vars','time','models'])

models20=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']


def draw3_range(ax,ssp245_all,ssp245_bmme,ssp245_wmme,ssp585_all,ssp585_bmme,ssp585_wmme,obsp,label,num):
    x=np.arange(2001,2100,1)
    x1=np.arange(2001,2015,1)
    x2=np.arange(2014,2100,1)
    ax.set_xlim(2001,2100)
    ax.fill_between(x2,np.min(ssp585_bmme,1)[13:99],np.max(ssp585_bmme,1)[13:99],alpha=0.2,color='r',label='SSP585 BMME range')
    ax.plot(x2,ssp585_bmme.mean('models')[13:99],'r-',label='ssp585 BMME',linewidth=0.75)
    ax.plot(x2,ssp245_bmme.mean('models')[13:99],'r--',label='ssp245 BMME',linewidth=0.75)
    ax.plot(x1,ssp245_bmme.mean('models')[0:14],'r-',label='historical BMME',linewidth=0.75,alpha=0.5)
    ax.plot(x,[0]*99,color='gray',linestyle='--')
    ax.fill_between(x2,np.min(ssp585_wmme,1)[13:99],np.max(ssp585_wmme,1)[13:99],alpha=0.2,color='b',label='SSP585 WMME range')
    ax.plot(x2,ssp585_wmme.mean('models')[13:99],'b-',label='ssp585 WMME',linewidth=0.75)
    ax.plot(x2,ssp245_wmme.mean('models')[13:99],'b--',label='ssp245 WMME',linewidth=0.75)
    ax.plot(x1,ssp245_wmme.mean('models')[0:14],'b-',label='historical WMME',linewidth=0.75,alpha=0.5)
    ax.plot(x2,np.mean(ssp585_all,1)[13:99],'k-',label='ssp585 AMME',linewidth=0.75)
    ax.plot(x2,np.mean(ssp245_all,1)[13:99],'k--',label='ssp245 AMME',linewidth=0.75)
    ax.plot(x1,np.mean(ssp245_all,1)[0:14],'k-',label='historical AMME',linewidth=0.75,alpha=0.5)
    ax.fill_between(x1,np.min(ssp245_all,1)[0:14],np.max(ssp245_all,1)[0:14],alpha=0.2,color='k')
    ax.plot(x1,obsp,'y--',label='OBS',linewidth=0.75)
    ax.set_title(label,loc='left',fontsize=9)
    ax.tick_params(axis='x',labelsize=9)
    ax.tick_params(axis='y',labelsize=9)
    ax.set_xticks(np.arange(2001,2100,20))
    if num==1:
        ax.legend(fontsize=9,bbox_to_anchor=(1,1))

t1=(ssp245_ts_xr.loc[0,:,models20]+ssp245_ts_xr.loc[1,:,models20]).groupby('time.year').mean().loc['2001':'2101']
t2=(ssp585_ts_xr.loc[0,:,models20]+ssp585_ts_xr.loc[1,:,models20]).groupby('time.year').mean().loc['2001':'2101']
t3=(ssp245_ts_xr.loc[2,:,models20]+ssp245_ts_xr.loc[3,:,models20]).groupby('time.year').mean().loc['2001':'2101']
t4=(ssp585_ts_xr.loc[2,:,models20]+ssp585_ts_xr.loc[3,:,models20]).groupby('time.year').mean().loc['2001':'2101']
t5=ssp245_ts_xr.loc[4,:,models20].groupby('time.year').mean().loc['2001':'2101']
t6=ssp585_ts_xr.loc[4,:,models20].groupby('time.year').mean().loc['2001':'2101']
t7=ssp245_ts_xr.loc[5,:,models20].groupby('time.year').mean().loc['2001':'2101']
t8=ssp585_ts_xr.loc[5,:,models20].groupby('time.year').mean().loc['2001':'2101']
t1=t1-np.mean(t1[0:14,:],0)
t2=t2-np.mean(t2[0:14,:],0)
t3=t3-np.mean(t3[0:14,:],0)
t4=t4-np.mean(t4[0:14,:],0)
t5=t5-np.mean(t5[0:14,:],0)
t6=t6-np.mean(t6[0:14,:],0)
t7=t7-np.mean(t7[0:14,:],0)
t8=t8-np.mean(t8[0:14,:],0)

fig,ax=plt.subplots(4,1,figsize=(5.5,10),dpi=300)
fig.subplots_adjust(hspace=0.2) # Adjust vertical spacing between subplots
colors=plt.cm.nipy_spectral(np.linspace(0,1,20))
draw3_range(ax[0],t1,t1.loc[:,list(set(bmme))],t1.loc[:,list(set(wmme))],t2,t2.loc[:,list(set(bmme))],t2.loc[:,list(set(wmme))],obs2[0,:]+obs2[1,:],'a) TOA NETCRF',1)
draw3_range(ax[1],t3,t3.loc[:,list(set(bmme))],t3.loc[:,list(set(wmme))],t4,t4.loc[:,list(set(bmme))],t4.loc[:,list(set(wmme))],obs2[2,:]+obs2[3,:],'b) SFC NETCRF',2)
draw3_range(ax[2],t5,t5.loc[:,list(set(bmme))],t5.loc[:,list(set(wmme))],t6,t6.loc[:,list(set(bmme))],t6.loc[:,list(set(wmme))],obs2[4,:],'c) CLT',3)
draw3_range(ax[3],t7,t7.loc[:,list(set(bmme))],t7.loc[:,list(set(wmme))],t8,t8.loc[:,list(set(bmme))],t8.loc[:,list(set(wmme))],obs2[5,:],'d) Tas',4)
plt.savefig('../fig/bwmme_ssp_trend.svg',bbox_inches='tight')