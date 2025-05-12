import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
# models=['ACCESS-CM2','BCC-CSM2-MR','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3']
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
#去除不可以的模式'BCC-CSM2-MR','IPSL-CM6A-LR',
#models=['ACCESS-CM2','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0',  'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3']
area=['-90:90','-10:10','10:30','30:60','60:90'] 
def cal_my_ssp245(num):
    model_his='/data04/shiy/cmip6_his_ssp585/ssp245/'
    if num==0 or num==1:
        #先取出cas的历史实验各个变量并求areamean
        print('cas-esm2')
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsutcs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        pattern=re.compile(r'\-?\d+')#正则表达式对象，\d+代表任意长度数字字符
        area_my=re.findall(pattern,area[num])
        rsutcs=xr.open_dataset(cas_path)['rsutcs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsut/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsut=xr.open_dataset(cas_path)['rsut'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
        sw_crf=rsutcs-rsut#短波云辐射强迫
        # print(sw_crf)
        timelen=sw_crf.shape[0]
        data_out=np.zeros((6,timelen,len(models)))#存储toa crf,sfc crf, clt
        weights=np.cos(np.deg2rad(sw_crf.coords['lat']))#对纬度赋予权重求加权平均
        weights.name='weights'
        # sw_crf_weighted=sw_crf.weighted(weights)
        sw_crf_weighted_mean=sw_crf.weighted(weights).mean(('lon','lat'))
        data_out[0,:,5]=sw_crf_weighted_mean
        # print(sw_crf_weighted_mean)
        #lwcrf
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rlutcs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rlutcs=xr.open_dataset(cas_path)['rlutcs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rlut/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rlut=xr.open_dataset(cas_path)['rlut'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
        lw_crf=rlutcs-rlut
        weights2=np.cos(np.deg2rad(lw_crf.coords['lat']))
        lw_crf_weighted=lw_crf.weighted(weights2)
        lw_crf_weighted_mean=lw_crf_weighted.mean(('lon','lat'))
        data_out[1,:,5]=lw_crf_weighted_mean
        #求sfc sw crf
        #rsds-rsus-rsdscs+rsuscs
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsus/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsus=xr.open_dataset(cas_path)['rsus'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsds/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsds=xr.open_dataset(cas_path)['rsds'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsdscs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsdscs=xr.open_dataset(cas_path)['rsdscs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsuscs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsuscs=xr.open_dataset(cas_path)['rsuscs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
        sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
        sfc_sw_crf_weighted=sfc_sw_crf.weighted(weights2)
        sfc_sw_crf_weighted_mean=sfc_sw_crf_weighted.mean(('lon','lat'))
        data_out[2,:,5]=sfc_sw_crf_weighted_mean
        #求sfc lw crf
        #rlds-rldscs
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rldscs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rldscs=xr.open_dataset(cas_path)['rldscs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rlds/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rlds=xr.open_dataset(cas_path)['rlds'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
        sfc_lw_crf=rlds-rldscs
        sfc_lw_crf_weighted=sfc_lw_crf.weighted(weights2)
        sfc_lw_crf_weighted_mean=sfc_lw_crf_weighted.mean(('lon','lat'))
        data_out[3,:,5]=sfc_lw_crf_weighted_mean
        #求clt
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/clt/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        clt=xr.open_dataset(cas_path)['clt'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        weights=np.cos(np.deg2rad(clt.coords['lat']))
        clt_weighted=clt.weighted(weights)
        clt_weighted_mean=clt_weighted.mean(('lon','lat'))
        data_out[4,:,5]=clt_weighted_mean

        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/tas/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        tas=xr.open_dataset(cas_path)['tas'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        weights=np.cos(np.deg2rad(tas.coords['lat']))
        tas_weighted=tas.weighted(weights)
        tas_weighted_mean=tas_weighted.mean(('lon','lat'))
        data_out[5,:,5]=tas_weighted_mean
        for m in range(len(models)):
            if m!=5:
                print(models[m])
                #求swcrf
                fhis=glob.glob(model_his+models[m]+'/rsutcs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsutcs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsutcs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rsut_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsut']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsut=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                sw_crf=rsutcs-rsut
                weights=np.cos(np.deg2rad(sw_crf.coords['lat']))
                sw_crf_weighted_mean=sw_crf.weighted(weights).mean(('lon','lat'))
                data_out[0,:,m]=sw_crf_weighted_mean
                #求lwcrf
                fhis=glob.glob(model_his+models[m]+'/rlutcs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rlutcs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rlutcs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rlut_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rlut']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rlut=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                lw_crf=rlutcs-rlut
                # print(lw_crf)
                weights2=np.cos(np.deg2rad(lw_crf.coords['lat']))
                lw_crf_weighted=lw_crf.weighted(weights2)
                lw_crf_weighted_mean=lw_crf_weighted.mean(('lon','lat'))
                #annual_lw_crf=lw_crf_weighted_mean.groupby('time.season').mean()
                data_out[1,:,m]=lw_crf_weighted_mean
                #求sfc sw cre
                fhis=glob.glob(model_his+models[m]+'/rsds_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsds']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsds=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rsus_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsus']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsus=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                fhis=glob.glob(model_his+models[m]+'/rsuscs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsuscs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsuscs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rsdscs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsdscs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsdscs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
                sfc_sw_crf_weighted=sfc_sw_crf.weighted(weights2)
                sfc_sw_crf_weighted_mean=sfc_sw_crf_weighted.mean(('lon','lat'))
                #annual_lw_crf=lw_crf_weighted_mean.groupby('time.season').mean()
                data_out[2,:,m]=sfc_sw_crf_weighted_mean
                #求sfc lw cre
                fhis=glob.glob(model_his+models[m]+'/rlds_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rlds']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rlds=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rldscs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rldscs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rldscs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                sfc_lw_crf=rlds-rldscs
                sfc_lw_crf_weighted=sfc_lw_crf.weighted(weights2)
                sfc_lw_crf_weighted_mean=sfc_lw_crf_weighted.mean(('lon','lat'))
                #annual_lw_crf=lw_crf_weighted_mean.groupby('time.season').mean()
                data_out[3,:,m]=sfc_lw_crf_weighted_mean
                #求clt
                fhis=glob.glob(model_his+models[m]+'/clt_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['clt']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                # if m==4 or m==6:
                #     # print('CIESM')
                #     clt=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]*100 #240x48x192
                # else:
                clt=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                weights=np.cos(np.deg2rad(clt.coords['lat']))
                clt_weighted=clt.weighted(weights)
                clt_weighted_mean=clt_weighted.mean(('lon','lat'))
                #annual_clt=clt_weighted_mean.groupby('time.season').mean()
                data_out[4,:,m]=clt_weighted_mean

                fhis=glob.glob(model_his+models[m]+'/tas_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['tas']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                tas=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                weights=np.cos(np.deg2rad(tas.coords['lat']))
                tas_weighted=tas.weighted(weights)
                tas_weighted_mean=tas_weighted.mean(('lon','lat'))
                data_out[5,:,m]=tas_weighted_mean

    else:
        #先取出cas的历史实验各个变量并求areamean
        print('cas-esm2')
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsutcs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        pattern=re.compile(r'\d+')#正则表达式对象，\d+代表任意长度数字字符
        area_my=re.findall(pattern,area[num])
        rsutcs=xr.open_dataset(cas_path)['rsutcs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
        rsutcs2=xr.open_dataset(cas_path)['rsutcs'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360]
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsut/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsut=xr.open_dataset(cas_path)['rsut'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
        rsut2=xr.open_dataset(cas_path)['rsut'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):int(area_my[0]),0:360]
        sw_crf=rsutcs-rsut#短波云辐射强迫
        sw_crf2=rsutcs2-rsut2
        timelen=sw_crf.shape[0]
        data_out=np.zeros((5,timelen,len(models)))#存储toa crf,sfc crf, clt
        # weights=np.cos(np.deg2rad(sw_crf.coords['lat']))#对纬度赋予权重求加权平均
        # weights.name='weights'
        # sw_crf_weighted=sw_crf.weighted(weights)
        weights1=np.cos(np.deg2rad(sw_crf.coords['lat']))
        weights2=np.cos(np.deg2rad(sw_crf2.coords['lat']))
        sw_crf_weighted_mean=sw_crf.weighted(weights1).mean(('lon','lat'))+sw_crf2.weighted(weights2).mean(('lon','lat'))
        data_out[0,:,5]=sw_crf_weighted_mean/2
        #lwcrf
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rlutcs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rlutcs=xr.open_dataset(cas_path)['rlutcs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        rlutcs2=xr.open_dataset(cas_path)['rlutcs'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rlut/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rlut=xr.open_dataset(cas_path)['rlut'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
        rlut2=xr.open_dataset(cas_path)['rlut'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] 
        lw_crf=rlutcs-rlut
        lw_crf2=rlutcs2-rlut2
        # print(lw_crf)
        weights2=np.cos(np.deg2rad(lw_crf.coords['lat']))
        weights22=np.cos(np.deg2rad(lw_crf2.coords['lat']))
        lw_crf_weighted=lw_crf.weighted(weights2)
        lw_crf_weighted2=lw_crf2.weighted(weights22)
        lw_crf_weighted_mean=lw_crf_weighted.mean(('lon','lat'))+lw_crf_weighted2.mean(('lon','lat'))
        #annual_lw_crf=lw_crf_weighted_mean.groupby('time.season').mean()
        data_out[1,:,5]=lw_crf_weighted_mean/2
        #求sfc sw crf
        #rsds-rsus-rsdscs+rsuscs
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsus/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsus=xr.open_dataset(cas_path)['rsus'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        rsus2=xr.open_dataset(cas_path)['rsus'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsds/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsds=xr.open_dataset(cas_path)['rsds'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
        rsds2=xr.open_dataset(cas_path)['rsds'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] 
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsdscs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsdscs=xr.open_dataset(cas_path)['rsdscs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        rsdscs2=xr.open_dataset(cas_path)['rsdscs'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rsuscs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rsuscs=xr.open_dataset(cas_path)['rsuscs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
        rsuscs2=xr.open_dataset(cas_path)['rsuscs'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360]  
        sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
        sfc_sw_crf2=rsds2-rsus2-rsdscs2+rsuscs2
        sfc_sw_crf_weighted=sfc_sw_crf.weighted(weights2)
        sfc_sw_crf_weighted2=sfc_sw_crf2.weighted(weights22)
        sfc_sw_crf_weighted_mean=sfc_sw_crf_weighted.mean(('lon','lat'))+sfc_sw_crf_weighted2.mean(('lon','lat'))
        data_out[2,:,5]=sfc_sw_crf_weighted_mean/2
        #求sfc lw crf
        #rlds-rldscs
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rldscs/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rldscs=xr.open_dataset(cas_path)['rldscs'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        rldscs2=xr.open_dataset(cas_path)['rldscs'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/rlds/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        rlds=xr.open_dataset(cas_path)['rlds'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
        rlds2=xr.open_dataset(cas_path)['rlds'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] 
        sfc_lw_crf=rlds-rldscs
        sfc_lw_crf2=rlds2-rldscs2
        sfc_lw_crf_weighted=sfc_lw_crf.weighted(weights2)
        sfc_lw_crf_weighted2=sfc_lw_crf2.weighted(weights22)
        sfc_lw_crf_weighted_mean=sfc_lw_crf_weighted.mean(('lon','lat'))+sfc_lw_crf_weighted2.mean(('lon','lat'))
        data_out[3,:,5]=sfc_lw_crf_weighted_mean/2
        #求clt
        cas_his='/data03/cmip6/post-new/CMIP6/CMIP6/ScenarioMIP/CAS/CAS-ESM2-0/ssp245/r1i1p1f1/Amon/clt/'
        cas_path=cas_his+os.listdir(cas_his)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]+'/'
        cas_path=cas_path+os.listdir(cas_path)[0]
        clt=xr.open_dataset(cas_path)['clt'].loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
        clt2=xr.open_dataset(cas_path)['clt'].loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
        weights=np.cos(np.deg2rad(clt.coords['lat']))
        weightss=np.cos(np.deg2rad(clt2.coords['lat']))
        clt_weighted=clt.weighted(weights)
        clt_weighted2=clt2.weighted(weightss)
        clt_weighted_mean=clt_weighted.mean(('lon','lat'))+clt_weighted2.mean(('lon','lat'))
        #annual_clt=clt_weighted_mean.groupby('time.season').mean()
        data_out[4,:,5]=clt_weighted_mean/2
        for m in range(len(models)):
            if m!=5:
                print(models[m])
                #求swcrf
                fhis=glob.glob(model_his+models[m]+'/rsutcs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsutcs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsutcs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                rsutcs2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rsut_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsut']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsut=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
                rsut2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360]  
                sw_crf=rsutcs-rsut
                sw_crf2=rsutcs2-rsut2
                weights1=np.cos(np.deg2rad(sw_crf.coords['lat']))
                weights2=np.cos(np.deg2rad(sw_crf2.coords['lat']))
                sw_crf_weighted_mean=sw_crf.weighted(weights1).mean(('lon','lat'))+sw_crf2.weighted(weights2).mean(('lon','lat'))
                data_out[0,:,m]=sw_crf_weighted_mean/2
                #求lwcrf
                fhis=glob.glob(model_his+models[m]+'/rlutcs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rlutcs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rlutcs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                rlutcs2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rlut_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rlut']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rlut=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                rlut2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] 
                lw_crf=rlutcs-rlut
                lw_crf2=rlutcs2-rlut2
                # print(lw_crf)
                weights2=np.cos(np.deg2rad(lw_crf.coords['lat']))
                weights22=np.cos(np.deg2rad(lw_crf2.coords['lat']))
                lw_crf_weighted=lw_crf.weighted(weights2)
                lw_crf_weighted2=lw_crf2.weighted(weights22)
                lw_crf_weighted_mean=lw_crf_weighted.mean(('lon','lat'))+lw_crf_weighted2.mean(('lon','lat'))
                #annual_lw_crf=lw_crf_weighted_mean.groupby('time.season').mean()
                data_out[1,:,m]=lw_crf_weighted_mean/2
                #求sfc sw cre
                fhis=glob.glob(model_his+models[m]+'/rsds_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsds']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsds=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
                rsds2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rsus_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsus']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsus=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                rsus2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360]
                fhis=glob.glob(model_his+models[m]+'/rsuscs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsuscs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsuscs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] #240x48x192
                rsuscs2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] 
                fhis=glob.glob(model_his+models[m]+'/rsdscs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rsdscs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rsdscs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
                rsdscs2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] 
                sfc_sw_crf=rsds-rsus-rsdscs+rsuscs
                sfc_sw_crf2=rsds2-rsus2-rsdscs2+rsuscs2
                sfc_sw_crf_weighted=sfc_sw_crf.weighted(weights2)
                sfc_sw_crf_weighted2=sfc_sw_crf2.weighted(weights22)
                sfc_sw_crf_weighted_mean=sfc_sw_crf_weighted.mean(('lon','lat'))+sfc_sw_crf_weighted2.mean(('lon','lat'))
                #annual_lw_crf=lw_crf_weighted_mean.groupby('time.season').mean()
                data_out[2,:,m]=sfc_sw_crf_weighted_mean/2
                #求sfc lw cre
                fhis=glob.glob(model_his+models[m]+'/rlds_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rlds']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rlds=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                rlds2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
                fhis=glob.glob(model_his+models[m]+'/rldscs_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['rldscs']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                rldscs=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360] 
                rldscs2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] 
                sfc_lw_crf=rlds-rldscs
                sfc_lw_crf2=rlds2-rldscs2
                sfc_lw_crf_weighted=sfc_lw_crf.weighted(weights2)
                sfc_lw_crf_weighted2=sfc_lw_crf2.weighted(weights22)
                sfc_lw_crf_weighted_mean=sfc_lw_crf_weighted.mean(('lon','lat'))+sfc_lw_crf_weighted2.mean(('lon','lat'))
                #annual_lw_crf=lw_crf_weighted_mean.groupby('time.season').mean()
                data_out[3,:,m]=sfc_lw_crf_weighted_mean/2
                #求clt
                fhis=glob.glob(model_his+models[m]+'/clt_Amon_'+models[m]+'_ssp245_r1i1p1f1'+'*201501-210012.nc')[0]
                fhis_data=xr.open_dataset(fhis)['clt']
                if len(fhis_data['time'])==1032:
                    fhis_data['time']=pd.date_range('20150101','21001231',freq='M')
                # if m==7 or m==9:
                #     # print('CIESM')
                #     clt=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]*100 
                #     clt2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360]*100 #240x48x192
                # else:
                clt=fhis_data.loc['2015-01-01':'2099-12-31',int(area_my[0]):int(area_my[1]),0:360]
                clt2=fhis_data.loc['2015-01-01':'2099-12-31',-int(area_my[1]):-int(area_my[0]),0:360] #240x48x192
                weights=np.cos(np.deg2rad(clt.coords['lat']))
                weightss=np.cos(np.deg2rad(clt2.coords['lat']))
                clt_weighted=clt.weighted(weights)
                clt_weighted2=clt2.weighted(weightss)
                clt_weighted_mean=clt_weighted.mean(('lon','lat'))+clt_weighted2.mean(('lon','lat'))
                #annual_clt=clt_weighted_mean.groupby('time.season').mean()
                data_out[4,:,m]=clt_weighted_mean/2
    return data_out


final_out2=np.zeros((6,1020,len(models)))
final_out2[:,:,:]=cal_my_ssp245(0)
da = os.path.exists('fig7_2.npy')
if da:
    os.remove('fig7_2.npy')
np.save('fig7_2.npy',final_out2)

print(final_out2.shape,'file save')