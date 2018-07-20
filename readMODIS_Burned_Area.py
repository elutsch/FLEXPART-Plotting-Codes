import os, sys, shapefile
import numpy as np
#import pandas as pd
#import geopandas as gpd 
import pandas as pd
import datetime as dt 

years = [str(x) for x in range(2000,2018)] 

##if __name__ == "__main__":
def read_modis(main_dir):
    
    #main_dir = sys.argv[1] 
    
    modFile = os.path.join(main_dir,'MODIS_Burned_Areas')
    if os.path.isfile(modFile):
        print 'Found MODIS_Burned_Areas'
        df = pd.read_msgpack(modFile)
    
    else:
        df = []
        shpFiles = [] 
        for yr in years: 
            print yr 
            if os.path.isdir(os.path.join(main_dir,yr)):
                shpDir = [x for x in os.listdir(yr) if x.endswith('.shapefiles')] 
                
                for d in shpDir: 
                    shpPath = os.path.join(main_dir,yr,d)
                    
                    for f in os.listdir(shpPath):
                        if f.endswith('.shp'):
                            shp = os.path.join(shpPath,f)
                            shpFiles.append(shp)
                            Flg = True
                            break
                        else: 
                            print 'No shapfile for '+shpPath  
                            Flg = False
                    
                    if Flg:
                        print '\t'+shp
                        sf = shapefile.Reader(shp)
                        fields = [x[0] for x in sf.fields][1:]
                        records = sf.records()
                        shps = [s.points for s in sf.shapes()]
                    
                        temp = pd.DataFrame(columns=fields, data=records)
                        temp.index = pd.to_datetime([dt.date(int(yr),1,1)+dt.timedelta(days=int(i)) for i in temp['BurnDate'].values])
                        df.append(temp.assign(coords=shps))
            
            else: 
                print 'No Date for '+yr
            
        df = pd.concat(df)     
        df.to_msgpack(modFile)
    
    return df
    
    
    