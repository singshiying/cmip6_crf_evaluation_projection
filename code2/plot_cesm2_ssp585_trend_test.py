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

data_out3=np.load('../fig7_3.npy')[:,:,:]#5varx1020timex24models
# data_out3=xr.open_dataarray('./ssp585_crf_clt_cas-esm2.nc')[:,0:1020]
time=pd.date_range('20150101','20991231',freq='M')
models23=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
ssp585_ts_xr=xr.DataArray(data_out3,coords=[np.arange(0,6,1),time,models23],dims=['vars','time','models'])


toa_netcrf_yearly = (ssp585_ts_xr.loc[2,:,'CESM2-WACCM']+ssp585_ts_xr.loc[3,:,'CESM2-WACCM']).groupby('time.year').mean()

# Create figure and plot
plt.switch_backend('agg')
plt.figure(figsize=(10,6))
plt.plot(toa_netcrf_yearly.year, toa_netcrf_yearly.values, '-k', linewidth=2)
plt.xlabel('Year')
plt.ylabel('SFC Net CRF (W/m²)')
plt.title('SFC Net Cloud Radiative Forcing -CESM2-WACCM SSP585')
plt.grid(True)

# Save figure
plt.savefig('../fig/ssp585_sfc_netcrf_yearly_CESM2-WACCM.png', dpi=300, bbox_inches='tight')
plt.close()
