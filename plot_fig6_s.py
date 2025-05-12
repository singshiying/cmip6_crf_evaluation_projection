#取出好模式与坏模式的5个区域(area=['-90:90','-10:10','10:30','30:60','60:90'] )的平均画图
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
import re

data_out=np.load('fig3_s2.npy')[:,:,:,0:20]#(5,180,360,len(models)+1)
data_out2=np.load('fig3_s2.npy')
print(data_out.shape)
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)
# models=['ACCESS-CM2','ACCESS-ESM1-5','AWI-CM-1-1-MR','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CIESM','CMCC-CM2-SR5','E3SM-1-0','EC-Earth3-CC','FGOALS-f3-L','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']
# wmodels=np.array([['FGOALS-g3','CIESM','ACCESS-ESM1-5'],['CAS-ESM2-0','NESM3','FGOALS-g3'],['INM-CM4-8','INM-CM5-0','ACCESS-ESM1-5'],['FGOALS-g3','CIESM','INM-CM4-8'],['KACE-1-0-G','ACCESS-ESM1-5','ACCESS-CM2']])
# bmodels=np.array([['EC-Earth3-CC','CMCC-CM2-SR5','E3SM-1-0'],['CMCC-CM2-SR5','IPSL-CM6A-LR','MRI-ESM2-0'],['CESM2-WACCM','CMCC-CM2-SR5','MRI-ESM2-0'],['MPI-ESM1-2-HR','BCC-CSM2-MR','AWI-CM-1-1-MR'],[ 'MRI-ESM2-0','EC-Earth3-CC','MIROC6']])
wmodels1=np.array([['FGOALS-g3', 'MRI-ESM2-0', 'ACCESS-ESM1-5'],['CAS-ESM2-0', 'KIOST-ESM', 'FGOALS-g3'],['INM-CM4-8', 'KIOST-ESM', 'CAS-ESM2-0'],['FGOALS-g3', 'IPSL-CM6A-LR', 'INM-CM4-8'],['ACCESS-CM2', 'CESM2-WACCM' ,'CAS-ESM2-0']])
bmodels1=np.array([['CMCC-CM2-SR5', 'CESM2-WACCM' ,'ACCESS-CM2'],['CESM2-WACCM', 'GFDL-ESM4', 'ACCESS-ESM1-5'],[ 'MPI-ESM1-2-HR', 'KACE-1-0-G', 'ACCESS-CM2'],[  'GFDL-ESM4', 'MPI-ESM1-2-LR', 'MPI-ESM1-2-HR'],['MPI-ESM1-2-HR', 'MIROC6', 'MPI-ESM1-2-LR']])

wmodels2=np.array([['FGOALS-g3', 'INM-CM4-8', 'NESM3'],['FGOALS-g3', 'INM-CM4-8', 'NESM3'],['INM-CM4-8', 'IPSL-CM6A-LR', 'CAS-ESM2-0'],['INM-CM4-8', 'IPSL-CM6A-LR' ,'CAS-ESM2-0'],['ACCESS-CM2', 'CESM2-WACCM' ,'CAS-ESM2-0']])
bmodels2=np.array([[ 'CESM2-WACCM', 'CMCC-CM2-SR5', 'ACCESS-CM2'],[ 'CESM2-WACCM', 'CMCC-CM2-SR5', 'ACCESS-CM2'],[ 'MPI-ESM1-2-HR' ,'CESM2-WACCM' ,'GFDL-ESM4'],[ 'MPI-ESM1-2-HR', 'CESM2-WACCM', 'GFDL-ESM4'],['MPI-ESM1-2-HR', 'MIROC6', 'MPI-ESM1-2-LR']])

def my_data(wmodels,bmodels):
    wm_temp=np.zeros([5,3])
    bm_temp=np.zeros([5,3])
    wmdata=np.zeros([5,3,180,360])
    bmdata=np.zeros([5,3,180,360])
    for i in range(5):
        for j in range(3):
            wm_temp[i,j]=models.index(wmodels[i,j])
            bm_temp[i,j]=models.index(bmodels[i,j])
            wmdata[i,j,:,:]=np.mean(data_out[i,:,:,:].take(wm_temp[i,:].astype(int),axis=2),2)-data_out2[i,:,:,20]
            bmdata[i,j,:,:]=np.mean(data_out[i,:,:,:].take(bm_temp[i,:].astype(int),axis=2),2)-data_out2[i,:,:,20]
    print(data_out[4,20,:,7])
    # print(data_out2[4,20,:,20])
    data_outt=np.zeros([5,180,360,20])
    for i in range(5):
        for j in range(20):
            data_outt[i,:,:,j]=data_out[i,:,:,j]-data_out2[i,:,:,20]

    #对好坏模式以及所有模式进行区域平均
    area=['-90:90','-10:10','10:30','30:60','60:90']
    varnum=np.arange(0,5)
    bwnum=np.arange(3)
    modelnum=np.arange(0,20)
    olat=np.arange(-89.5,90,1)
    olon=np.arange(0.5,360,1)
    allm = xr.DataArray(data_outt, coords=[varnum,olat,olon,modelnum], dims=['varnum','lat','lon','modelnum'])
    wm = xr.DataArray(wmdata, coords=[varnum,bwnum,olat,olon], dims=['varnum','bwnum','lat','lon'])
    bm = xr.DataArray(bmdata, coords=[varnum,bwnum,olat,olon], dims=['varnum','bwnum','lat','lon'])
    datap=np.zeros([5,5,3,3])#5areax5varxgood,worse,ammexmax,min,mean
    for a in range(5):
        if a==0 or a==1:
            pattern=re.compile(r'\-?\d+')
            area_my=re.findall(pattern,area[a])
            print(int(area_my[0]),int(area_my[1]))
            allma=allm.loc[:,int(area_my[0]):int(area_my[1]),:]
            wma=wm.loc[:,:,int(area_my[0]):int(area_my[1]),:]
            bma=bm.loc[:,:,int(area_my[0]):int(area_my[1]),:]

            weights=np.cos(np.deg2rad(allma.coords['lat']))
            allma_weighted=allma.weighted(weights).mean(('lon','lat')).values
            allma_weighted[0,:]=allma.mean(('lon','lat')).values[0,:]
            wma_weighted=wma.weighted(weights).mean(('lon','lat')).values
            wma_weighted[0,:]=wma.mean(('lon','lat')).values[0,:]
            bma_weighted=bma.weighted(weights).mean(('lon','lat')).values
            bma_weighted[0,:]=bma.mean(('lon','lat')).values[0,:]
            print(allma_weighted[4,:])
            # print(np.max(bma_weighted,1))
            datap[a,:,0,0]=np.max(bma_weighted,1)
            datap[a,:,0,1]=np.min(bma_weighted,1)
            datap[a,:,0,2]=np.mean(bma_weighted,1)
            datap[a,:,1,0]=np.max(wma_weighted,1)
            datap[a,:,1,1]=np.min(wma_weighted,1)
            datap[a,:,1,2]=np.mean(wma_weighted,1)
            datap[a,:,2,0]=np.max(allma_weighted,1)
            datap[a,:,2,1]=np.min(allma_weighted,1)
            datap[a,:,2,2]=np.mean(allma_weighted,1)
        else:
            pattern=re.compile(r'\-?\d+')
            area_my=re.findall(pattern,area[a])
            allma1=allm.loc[:,int(area_my[0]):int(area_my[1]),:]
            allma2=allm.loc[:,-int(area_my[1]):-int(area_my[0]),:]
            wma1=wm.loc[:,:,int(area_my[0]):int(area_my[1]),:]
            wma2=wm.loc[:,:,-int(area_my[1]):-int(area_my[0]),:]
            bma1=bm.loc[:,:,int(area_my[0]):int(area_my[1]),:]
            bma2=bm.loc[:,:,-int(area_my[1]):-int(area_my[0]),:]
            weights1=np.cos(np.deg2rad(allma1.coords['lat']))
            weights2=np.cos(np.deg2rad(allma2.coords['lat']))
            allma_weighted1=allma1.weighted(weights1).mean(('lon','lat')).values
            allma_weighted1[0,:]=allma1.mean(('lon','lat')).values[0,:]
            wma_weighted1=wma1.weighted(weights1).mean(('lon','lat')).values
            wma_weighted1[0,:]=wma1.mean(('lon','lat')).values[0,:]
            bma_weighted1=bma1.weighted(weights1).mean(('lon','lat')).values
            bma_weighted1[0,:]=bma1.mean(('lon','lat')).values[0,:]
            allma_weighted2=allma2.weighted(weights2).mean(('lon','lat')).values
            allma_weighted2[0,:]=allma2.mean(('lon','lat')).values[0,:]
            wma_weighted2=wma2.weighted(weights2).mean(('lon','lat')).values
            wma_weighted2[0,:]=wma2.mean(('lon','lat')).values[0,:]
            bma_weighted2=bma2.weighted(weights2).mean(('lon','lat')).values
            bma_weighted2[0,:]=bma2.mean(('lon','lat')).values[0,:]
            allma_weighted=(allma_weighted1+allma_weighted2)/2
            wma_weighted=(wma_weighted1+wma_weighted2)/2
            bma_weighted=(bma_weighted1+bma_weighted2)/2
            # print(bma_weighted.shape)
            datap[a,:,0,0]=np.max(bma_weighted,1)
            datap[a,:,0,1]=np.min(bma_weighted,1)
            datap[a,:,0,2]=np.mean(bma_weighted,1)
            datap[a,:,1,0]=np.max(wma_weighted,1)
            datap[a,:,1,1]=np.min(wma_weighted,1)
            datap[a,:,1,2]=np.mean(wma_weighted,1)
            datap[a,:,2,0]=np.max(allma_weighted,1)
            datap[a,:,2,1]=np.min(allma_weighted,1)
            datap[a,:,2,2]=np.mean(allma_weighted,1)
    return datap
# print(datap[:,4,2,:])
#全部减去obsp
# data_out2=np.load('cal_fig3.npy')#5areax5varx168timex25model+obs
# obsp=np.mean(data_out2[:,:,:,24],2)#5areax5var
datapf=my_data(wmodels1,bmodels1)#5areax5varxgood,worse,ammexmax,min,mean
datapf2=my_data(wmodels2,bmodels2)

#draw
def hat_graph1(ax, xlabels, values, group_labels,colors):
    """
    Create a hat graph.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to plot into.
    xlabels : list of str
        The category names to be displayed on the x-axis.
    values : (M, N) array-like
        The data values.
        Rows are the groups (len(group_labels) == M).
        Columns are the categories (len(xlabels) == N).
    group_labels : list of str
        The group labels displayed in the legend.
    """

    # def label_bars(heights, rects):
    #     """Attach a text label on top of each bar."""
    #     for height, rect in zip(heights, rects):
    #         ax.annotate(f'{height}',
    #                     xy=(rect.get_x() + rect.get_width() / 2, height),
    #                     xytext=(0, 4),  # 4 points vertical offset.
    #                     textcoords='offset points',
    #                     ha='center', va='bottom')

    values = np.asarray(values)
    x = np.arange(5)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels)
    spacing = 0.3  # spacing between hat groups
    width = (1 - spacing) / values.shape[1]#3
    style = {'fill': True,'edgecolor': 'black'} 
    rects1 = ax.bar(x-width, values[:,1,0] - values[:,1,1],width, bottom=values[:,1,1], label=group_labels[0],color=colors[0], **style)
    rects2 = ax.bar(x, values[:,2,0] - values[:,2,1],width, bottom=values[:,2,1], label=group_labels[1],color=colors[1], **style)
    rects3 = ax.bar(x+width, values[:,0,0] - values[:,0,1],width, bottom=values[:,0,1], label=group_labels[2],color=colors[2], **style)
    for i in range(5):
        lines1 = ax.plot(np.linspace(i-3*width/2,i-width/2,50),[values[i,1,2]]*50,'k-')
        lines2 = ax.plot(np.linspace(i-width/2,i+width/2,50),[values[i,2,2]]*50,'k-')
        lines3 = ax.plot(np.linspace(i+width/2,i+3*width/2,50),[values[i,0,2]]*50,'k-')
    ax.set_ylim(-40,40)
    ax.set_xlim(-0.5,4.5)
    ax.plot(np.linspace(-0.5,4.5,100),[0]*100,color='grey',linestyle='-.',alpha=0.8)
    ax.legend(loc=2,bbox_to_anchor=(1.05,1))


def hat_graph3(ax, xlabels, valuessw,valueslw,values):
    """
    Create a hat graph.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to plot into.
    xlabels : list of str
        The category names to be displayed on the x-axis.
    values : (M, N) array-like
        The data values.
        Rows are the groups (len(group_labels) == M).
        Columns are the categories (len(xlabels) == N).
    group_labels : list of str
        The group labels displayed in the legend.
    """

    # def label_bars(heights, rects):
    #     """Attach a text label on top of each bar."""
    #     for height, rect in zip(heights, rects):
    #         ax.annotate(f'{height}',
    #                     xy=(rect.get_x() + rect.get_width() / 2, height),
    #                     xytext=(0, 4),  # 4 points vertical offset.
    #                     textcoords='offset points',
    #                     ha='center', va='bottom')
    colorslw=['red','lightcoral','mistyrose']
    colorssw=['dodgerblue','lightblue','aliceblue']
    colorsnet=['darkorange','peachpuff','oldlace']
    group_labelssw=['sw WMME','sw AMME','sw BMME']
    group_labelslw=['lw WMME','lw AMME','lw BMME']
    group_labelsnet=['net WMME','net AMME','net BMME']
    values = np.asarray(values)
    x = np.arange(5)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels)
    spacing = 0.3  # spacing between hat groups
    width = ((1 - spacing) / values.shape[1])/3#3
    style = {'fill': True,'edgecolor': 'black'} 
    rects1 = ax.bar(x-4*width, valuessw[:,1,0] - valuessw[:,1,1],width, bottom=valuessw[:,1,1], label=group_labelssw[0],color=colorssw[0], **style)
    rects2 = ax.bar(x-3*width, valuessw[:,2,0] - valuessw[:,2,1],width, bottom=valuessw[:,2,1], label=group_labelssw[1],color=colorssw[1], **style)
    rects3 = ax.bar(x-2*width, valuessw[:,0,0] - valuessw[:,0,1],width, bottom=valuessw[:,0,1], label=group_labelssw[2],color=colorssw[2], **style)

    rects1 = ax.bar(x-width, valueslw[:,1,0] - valueslw[:,1,1],width, bottom=valueslw[:,1,1], label=group_labelslw[0],color=colorslw[0], **style)
    rects2 = ax.bar(x, valueslw[:,2,0] - valueslw[:,2,1],width, bottom=valueslw[:,2,1], label=group_labelslw[1],color=colorslw[1], **style)
    rects3 = ax.bar(x+width, valueslw[:,0,0] - valueslw[:,0,1],width, bottom=valueslw[:,0,1], label=group_labelslw[2],color=colorslw[2], **style)

    rects1 = ax.bar(x+2*width, values[:,1,0] - values[:,1,1],width, bottom=values[:,1,1], label=group_labelsnet[0],color=colorsnet[0], **style)
    rects2 = ax.bar(x+3*width, values[:,2,0] - values[:,2,1],width, bottom=values[:,2,1], label=group_labelsnet[1],color=colorsnet[1], **style)
    rects3 = ax.bar(x+4*width, values[:,0,0] - values[:,0,1],width, bottom=values[:,0,1], label=group_labelsnet[2],color=colorsnet[2], **style)
    for i in range(5):
        lines1 = ax.plot(np.linspace(i-3*width/2-3*width,i-width/2-3*width,50),[valuessw[i,1,2]]*50,'k-')
        lines2 = ax.plot(np.linspace(i-width/2-3*width,i+width/2-3*width,50),[valuessw[i,2,2]]*50,'k-')
        lines3 = ax.plot(np.linspace(i+width/2-3*width,i+3*width/2-3*width,50),[valuessw[i,0,2]]*50,'k-')

        lines1 = ax.plot(np.linspace(i-3*width/2,i-width/2,50),[valueslw[i,1,2]]*50,'k-')
        lines2 = ax.plot(np.linspace(i-width/2,i+width/2,50),[valueslw[i,2,2]]*50,'k-')
        lines3 = ax.plot(np.linspace(i+width/2,i+3*width/2,50),[valueslw[i,0,2]]*50,'k-')

        lines1 = ax.plot(np.linspace(i-3*width/2+3*width,i-width/2+3*width,50),[values[i,1,2]]*50,'k-')
        lines2 = ax.plot(np.linspace(i-width/2+3*width,i+width/2+3*width,50),[values[i,2,2]]*50,'k-')
        lines3 = ax.plot(np.linspace(i+width/2+3*width,i+3*width/2+3*width,50),[values[i,0,2]]*50,'k-')
    ax.set_ylim(-40,40)
    ax.set_xlim(-0.5,4.5)
    ax.plot(np.linspace(-0.5,4.5,100),[0]*100,color='grey',linestyle='-.',alpha=0.8)
    ax.legend(loc=2,bbox_to_anchor=(1.05,1))



xlabels=['Global','Tropic','Subtropic','Midlatitude','Highlatitude']
toa_net=datapf2[:,0,:,:]+datapf2[:,1,:,:]#5varx5areax3good worse ammex3max,min,mean
# print(toa_net[0,:,:,])
sfc_net=datapf2[:,2,:,:]+datapf2[:,3,:,:]
# print(datapf[3,2,:,:])
# print(datapf[3,3,:,:])
fig, ax = plt.subplots(3,1)
fig.set_figheight(10)
fig.set_figwidth(10)
fig.set_dpi(300)
hat_graph3(ax[0], xlabels, datapf[:,0,:,:],datapf[:,1,:,:],toa_net)
ax[0].set_title('a) Toa net crf',loc='left')
hat_graph3(ax[1], xlabels, datapf[:,2,:,:],datapf[:,3,:,:],sfc_net)
ax[1].set_title('b) Sfc net crf',loc='left')
hat_graph1(ax[2], xlabels, datapf[:,4,:,:], ['CLT WMME', 'CLT AMME','CLT BMME'],['forestgreen','palegreen','honeydew'])
ax[2].set_title('c) CLT',loc='left')
# ax[2].legend()
plt.savefig('fig6.png',bbox_inches='tight')
