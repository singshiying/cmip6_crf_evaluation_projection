import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator, FormatStrFormatter,FixedLocator
import mpl_toolkits.axisartist as axisartist
###画热点图，不同模式为横坐标，相关系数，std，rmse为横坐标
models=['ACCESS-CM2','BCC-CSM2-MR','CanESM5','CESM2-WACCM','CIESM','CMCC-CM2-SR5','FGOALS-f3-L','INM-CM4-8','MPI-ESM1-2-LR','MRI-ESM2-0','ACCESS-ESM1-5', 'AWI-CM-1-1-MR', 'E3SM-1-0', 'EC-Earth3-CC', 'FGOALS-g3', 'GFDL-ESM4',  'INM-CM5-0', 'IPSL-CM6A-LR', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC6', 'MPI-ESM1-2-HR', 'NESM3','CAS-ESM2-0','ModelMean']
model_his='/data04/shiy/cmip6_his_ssp585/historical/'
model_ssp585='/data04/shiy/cmip6_his_ssp585/ssp585/'
area=['-90:90','-10-10','10-30','30-60','60-90'] 
data_out=np.load('cal_fig3.npy')#5area,5var,l68timelen,25models+obs
data_out2=np.zeros((5,5,168,25))
toa_net=data_out[:,0,:,:]+data_out[:,1,:,:]
sfc_net=data_out[:,2,:,:]+data_out[:,3,:,:]
toa_net2=np.zeros((5,168,25))
sfc_net2=np.zeros((5,168,25))
#进行标准化
for i in range(5):
    for j in range(5):
        for k in range(25):
            data_out2[i,j,:,k]=(data_out[i,j,:,k]-np.mean(data_out[i,j,:,24]))/np.std(data_out[i,j,:,24])
for i in range(5):
    for j in range(25):
        toa_net2[i,:,j]=(toa_net[i,:,j]-np.mean(toa_net[i,:,24]))/np.std(toa_net[i,:,24])
        sfc_net2[i,:,j]=(sfc_net[i,:,j]-np.mean(sfc_net[i,:,24]))/np.std(sfc_net[i,:,24])
csr_data1=np.zeros([25,15])#24model+model mean,csr3x3varx5area
csr_data2=np.zeros([25,15])
csr_data3=np.zeros([25,15])
#计算cor，std，rmse
def cal_csr(refsample,sample):
    corr = np.corrcoef(refsample, sample)
    theta = np.arccos(corr[0,1])
    std = np.std(refsample)/np.std(sample)
    # print(std)
    #rmse = np.sqrt(1 + std**2 - 2*std*corr[0,1])
    # print(rmse)
    rmse =1/np.sqrt(np.square(np.subtract(refsample,sample)).mean())#这样转换以后都是越大越好
    # print(np.sqrt(np.square(np.subtract(refsample,sample)).mean()))
    return corr[0,1],std,rmse
print(models[11])
# print(data_out2[0,4,:,11])
print(cal_csr(data_out2[0,4,:,24],data_out2[0,4,:,11]))
print(models[23])
# print(data_out2[0,4,:,23])
print(cal_csr(data_out2[0,4,:,24],data_out2[0,4,:,23]))
for i in range(csr_data1.shape[0]):#对于不同模式
    s=0
    e=3
    if i<24:#对于models
        for j in range(5):#对于不同area
            csr_data1[i,s:e]=cal_csr(toa_net2[j,:,24],toa_net2[j,:,i])#area0,toa net
            csr_data2[i,s:e]=cal_csr(sfc_net2[j,:,24],sfc_net2[j,:,i])#area0,sfc net
            csr_data3[i,s:e]=cal_csr(data_out2[j,4,:,24],data_out2[j,4,:,i])#area0,clt
            s=s+3
            e=e+3
    else:#对于model mean
        for j in range(5):#对于不同area
            csr_data1[i,s:e]=cal_csr(toa_net2[j,:,24],np.mean(toa_net2[j,:,0:24],1))#area0,toa net
            csr_data2[i,s:e]=cal_csr(sfc_net2[j,:,24],np.mean(sfc_net2[j,:,0:24],1))#area0,sfc net
            csr_data3[i,s:e]=cal_csr(data_out2[j,4,:,24],np.mean(data_out2[j,4,:,0:24],1))#area0,clt
            s=s+3
            e=e+3

def cal_rank(arr):
    rank=np.zeros(arr.shape[0])
    index=np.argsort(arr)#从小到大排序的索引
    rank[index]=np.arange(1,arr.shape[0]+1)#小的得分低，大的得分高
    return rank

csr_rank1=np.zeros([25,15])
csr_rank2=np.zeros([25,15])
csr_rank3=np.zeros([25,15])
for j in range(csr_data1.shape[1]):
    csr_rank1[:,j]=cal_rank(csr_data1[:,j])
    csr_rank2[:,j]=cal_rank(csr_data2[:,j])
    csr_rank3[:,j]=cal_rank(csr_data3[:,j])
#####依据总分数从小到大排序
index1=np.argsort(np.mean(csr_rank1,1))
models_p1=models
models_p1=np.array(models)[index1]
csr_rank_p1=csr_rank1[index1,:]
index2=np.argsort(np.mean(csr_rank2,1))
models_p2=models
models_p2=np.array(models)[index2]
csr_rank_p2=csr_rank2[index2,:]
index3=np.argsort(np.mean(csr_rank3,1))
models_p3=models
models_p3=np.array(models)[index3]
csr_rank_p3=csr_rank3[index3,:]
####画图
colors=plt.cm.nipy_spectral(np.linspace(0,1,25))
fig = plt.figure(figsize=(25,10))
fig.subplots_adjust(wspace=0.25,hspace=0.05,right=0.9,top=0.8,bottom=0.1)

ax=fig.add_subplot(131)
ax = sns.heatmap(csr_rank_p1, annot=True,fmt='.0f',cmap='RdYlGn',linewidths=0.5,cbar=True)#,linewidths=0.5,line
ax.set_adjustable('box')
ax.set_xticks(np.arange(0,15,1))
ax.set_yticks(np.linspace(0,24,25))
ax.tick_params(axis="both", which="major", direction="in")
ax.tick_params(axis="both", which="minor", direction="in")
ax.xaxis.set_major_locator(FixedLocator(np.arange(0,15,3)))#设置y主坐标间隔 1
ax.xaxis.set_minor_locator(FixedLocator(np.arange(0,15,1)))
ax.yaxis.set_major_locator(FixedLocator(np.linspace(0,24,25)))#设置y主坐标间隔 1
ax.xaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
# ax.xaxis.grid(True,which='minor',color='black',linestyle='--')#major,color='black'
ax.yaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
ax.tick_params(bottom=False,top=False,left=False,right=False)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['top'].set_visible(True)
ax.spines['left'].set_linewidth(1.5)
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['right'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_color('black')
ax.set_yticks(np.arange(0.5,25,1),minor=True)
ax.set_yticklabels(models_p1,minor=True)
ax.tick_params(axis='y',labelrotation=0)
xlabel=['c','s','r']*5
ax.set_xticks(np.arange(0.5,15,1),minor=True)
ax.set_xticklabels(xlabel,minor=True)
ax.set_title("a) Toa net crf",loc='left',pad=10)
ax.text(1.5, 27,"Global",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(4.5, 27,"Tropical",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(7.5, 27,"Subtropical",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(10.5, 27,"Midlatitude",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(13.5, 27,"Highlatitude",ha='center',va='center',fontsize=10,rotation=-15)

ax=fig.add_subplot(132)
ax = sns.heatmap(csr_rank_p2, annot=True,fmt='.0f',cmap='RdYlGn',linewidths=0.5,cbar=True)#,linewidths=0.5,line
ax.set_adjustable('box')
ax.set_xticks(np.arange(0,15,1))
ax.set_yticks(np.linspace(0,24,25))
ax.tick_params(axis="both", which="major", direction="in")
ax.tick_params(axis="both", which="minor", direction="in")
ax.xaxis.set_major_locator(FixedLocator(np.arange(0,15,3)))#设置y主坐标间隔 1
ax.xaxis.set_minor_locator(FixedLocator(np.arange(0,15,1)))
ax.yaxis.set_major_locator(FixedLocator(np.linspace(0,24,25)))#设置y主坐标间隔 1
ax.xaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
# ax.xaxis.grid(True,which='minor',color='black',linestyle='--')#major,color='black'
ax.yaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
ax.tick_params(bottom=False,top=False,left=False,right=False)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['top'].set_visible(True)
ax.spines['left'].set_linewidth(1.5)
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['right'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_color('black')
ax.set_yticks(np.arange(0.5,25,1),minor=True)
ax.set_yticklabels(models_p2,minor=True)
ax.tick_params(axis='y',labelrotation=0)
xlabel=['c','s','r']*5
ax.set_xticks(np.arange(0.5,15,1),minor=True)
ax.set_xticklabels(xlabel,minor=True)
ax.set_title("b) sfc net crf",loc='left',pad=10)
ax.text(1.5, 27,"Global",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(4.5, 27,"Tropical",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(7.5, 27,"Subtropical",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(10.5, 27,"Midlatitude",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(13.5, 27,"Highlatitude",ha='center',va='center',fontsize=10,rotation=-15)

ax=fig.add_subplot(133)
ax = sns.heatmap(csr_rank_p3, annot=True,fmt='.0f',cmap='RdYlGn',linewidths=0.5,cbar=True)#,linewidths=0.5,line
ax.set_adjustable('box')
ax.set_xticks(np.arange(0,15,1))
ax.set_yticks(np.linspace(0,24,25))
ax.tick_params(axis="both", which="major", direction="in")
ax.tick_params(axis="both", which="minor", direction="in")
ax.xaxis.set_major_locator(FixedLocator(np.arange(0,15,3)))#设置y主坐标间隔 1
ax.xaxis.set_minor_locator(FixedLocator(np.arange(0,15,1)))
ax.yaxis.set_major_locator(FixedLocator(np.linspace(0,24,25)))#设置y主坐标间隔 1
ax.xaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
# ax.xaxis.grid(True,which='minor',color='black',linestyle='--')#major,color='black'
ax.yaxis.grid(True,which='major',color='black',linewidth=1.5)#major,color='black'
ax.tick_params(bottom=False,top=False,left=False,right=False)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['top'].set_visible(True)
ax.spines['left'].set_linewidth(1.5)
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['right'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_color('black')
ax.set_yticks(np.arange(0.5,25,1),minor=True)
ax.set_yticklabels(models_p3,minor=True)
ax.tick_params(axis='y',labelrotation=0)
xlabel=['c','s','r']*5
ax.set_xticks(np.arange(0.5,15,1),minor=True)
ax.set_xticklabels(xlabel,minor=True)
ax.set_title("c) Tcf",loc='left',pad=10)
ax.text(1.5, 27,"Global",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(4.5, 27,"Tropical",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(7.5, 27,"Subtropical",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(10.5, 27,"Midlatitude",ha='center',va='center',fontsize=10,rotation=-15)
ax.text(13.5, 27,"Highlatitude",ha='center',va='center',fontsize=10,rotation=-15)

# position = fig.add_axes([0.92, 0.2, 0.010, 0.85])
# fig.colorbar(ax)
plt.savefig('fig4.png',bbox_inches='tight')
