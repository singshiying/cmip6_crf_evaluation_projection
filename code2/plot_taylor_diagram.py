#画toa sw crf,toa lw crf,toa net crf,sfcX3,clt的taylor图
import os
import numpy as np
import xarray as xr
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist import floating_axes
from mpl_toolkits.axisartist import grid_finder
from matplotlib.font_manager import FontProperties
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()
plt.rcParams['figure.figsize']=(3*2,3*2)

models=['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CAS-ESM2-0','CESM2-WACCM','CMCC-CM2-SR5','EC-Earth3-CC','FGOALS-g3','GFDL-ESM4','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','KACE-1-0-G','KIOST-ESM','MIROC6','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3']#20models
model_his='/data04/shiy/cmip6_his_ssp585/historical/'
data_out=np.load('../fig1.npy').reshape(5,180*360,21,order='A')#5var,180lat,360lon,21models+obs
data_out2=np.zeros((5,180*360,21))
print(len(data_out[4,:,20][np.isnan(data_out[4,:,20])]))#有1076个缺测
print(len(data_out[0,:,20][np.isnan(data_out[0,:,20])]))#有0个缺测
#normlize
for i in range(5):
        for k in range(21):
            data_out2[i,:,k]=(data_out[i,:,k]-np.nanmean(data_out[i,:,20]))/np.nanstd(data_out[i,:,20])

# toa_net=data_out2[0,:,:]+data_out2[1,:,:]
# atm_net=data_out2[0,:,:]+data_out2[1,:,:]-(data_out2[2,:,:]+data_out2[3,:,:])
def set_tayloraxes(fig, location):
    trans = PolarAxes.PolarTransform()
    r1_locs = np.hstack((np.arange(1,10)/10.0,[0.95,0.99]))
    t1_locs = np.arccos(r1_locs)        
    gl1 = grid_finder.FixedLocator(t1_locs)    
    tf1 = grid_finder.DictFormatter(dict(zip(t1_locs, map(str,r1_locs))))
    r2_locs = np.arange(0,2.3,0.25)
    r2_labels = ['0 ', '0.25 ', '0.50 ', '0.75 ', 'REF ', '1.25 ', '1.50 ', '1.75 ','2.0','2.25']
    gl2 = grid_finder.FixedLocator(r2_locs)
    tf2 = grid_finder.DictFormatter(dict(zip(r2_locs, map(str,r2_labels))))
    ghelper = floating_axes.GridHelperCurveLinear(trans,extremes=(0,np.pi/2,0,2.25),
                                                  grid_locator1=gl1,tick_formatter1=tf1,
                                                  grid_locator2=gl2,tick_formatter2=tf2)
    ax = floating_axes.FloatingSubplot(fig, location, grid_helper=ghelper)
    fig.add_subplot(ax)

    ax.axis["top"].set_axis_direction("bottom")  
    ax.axis["top"].toggle(ticklabels=True, label=True)
    ax.axis["top"].major_ticklabels.set_axis_direction("top")
    ax.axis["top"].major_ticklabels.set_fontsize(9*2)
    ax.axis["top"].label.set_axis_direction("top")
    ax.axis["top"].label.set_text("Correlation")
    ax.axis["top"].label.set_fontsize(9*2-2)
    ax.axis["left"].set_axis_direction("bottom") 
    ax.axis["left"].major_ticklabels.set_fontsize(9*2-2)
    ax.axis["left"].label.set_text("Standard deviation")
    ax.axis["left"].label.set_fontsize(9*2-2)
    ax.axis["right"].set_axis_direction("top")   
    ax.axis["right"].toggle(ticklabels=True)
    ax.axis["right"].major_ticklabels.set_axis_direction("left")
    ax.axis["right"].major_ticklabels.set_fontsize(9*2-2)
    ax.axis["bottom"].set_visible(False)         
    ax.grid(True)
    polar_ax = ax.get_aux_axes(trans)   

    rs,ts = np.meshgrid(np.linspace(0,2.25,100),
                            np.linspace(0,np.pi/2,100))
    rms = np.sqrt(1 + rs**2 - 2*rs*np.cos(ts))
    CS = polar_ax.contour(ts, rs,rms,colors='gray',linestyles='--')
    plt.clabel(CS, inline=1, fontsize=9*2)
    t = np.linspace(0,np.pi/2)
    r = np.zeros_like(t) + 1
    polar_ax.plot(t,r,'k--')
    polar_ax.text(np.pi/2+0.032,1.02, " 1.00", size=9*2 ,ha="right", va="top",
                  bbox=dict(boxstyle="square",ec='w',fc='w'))

    return polar_ax

def plot_taylor(axes, refsample, sample,num, *args, **kwargs):
    df=pd.DataFrame({'ref':refsample,'samp':sample})
    std = np.nanstd(sample)
    corr = df.corr().values
    theta = np.arccos(corr[0,1])
    t,r = theta,std
    print(corr[0,1],std)
    d = axes.plot(t,r, *args, **kwargs) 
    
    # if num<24:
    #     t = axes.text(t,r,num+1,fontsize=9,color=kwargs['color'])
    return d


fig = plt.figure(dpi=300)
ax1 = set_tayloraxes(fig, 111)#toa sw crf
for m in np.arange(0,20):
    d1 = plot_taylor(ax1,data_out2[0,:,20],data_out2[0,:,m], m,color='aqua',marker='o',alpha=0.8,markersize=3*2,markeredgewidth=2,label=models[m])
    d2 = plot_taylor(ax1,data_out2[1,:,20],data_out2[1,:,m], m,color='salmon',marker='o',alpha=0.8,markersize=3*2,markeredgewidth=2,label=models[m])
    # d3 = plot_taylor(ax1,toa_net[:,24],toa_net[:,m], m,color='gold',marker='o',alpha=0.8,markersize=2,markeredgewidth=2,label=models[m])
    d4 = plot_taylor(ax1,data_out2[0,:,20]-data_out2[2,:,20],data_out2[0,:,m]-data_out2[2,:,m], m,color='darkblue',marker='o',alpha=0.8,markersize=3*2,markeredgewidth=2,label=models[m])
    d5 = plot_taylor(ax1,data_out2[1,:,20]-data_out2[3,:,20],data_out2[1,:,m]-data_out2[3,:,m], m,color='darkred',marker='o',alpha=0.8,markersize=3*2,markeredgewidth=2,label=models[m])
    # d6 = plot_taylor(ax1,sfc_net[:,24],sfc_net[:,m], m,color='olive',marker='o',alpha=0.8,markersize=2,markeredgewidth=2,label=models[m])
    # d7 = plot_taylor(ax1,data_out2[4,:,20],data_out2[4,:,m], m,color='g',marker='o',alpha=0.8,markersize=3*2,markeredgewidth=2,label=models[m])
d8 = plot_taylor(ax1,data_out2[0,:,20],np.mean(data_out2[0,:,0:20],1), 24,color='aqua',marker='v',markeredgecolor='k',markeredgewidth=2,alpha=0.7,markersize=7*2,zorder=50)
d9 = plot_taylor(ax1,data_out2[1,:,20],np.mean(data_out2[1,:,0:20],1), 24,color='salmon',marker='v',markeredgecolor='k',markeredgewidth=2,alpha=0.7,markersize=7*2,zorder=50)
# d10 = plot_taylor(ax1,toa_net[:,24],np.mean(toa_net[:,0:24],1), 24,color='gold',marker='v',markeredgecolor='k',markeredgewidth=2,alpha=0.7,markersize=10,zorder=10)
d11 = plot_taylor(ax1,data_out2[0,:,20]-data_out2[2,:,20],np.mean(data_out2[0,:,0:20]-data_out2[2,:,0:20],1), 24,color='darkblue',marker='v',markeredgecolor='k',markeredgewidth=2,alpha=0.7,markersize=7*2,zorder=50)
d12 = plot_taylor(ax1,data_out2[1,:,20]-data_out2[3,:,20],np.mean(data_out2[1,:,0:20]-data_out2[3,:,0:20],1), 24,color='darkred',marker='v',markeredgecolor='k',markeredgewidth=2,alpha=0.7,markersize=7*2,zorder=50)
# d13 = plot_taylor(ax1,sfc_net[:,24],np.mean(sfc_net[:,0:24],1), 24,color='olive',marker='v',markeredgecolor='k',markeredgewidth=2,alpha=0.7,markersize=10,zorder=50)
# d14 = plot_taylor(ax1,data_out2[4,:,20],np.mean(data_out2[4,:,0:20],1), 24,color='g',marker='v',markeredgecolor='k',markeredgewidth=2,alpha=0.7,markersize=7*2,zorder=50)

ax1.text(0.85,0.95,'TOA SWCRF',color='aqua',transform=ax1.transAxes,fontsize=9*2)
ax1.text(0.85,0.89,'TOA LWCRF',color='salmon',transform=ax1.transAxes,fontsize=9*2)
ax1.text(0.85,0.83,'ATM SWCRF',color='darkblue',transform=ax1.transAxes,fontsize=9*2)
ax1.text(0.85,0.77,'ATM LWCRF',color='darkred',transform=ax1.transAxes,fontsize=9*2)
# ax1.text(0.85,0.71,'CLT',color='g',transform=ax1.transAxes,fontsize=9*2)

plt.savefig('../fig2/taylor_diagram.svg',bbox_inches='tight')