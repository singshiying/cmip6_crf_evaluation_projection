#seasonal vi
############5varx180latx360lonx20model+AMME
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
#models=['ACCESS-CM2','BCC-CSM2-MR','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3']
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
#20models
model_his='/data04/shiy/cmip6_his_ssp585/historical/'
model_ssp585='/data04/shiy/cmip6_his_ssp585/ssp585/'
data_out=np.zeros((5,12,180,360,len(models)+1))#toa cre,sfc cre,clt;models+cas+obs
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
time_len=168
lon_len=360
lat_len=180
lat_weight=np.cos(np.deg2rad(olat))
lat_lon_weight=np.repeat(lat_weight,lon_len).reshape(lat_len,lon_len)
time_lat_lon_weight=np.tile(lat_lon_weight,(time_len,1,1))
print('cas-esm2')
#cas-esm2
#swcrf
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rsut/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsut=xr.open_dataset(cas_path)['rsut'].loc['2001-01-01':'2014-12-30',-90:90,0:360]
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rsutcs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsutcs=xr.open_dataset(cas_path)['rsutcs'].loc['2001-01-01':'2014-12-30',-90:90,0:360]
sw_crf=rsutcs-rsut
sw_crf=sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
# sw_crf.data=sw_crf.data/time_lat_lon_weight
sw_crf_weighted_mean=sw_crf.groupby('time.month').mean()#12x180x360
print(sw_crf_weighted_mean.values.shape)
data_out[0,:,:,:,4]=sw_crf_weighted_mean.values
#lwcrf
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rlutcs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rlutcs=xr.open_dataset(cas_path)['rlutcs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rlut/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rlut=xr.open_dataset(cas_path)['rlut'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
lw_crf=rlutcs-rlut
lw_crf=lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
lw_crf_weighted_mean=lw_crf.groupby('time.month').mean()
data_out[1,:,:,:,4]=lw_crf_weighted_mean.values
#sfc sw crf
#rsds-rsus-rsdscs+rsuscs
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rsus/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsus=xr.open_dataset(cas_path)['rsus'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rsds/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsds=xr.open_dataset(cas_path)['rsds'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rsdscs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsdscs=xr.open_dataset(cas_path)['rsdscs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rsuscs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsuscs=xr.open_dataset(cas_path)['rsuscs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
sfc_sw_crf=sfc_sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
data_out[2,:,:,:,4]=sw_crf_weighted_mean.values-sfc_sw_crf.groupby('time.month').mean().values
#sfc lw crf
#rlds-rldscs
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rldscs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rldscs=xr.open_dataset(cas_path)['rldscs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/rlds/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rlds=xr.open_dataset(cas_path)['rlds'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
sfc_lw_crf=rlds-rldscs
sfc_lw_crf=sfc_lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
data_out[3,:,:,:,4]=lw_crf_weighted_mean.values-sfc_lw_crf.groupby('time.month').mean().values
#clt
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/CMIP/CAS/CAS-ESM2-0/historical/r1i1p1f1/Amon/clt/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
clt=xr.open_dataset(cas_path)['clt'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
clt=clt.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
data_out[4,:,:,:,4]=clt.groupby('time.month').mean().values
for m in range(len(models)):
    if m!=4:
        print(models[m])
        #swcrf
        fhis=glob.glob(model_his+models[m]+'/rsutcs_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rsutcs=xr.open_dataset(fhis)['rsutcs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rsut_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rsut=xr.open_dataset(fhis)['rsut'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
        sw_crf=rsutcs-rsut
        sw_crf=sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        # sw_crf.data=sw_crf.data/time_lat_lon_weight
        data_out[0,:,:,:,m]=sw_crf.groupby('time.month').mean().values
        #lwcrf
        fhis=glob.glob(model_his+models[m]+'/rlutcs_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rlutcs=xr.open_dataset(fhis)['rlutcs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rlut_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rlut=xr.open_dataset(fhis)['rlut'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
        lw_crf=rlutcs-rlut
        lw_crf=lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[1,:,:,:,m]=lw_crf.groupby('time.month').mean().values
        #sfc sw cre
        fhis=glob.glob(model_his+models[m]+'/rsds_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rsds=xr.open_dataset(fhis)['rsds'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rsus_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rsus=xr.open_dataset(fhis)['rsus'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
        fhis=glob.glob(model_his+models[m]+'/rsuscs_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rsuscs=xr.open_dataset(fhis)['rsuscs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rsdscs_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rsdscs=xr.open_dataset(fhis)['rsdscs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
        sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
        sfc_sw_crf=sfc_sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[2,:,:,:,m]=sw_crf.groupby('time.month').mean().values-sfc_sw_crf.groupby('time.month').mean().values
        #sfc lw cre
        fhis=glob.glob(model_his+models[m]+'/rlds_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rlds=xr.open_dataset(fhis)['rlds'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rldscs_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        rldscs=xr.open_dataset(fhis)['rldscs'].loc['2001-01-01':'2014-12-30',-90:90,0:360] 
        sfc_lw_crf=rlds-rldscs
        sfc_lw_crf=sfc_lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[3,:,:,:,m]=lw_crf.groupby('time.month').mean().values-sfc_lw_crf.groupby('time.month').mean().values
        #clt
        fhis=glob.glob(model_his+models[m]+'/clt_Amon_'+models[m]+'_historical_r1i1p1f1'+'*185001-201412.nc')[0]
        # if m==7:
        #     # print('CIESM')
        #     clt=xr.open_dataset(fhis)['clt'].loc['2001-01-01':'2014-12-30',-90:90,0:360]*100 #240x48x192
        # else:
        clt=xr.open_dataset(fhis)['clt'].loc['2001-01-01':'2014-12-30',-90:90,0:360] #240x48x192
        clt=clt.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[4,:,:,:,m]=clt.groupby('time.month').mean().values

#obs
print('obs')
##ceres 200101-201412
ceres_path='/data04/shiy/observation/CERES_EBAF_Edition4.1_200003-202011.nc'
fc=xr.open_dataset(ceres_path)
sw_crf=fc['toa_cre_sw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
# sw_crf.data=sw_crf.data/time_lat_lon_weight
data_out[0,:,:,:,len(models)]=sw_crf.groupby('time.month').mean().values
lw_crf=fc['toa_cre_lw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
data_out[1,:,:,:,len(models)]=lw_crf.groupby('time.month').mean().values
sfc_sw_crf=fc['sfc_cre_net_sw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
data_out[2,:,:,:,len(models)]=sw_crf.groupby('time.month').mean().values-sfc_sw_crf.groupby('time.month').mean().values
sfc_lw_crf=fc['sfc_cre_net_lw_mon'].loc['2001-01-01':'2014-12-30',-90:90,0:360]#time,lat,lon
data_out[3,:,:,:,len(models)]=lw_crf.groupby('time.month').mean().values-sfc_lw_crf.groupby('time.month').mean().values
#ISCCP-h
isccp_path='/data04/shiy/observation/isccph/isccp-basic.HGM.200101-201412.nc'
clt=xr.open_dataset(isccp_path)['cldamt'].loc['2001-01-01':'2014-12-30',-90:90,0:360]
data_out[4,:,:,:,len(models)]=clt.groupby('time.month').mean().values

def cal_VI(ref,sample):
    stdref=np.nanstd(ref[:,:,:,:],axis=1,ddof=1)
    stdref2=np.repeat(stdref,sample.shape[4],axis=2).reshape(5,180,360,sample.shape[4])
    stdsamp=np.nanstd(sample[:,:,:,:,:],axis=1,ddof=1)
    VI=(stdsamp/stdref2-stdref2/stdsamp)**2#5x180x360x24
    return VI
def cal_VI2(ref,sample):
    stdref=np.nanstd(ref[:,:,:,:],axis=1,ddof=1)
    # stdref2=np.repeat(stdref,sample.shape[4],axis=2).reshape(5,180,360,sample.shape[4])
    # print(stdref2[:,:,:,0])
    # print(stdref2[:,:,:,12])
    stdsamp=np.nanmean(np.nanstd(sample[:,:,:,:,:],axis=1,ddof=1),axis=3)
    VI=(stdsamp/stdref-stdref/stdsamp)**2#5x180x360
    return VI
data_out2=np.zeros((5,180,360,21))
data_out2[:,:,:,0:20]=cal_VI(data_out[:,:,:,:,20],data_out[:,:,:,:,0:20])
data_out2[:,:,:,20]=cal_VI2(data_out[:,:,:,:,20],data_out[:,:,:,:,0:20])
# data_out2[:,:,:,20]=np.nanmean(data_out2[:,:,:,0:20],3)
da = os.path.exists('fig4_s2_v2.npy')
if da:
    os.remove('fig4_s2_v2.npy')

print(data_out2.shape)
np.save('fig4_s2_v2.npy',data_out2)