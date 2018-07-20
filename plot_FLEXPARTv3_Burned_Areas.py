import os, sys

modis_dir = '/data/02/elutsch/MODIS_Burned_Areas'
sys.path.append('./Pflexible/')
#sys.path.append('./MODIS/') 
sys.path.append(modis_dir) 

import pflexible as pf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt 
import matplotlib.ticker as ax
import scipy.interpolate as inter
import datetime
import calendar

#import shapefile
from matplotlib.colors import Normalize
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import tempfile, zipfile 
import urllib2, time
import mapping as mp 
import pandas as pd
import datetime as dt 

from readMODIS_Burned_Area import read_modis

#from datetime import date, time
#from matplotlib.dates import num2date, DateFormatter, MonthLocator, YearLocator, \
     #DayLocator
#from dateutil.relativedelta import relativedelta
from matplotlib import rc
#from scipy.stats import linregress

font = {'size' : 18}
rc('font', **font)  
props = dict(boxstyle='round', facecolor='white', alpha=0.9,edgecolor='none')  

loc = {} 
loc['Eureka'] = [80.05,-86.42]
loc['Thule'] = [76.53,-68.74]
loc['0pal'] = [79.99,-85.93]  

if __name__ == '__main__':
  
  main_dir = sys.argv[1]
  site = sys.argv[2] 
  proj = 'Canada' 
  dataMODIS = read_modis(modis_dir)

  for dir in os.listdir(main_dir):
    H = pf.Header(os.path.join(main_dir,dir))
    H.fill_backward() 
    #T = pf.read_trajectories(H)
      
    for s,k in H.C:
      data = H.C[(s,k)]
      temp = dataMODIS[dt.datetime.strftime(data.timestamp-dt.timedelta(days=3),'%Y-%m-%d %H:%M:%S'):dt.datetime.strftime(data.timestamp,'%Y-%m-%d %H:%M:%S')]
      
      for lev in range(1,2):
      	TC = None
#      	data = H.C[(s,k)]
      	TC = pf.plot_footprint(H, H.C[(s,k)], data_range = [0.001,0.1],level=lev,map_region=proj,FIGURE=TC)
      	#TC = pf.plot_trajectory(H,T,k,draw_labels=True,FIGURE=TC)
      	#TC = pf.plot_trajectory_ellipses(H,T,FIGURE=TC)
      
      	m = TC.m 
      	lon, lat = m(loc[site][1],loc[site][0])
      	m.scatter(lon, lat, s=200, color='r', marker='*', edgecolors='w', zorder=10)     
      

      	patches = []
      	for coords in temp['coords'].values:
        	x, y = np.transpose(coords) 
        	lon, lat = m(x,y)
        	shape = zip(lon,lat) 
        	poly = Polygon(shape,True,color='r',alpha=1,zorder=10)   
        	patches.append(poly)
        	plt.gca().add_patch(poly)
      
      	filename = main_dir+'%s_tc_%s_%d%d_Level%d' % (data.species, data.timestamp,s,k,lev)
      	TC.fig.savefig(filename+'.png')
      	TC.fig.savefig(filename+'.pdf')
      	#TC.fig.savefig('./FP'+str(I)+'.png') 
      	#plt.show()
      	plt.close()

