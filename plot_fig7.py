#画出好模式与坏模式平均的年时间序列
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
data_out1=np.load('fig7_1.npy')#5areax5varx1980timex24models历史实验
data_out2=np.load('fig7_2.npy')#ssp245实验
data_out3=np.load('fig7_3.npy')#5areax5varx1020timex24models
# models=['ACCESS-CM2','BCC-CSM2-MR','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3','CAS-ESM2-0']
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']

print(len(models))
area=['-90:90','-10:10','10:30','30:60','60:90'] 
# wmodels=np.array([['FGOALS-g3', 'MRI-ESM2-0', 'ACCESS-ESM1-5'],['CAS-ESM2-0', 'KIOST-ESM', 'FGOALS-g3'],['INM-CM4-8', 'KIOST-ESM', 'CAS-ESM2-0'],['FGOALS-g3', 'IPSL-CM6A-LR', 'INM-CM4-8'],['ACCESS-CM2', 'CESM2-WACCM' ,'CAS-ESM2-0']])
# gmodels=np.array([['CMCC-CM2-SR5', 'CESM2-WACCM' ,'ACCESS-CM2'],['CESM2-WACCM', 'GFDL-ESM4', 'ACCESS-ESM1-5'],[ 'MPI-ESM1-2-HR', 'KACE-1-0-G', 'ACCESS-CM2'],[  'GFDL-ESM4', 'MPI-ESM1-2-LR', 'MPI-ESM1-2-HR'],['MPI-ESM1-2-HR', 'MIROC6', 'MPI-ESM1-2-LR']])
wmodels=np.array([['FGOALS-g3', 'INM-CM4-8', 'NESM3'],['FGOALS-g3', 'INM-CM4-8', 'NESM3'],['INM-CM4-8', 'IPSL-CM6A-LR', 'CAS-ESM2-0'],['INM-CM4-8', 'IPSL-CM6A-LR' ,'CAS-ESM2-0'],['ACCESS-CM2', 'CESM2-WACCM' ,'CAS-ESM2-0']])
gmodels=np.array([[ 'CESM2-WACCM', 'CMCC-CM2-SR5', 'ACCESS-CM2'],[ 'CESM2-WACCM', 'CMCC-CM2-SR5', 'ACCESS-CM2'],[ 'MPI-ESM1-2-HR' ,'CESM2-WACCM' ,'GFDL-ESM4'],[ 'MPI-ESM1-2-HR', 'CESM2-WACCM', 'GFDL-ESM4'],['MPI-ESM1-2-HR', 'MIROC6', 'MPI-ESM1-2-LR']])


data_out=np.concatenate((data_out1,data_out2),axis = 2)
data_outt=np.concatenate((data_out1,data_out3),axis = 2)
# print(data_out[0,4,750:780,:])
# print(data_outt[3,4,65:70,:])
print(data_out.shape)
wm=np.zeros([5,3])
bm=np.zeros([5,3])
for i in range(5):
    for j in range(3):
        wm[i,j]=models.index(wmodels[i,j])
        bm[i,j]=models.index(gmodels[i,j])
gwmodels=np.hstack((bm,wm))
gwmodels=gwmodels.astype(int)
print(gwmodels)
# gwmodels=np.array([[18,16,7,23,3,22],[18,16,7,23,3,22],[18,16,7,3,23,20],[18,16,7,3,23,20],[12,3,15,22,17,0]])
# wmodels=[[23,3,22],[3,23,20],[22,17,0]]
# data1=np.zeros([5,5,3000,6])#5areax5varx1260timax3model
# data2=np.zeros([5,5,3000,6])#5areax5varx1260timax3model
# for a in range(5):
#     for v in range(5):#对于5个变量
#         for num in range(6):
#             temp=gwmodels[v,num]
#             data1[a,v,:,num]=data_out[a,v,:,temp]
#             data2[a,v,:,num]=data_outt[a,v,:,temp]
areanum=np.arange(5)
varnum=np.arange(5)
time=pd.date_range('18500101','20991231',freq='M')
gwnum=np.arange(6)
modelnum=np.arange(23)
# data1xr=xr.DataArray(data1, coords=[areanum,varnum, time,gwnum], dims=['areanum','varnum', 'time','gwnum'])#ssp245
data2xr=xr.DataArray(data_out[:,:,:,:], coords=[areanum,varnum, time,modelnum], dims=['areanum','varnum', 'time','modelnum'])
# data11xr=xr.DataArray(data2, coords=[areanum,varnum, time,gwnum], dims=['areanum','varnum', 'time','gwnum'])#ssp585
data22xr=xr.DataArray(data_outt[:,:,:,:], coords=[areanum,varnum, time,modelnum], dims=['areanum','varnum', 'time','modelnum'])

# datay1=data1xr.loc[:,:,'1995-01-01':'2099-12-31',:].groupby('time.year').mean().values#变成年平均
datay2=data2xr.loc[:,:,'2001-01-01':'2099-12-31',:].groupby('time.year').mean().values#变成年平均
# datay11=data11xr.loc[:,:,'1995-01-01':'2099-12-31',:].groupby('time.year').mean().values#变成年平均
datay22=data22xr.loc[:,:,'2001-01-01':'2099-12-31',:].groupby('time.year').mean().values#变成年平均
# print(datay2[0,4,65:70,:])
print(datay2.shape)
dataA=np.zeros([5,5,99,20])#装取anomaly150年 99年
dataA2=np.zeros([5,5,99,20])#装取anomaly
for a in range(5):
    for v in range(5):#对于5个变量
        s=0
        for num in range(23):
            if num==10  or num==2 or num==7 :##去掉'E3SM-1-0'  9，'FGOALS-f3-L'  10，CIESM  7' AWI-CM-1-1-MR'2
                print('AWI')#AWI的ssp585的sfc突然下坠，'FGOALS-f3-L'的ssp245的clt在2060有超大值.CIESM的ssp245的clt有一段突然下落
            else:
                dataA[a,v,:,s]=datay2[a,v,:,num]-np.mean(datay2[a,v,0:14,num],0)
                dataA2[a,v,:,s]=datay22[a,v,:,num]-np.mean(datay22[a,v,0:14,num],0)
                s=s+1
# obs[:,:,:]=data
# print(dataA[4,:,:,:])
# datay=np.zeros([5,5,105,6])
# datay2=np.zeros([5,5,105,6])
# for a in range(5):
#     for v in range(5):#对于5个变量
#         for num in range(6):
#             datay[a,v,:,num]=datay1[a,v,:,num]-np.mean(datay1[a,v,0:20,num],0)
#             datay2[a,v,:,num]=datay11[a,v,:,num]-np.mean(datay11[a,v,0:20,num],0)
datay=np.zeros([5,5,99,6])#5areax5varx1260timax3model
datay2=np.zeros([5,5,99,6])#5areax5varx1260timax3model
for a in range(5):
    for v in range(5):#对于5个变量
        for num in range(6):
            temp=gwmodels[v,num]
            print(temp)
            datay[a,v,:,num]=dataA[a,v,:,temp]
            datay2[a,v,:,num]=dataA2[a,v,:,temp]

#draw
# print(datap[4,:,0].shape)

# print(datap[0,0,:,:]+datap[0,1,:,:])
def draw1(ax,datap,datap2,label,num):
    ax.set_xlim(2001,2100)
    a=np.mean(datap[:,0:3],1)
    b=np.max(datap[:,0:3],1)
    c=np.min(datap[:,0:3],1)
    a2=np.mean(datap[:,3:6],1)
    b2=np.max(datap[:,3:6],1)
    c2=np.min(datap[:,3:6],1)
    ax.plot(x,a,'r-',label='BMME')
    ax.fill_between(x,c,b,alpha=0.2,color='r')
    ax.plot(x,a2,'b-',label='WMME')
    ax.fill_between(x,c2,b2,alpha=0.2,color='b')
    ax.plot(x,np.mean(datap2,1),'g-',label='AMME')
    # ax.fill_between(x,datap[:,7],datap[:,6],alpha=0.2,color='g')
    ax.plot(x,[0]*105,color='gray',linestyle='--')
    ax.set_title(label,loc='left')
    ax.legend()

# def draw2(ax,datap,datap2,label,num):
#     ax.set_xlim(1995,2100)
#     ax.plot(x,datap[:,8],'b-',label='ssp245 AMME',linewidth=1.5)
#     ax.fill_between(x,datap[:,6],datap[:,7],alpha=0.2,color='b')
#     ax.plot(x,datap[:,2],'b-.',label='ssp245 BMME',linewidth=1.5)
#     ax.plot(x,datap[:,5],'b--',label='ssp245 WMME',linewidth=1.5)
    
#     ax.fill_between(x,datap[:,7],datap[:,6],alpha=0.2,color='g')
#     ax.plot(x,[0]*105,color='gray',linestyle='--')

#     # ax.plot(x,datapsw[:,2],'r--',linewidth=0.9)
#     # # ax.fill_between(x,datapsw[:,1],datapsw[:,0],alpha=0.2,color='r')
#     # ax.plot(x,datapsw[:,5],'b--',linewidth=0.9)
#     # # ax.fill_between(x,datapsw[:,4],datapsw[:,3],alpha=0.2,color='b')
#     # ax.plot(x,datapsw[:,8],'g--',linewidth=0.9)

#     # ax.plot(x,dataplw[:,2],'r-.',linewidth=0.9)
#     # # ax.fill_between(x,dataplw[:,1],dataplw[:,0],alpha=0.2,color='r')
#     # ax.plot(x,dataplw[:,5],'b-.',linewidth=0.9)
#     # # ax.fill_between(x,dataplw[:,4],dataplw[:,3],alpha=0.2,color='b')
#     # ax.plot(x,dataplw[:,8],'g-.',linewidth=0.9)
#     ax.set_title(label,loc='left')
#     # if num==3:
#     ax.legend(loc=3)
x=np.arange(2001,2100,1)
x1=np.arange(2001,2015,1)
x2=np.arange(2014,2100,1)
# x3=np.arange(2001,2015,1)
##读取ceres的200101-201412数据
obs=np.zeros([5,14])
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
obs2=np.zeros([5,14])
for i in range(14):
    obs2[:,i]=obs[:,i]-np.mean(obs,1)
# obs=obs2
def draw3(ax,datap,dataAp,datap2,dataAp2,obsp,label,num):
    ax.set_xlim(2001,2100)
    a=np.mean(datap[:,0:3],1)
    a2=np.mean(datap[:,3:6],1)

    ax.plot(x2,np.mean(dataAp,1)[13:99],color='blue',linestyle='dotted',label='ssp245 AMME',linewidth=1.5)
    ax.fill_between(x2,np.min(dataAp,1)[13:99],np.max(dataAp,1)[13:99],alpha=0.2,color='b')
    ax.plot(x2,a[13:99],'b-',label='ssp245 BMME',linewidth=1.5)
    ax.plot(x2,a2[13:99],'b--',label='ssp245 WMME',linewidth=1.5)
    
    # ax.fill_between(x,datap[:,7],datap[:,6],alpha=0.2,color='g')
    ax.plot(x,[0]*99,color='gray',linestyle='--')
    a=np.mean(datap2[:,0:3],1)
    a2=np.mean(datap2[:,3:6],1)
    ax.plot(x2,np.mean(dataAp2,1)[13:99],color='red',linestyle='dotted',label='ssp585 AMME',linewidth=1.5)
    ax.fill_between(x2,np.min(dataAp2,1)[13:99],np.max(dataAp2,1)[13:99],alpha=0.2,color='r')
    ax.plot(x2,a[13:99],'r-',label='ssp585 BMME',linewidth=1.5)
    ax.plot(x2,a2[13:99],'r--',label='ssp585 WMME',linewidth=1.5)
    # ax.plot(x,datapsw[:,2],'r--',linewidth=0.9)
    # # ax.fill_between(x,datapsw[:,1],datapsw[:,0],alpha=0.2,color='r')
    # ax.plot(x,datapsw[:,5],'b--',linewidth=0.9)
    # # ax.fill_between(x,datapsw[:,4],datapsw[:,3],alpha=0.2,color='b')
    # ax.plot(x,datapsw[:,8],'g--',linewidth=0.9)

    # ax.plot(x,dataplw[:,2],'r-.',linewidth=0.9)
    # # ax.fill_between(x,dataplw[:,1],dataplw[:,0],alpha=0.2,color='r')
    # ax.plot(x,dataplw[:,5],'b-.',linewidth=0.9)
    # # ax.fill_between(x,dataplw[:,4],dataplw[:,3],alpha=0.2,color='b')
    # ax.plot(x,dataplw[:,8],'g-.',linewidth=0.9)

    ax.plot(x1,np.mean(dataAp,1)[0:14],color='k',linestyle='dotted',label='historical AMME',linewidth=1.5)
    ax.fill_between(x1,np.min(dataAp,1)[0:14],np.max(dataAp,1)[0:14],alpha=0.2,color='k')
    ax.plot(x1,a[0:14],'k-',label='historical BMME',linewidth=1.5)
    ax.plot(x1,a2[0:14],'k--',label='historical WMME',linewidth=1.5)
    ax.plot(x1,obsp,'y',label='OBS',linewidth=1.5)
    ax.set_title(label,loc='left',fontsize=14)
    # if num==3:
    # if num==1:
    #     ax.plot(x3,obs[0,:]+obs[1,:],'g-',label='obs')
    # elif num==2:
    #     ax.plot(x3,obs[2,:]+obs[3,:],'g-',label='obs')
    # else:
    #     ax.plot(x3,obs[4,:],'g-',label='obs')
    ax.tick_params(axis='x',labelsize=14)
    ax.tick_params(axis='y',labelsize=14)
    ax.set_xticks(np.arange(2001,2100,20))
    ax.legend(fontsize=10,bbox_to_anchor=(1,1))

def draw_all(ax,data1,data2,num):
    s=np.array([0,13,5,8,15,18])
    for i in s:
        # ax.plot(x,data1[:,i],color=colors[i],linestyle='-',label=models[i])
        ax.plot(x,data2[:,i],color=colors[i],linestyle='--',label=models[i])
        if num==3:
            ax.legend()

fig,ax=plt.subplots(3,1,figsize=(12,15),dpi=300)
colors=plt.cm.nipy_spectral(np.linspace(0,1,20))
# draw_all(ax[0],dataA[0,0,:,:]+dataA[0,1,:,:],dataA2[0,0,:,:]+dataA2[0,1,:,:],1)
# draw_all(ax[1],dataA[0,2,:,:]+dataA[0,3,:,:],dataA2[0,2,:,:]+dataA2[0,3,:,:],2)
# draw_all(ax[2],dataA[0,4,:,:],dataA2[0,4,:,:],3)

# draw1(ax[0],datay2[0,0,:,:]+datay2[0,1,:,:],dataA2[0,0,:,:]+dataA2[0,1,:,:],'a) Toa crf',1)
# draw1(ax[1],datay2[0,2,:,:]+datay2[0,3,:,:],dataA2[0,2,:,:]+dataA2[0,3,:,:],'b) Sfc crf',2)
# draw1(ax[2],datay2[0,4,:,:],dataA2[0,4,:,:],'c) Tcf',3)
draw3(ax[0],datay[0,0,:,:]+datay[0,1,:,:],dataA[0,0,:,:]+dataA[0,1,:,:],datay2[0,0,:,:]+datay2[0,1,:,:],dataA2[0,0,:,:]+dataA2[0,1,:,:],obs2[0,:]+obs2[1,:],'a) Toa net crf',1)
draw3(ax[1],datay[0,2,:,:]+datay[0,3,:,:],dataA[0,2,:,:]+dataA[0,3,:,:],datay2[0,2,:,:]+datay2[0,3,:,:],dataA2[0,2,:,:]+dataA2[0,3,:,:],obs2[2,:]+obs2[3,:],'b) sfc net crf',2)
draw3(ax[2],datay[0,4,:,:],dataA[0,4,:,:],datay2[0,4,:,:],dataA2[0,4,:,:],obs2[4,:],'c) CLT',3)
plt.savefig('fig7',bbox_inches='tight')

fig,ax=plt.subplots(4,3,figsize=(25,15),dpi=300)
arealabel=['Tropic','SubTropic','Midlatitude','Highlatitude']
s=0
for a in range(4):
    draw3(ax[a][0],datay[a+1,0,:,:]+datay[a+1,1,:,:],dataA[a+1,0,:,:]+dataA[a+1,1,:,:],datay2[a+1,0,:,:]+datay2[a+1,1,:,:],dataA2[a+1,0,:,:]+dataA2[a+1,1,:,:],obs2[0,:]+obs2[1,:],arealabel[a]+' Toa net crf',s+1)
    draw3(ax[a][1],datay[a+1,2,:,:]+datay[a+1,3,:,:],dataA[a+1,2,:,:]+dataA[a+1,3,:,:],datay2[a+1,2,:,:]+datay2[a+1,3,:,:],dataA2[a+1,2,:,:]+dataA2[a+1,3,:,:],obs2[2,:]+obs2[3,:],arealabel[a]+' Sfc net crf',s+2)
    draw3(ax[a][2],datay[a+1,4,:,:],dataA[a+1,4,:,:],datay2[a+1,4,:,:],dataA2[a+1,4,:,:],obs2[4,:],arealabel[a]+' CLT',s+3)
    s=s+3
plt.savefig('fig7.area.png',bbox_inches='tight')
