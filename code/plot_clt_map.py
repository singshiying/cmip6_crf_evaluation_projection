import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable
font =FontProperties(family='Arial')
plt.rcParams['font.family']=font.get_name()
plt.rcParams['figure.figsize']=(5.5,4)

data_out=np.load('fig1.npy')#5x180x360x21(20models,obs)
model_mean=np.mean(data_out[:,:,:,0:20],3)
olat=np.arange(-89.5,90,1)
olon=np.arange(0.5,360,1)