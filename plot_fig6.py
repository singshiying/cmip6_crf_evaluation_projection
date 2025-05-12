#求不同area mean的toa net sfc net and tcf
#对BMME,WMME,ANNE相对于obs的偏差
import numpy as np
import glob
import os
import re
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
import pandas as pd
data_out=np.load('fig6.npy')#5areax5varx2good worsex3model
# print(data_out[:,2,:,:])
data_out2=np.load('cal_fig3.npy')#5areax5varx168timex25model+obs
print(np.mean(data_out2[0,4,:,0:25],0))
print(data_out2.shape)
obsp=np.mean(data_out2[:,:,:,24],2)#5areax5var
data_out2p=np.zeros([5,5,3])#5areax5varxmax,min,mean
data_out2p[:,:,0]=np.max(np.mean(data_out2[:,:,:,0:24],2),2)#5x5
data_out2p[:,:,1]=np.min(np.mean(data_out2[:,:,:,0:24],2),2)#5x5
data_out2p[:,:,2]=np.mean(np.mean(data_out2[:,:,:,0:24],2),2)#5x5
#data_out2p放置AMME
# print(data_out2p[0,4,:])
#datap放置BMME，WMME，AMME
datap=np.zeros([5,5,3,3])#5areax5varxgood,worse,ammexmax,min,mean
datap[:,:,2,:]=data_out2p
datap[:,:,0:2,0]=np.max(data_out[:,:,:,:],3)
datap[:,:,0:2,1]=np.min(data_out[:,:,:,:],3)
datap[:,:,0:2,2]=np.mean(data_out[:,:,:,:],3)
# print(data_out[0,4,:,:])
# print(obsp[0,4])

#全部减去obsp
datapf=np.zeros([5,5,3,3])#5areax5varxgood,worse,ammexmax,min,mean
for i in range(5):
    for j in range(5):
        datapf[i,j,:,:]=datap[i,j,:,:]-obsp[i,j]

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
toa_net=datapf[:,0,:,:]+datapf[:,1,:,:]#5varx5areax3good worse ammex3max,min,mean
# print(toa_net[0,:,:,])
sfc_net=datapf[:,2,:,:]+datapf[:,3,:,:]
# print(datapf[3,2,:,:])
# print(datapf[3,3,:,:])
fig, ax = plt.subplots(3,1)
fig.set_figheight(10)
fig.set_figwidth(10)
fig.set_dpi(300)
hat_graph3(ax[0], xlabels, datapf[:,0,:,:],datapf[:,1,:,:],toa_net)
ax[0].set_title('a) Toa crf',loc='left')
hat_graph3(ax[1], xlabels, datapf[:,2,:,:],datapf[:,3,:,:],sfc_net)
ax[1].set_title('b) sfc crf',loc='left')
hat_graph1(ax[2], xlabels, datapf[:,4,:,:], ['tcf WMME', 'tcf AMME','tcf BMME'],['forestgreen','palegreen','honeydew'])
ax[2].set_title('c) CLT',loc='left')
# ax[2].legend()
plt.savefig('fig6.png',bbox_inches='tight')

