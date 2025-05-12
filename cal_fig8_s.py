#计算ssp5852080-2099平均的latxlon 场
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
model_his='/data04/shiy/cmip6_his_ssp585/ssp585/'
data_out=np.zeros((5,180,360,len(models)))#toa cre,sfc cre,clt;models+cas
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
time_len=240
lon_len=360
lat_len=180
lat_weight=np.cos(np.deg2rad(olat))
lat_lon_weight=np.repeat(lat_weight,lon_len).reshape(lat_len,lon_len)
time_lat_lon_weight=np.tile(lat_lon_weight,(time_len,1,1))
#先取出cas的历史实验各个变量并求areamean
print('cas-esm2')
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rsutcs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsutcs=xr.open_dataset(cas_path)['rsutcs'].loc['2080-01-01':'2099-12-31',-90:90,0:360]
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rsut/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsut=xr.open_dataset(cas_path)['rsut'].loc['2080-01-01':'2099-12-31',-90:90,0:360]
sw_crf=rsutcs-rsut#短波云辐射强迫
sw_crf=sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
sw_crf.data=sw_crf.data/time_lat_lon_weight
sw_crf_weighted_mean=sw_crf.mean(('time'))
data_out[0,:,:,4]=sw_crf_weighted_mean.values
# print(sw_crf_weighted_mean)
#lwcrf
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rlutcs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rlutcs=xr.open_dataset(cas_path)['rlutcs'].loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rlut/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rlut=xr.open_dataset(cas_path)['rlut'].loc['2080-01-01':'2099-12-31',-90:90,0:360] 
lw_crf=rlutcs-rlut
lw_crf=lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
lw_crf_weighted_mean=lw_crf.mean(('time'))
data_out[1,:,:,4]=lw_crf_weighted_mean.values
#求sfc sw crf
#rsds-rsus-rsdscs+rsuscs
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rsus/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsus=xr.open_dataset(cas_path)['rsus'].loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rsds/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsds=xr.open_dataset(cas_path)['rsds'].loc['2080-01-01':'2099-12-31',-90:90,0:360] 
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rsdscs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsdscs=xr.open_dataset(cas_path)['rsdscs'].loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rsuscs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rsuscs=xr.open_dataset(cas_path)['rsuscs'].loc['2080-01-01':'2099-12-31',-90:90,0:360] 
sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
sfc_sw_crf=sfc_sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
data_out[2,:,:,4]=sfc_sw_crf.mean(('time')).values
#求sfc lw crf
#rlds-rldscs
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rldscs/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rldscs=xr.open_dataset(cas_path)['rldscs'].loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/rlds/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
rlds=xr.open_dataset(cas_path)['rlds'].loc['2080-01-01':'2099-12-31',-90:90,0:360] 
sfc_lw_crf=rlds-rldscs
sfc_lw_crf=sfc_lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
data_out[3,:,:,4]=sfc_lw_crf.mean(('time')).values
#求clt
cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp585/r1i1p1f1/Amon/clt/'
cas_path=cas_his+os.listdir(cas_his)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]+'/'
cas_path=cas_path+os.listdir(cas_path)[0]
clt=xr.open_dataset(cas_path)['clt'].loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
clt=clt.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
data_out[4,:,:,4]=clt.mean(('time')).values
for m in range(len(models)):
    if m!=4:
        print(models[m])
        #求swcrf
        fhis=glob.glob(model_his+models[m]+'/rsutcs_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rsutcs']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rsutcs=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rsut_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rsut']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rsut=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] 
        sw_crf=rsutcs-rsut
        sw_crf=sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        sw_crf.data=sw_crf.data/time_lat_lon_weight
        data_out[0,:,:,m]=sw_crf.mean(('time')).values
        #求lwcrf
        fhis=glob.glob(model_his+models[m]+'/rlutcs_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rlutcs']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rlutcs=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rlut_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rlut']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rlut=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] 
        lw_crf=rlutcs-rlut
        lw_crf=lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[1,:,:,m]=lw_crf.mean(('time')).values
        #求sfc sw cre
        fhis=glob.glob(model_his+models[m]+'/rsds_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rsds']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rsds=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rsus_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rsus']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rsus=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] 
        fhis=glob.glob(model_his+models[m]+'/rsuscs_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rsuscs']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rsuscs=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rsdscs_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rsdscs']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rsdscs=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] 
        sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
        sfc_sw_crf=sfc_sw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[2,:,:,m]=sfc_sw_crf.mean(('time')).values
        #求sfc lw cre
        fhis=glob.glob(model_his+models[m]+'/rlds_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rlds']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rlds=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
        fhis=glob.glob(model_his+models[m]+'/rldscs_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['rldscs']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        rldscs=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] 
        sfc_lw_crf=rlds-rldscs
        sfc_lw_crf=sfc_lw_crf.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[3,:,:,m]=sfc_lw_crf.mean(('time')).values
        #求clt
        fhis=glob.glob(model_his+models[m]+'/clt_Amon_'+models[m]+'_ssp585_r1i1p1f1'+'*201501-210012.nc')[0]
        fhis_data=xr.open_dataset(fhis)['clt']
        if len(fhis_data['time'])==1032:
            fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
        clt=fhis_data.loc['2080-01-01':'2099-12-31',-90:90,0:360] #240x48x192
        clt=clt.interp(lat=olat,lon=olon,kwargs={'fill_value': 'extrapolate'})
        data_out[4,:,:,m]=clt.mean(('time')).values

da = os.path.exists('fig8_s.npy')
if da:
    os.remove('fig8_s.npy')

print(data_out.shape)
np.save('fig8_s.npy',data_out)