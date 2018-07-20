import os, urllib2, tarfile, time, calendar
import ftplib 
from datetime import datetime, date
cal= calendar.Calendar()  

baseDir = '/Collection6/SHP/'
server = 'ba1.geog.umd.edu'
ftp = ftplib.FTP(server)
ftp.login('user', 'burnt_data')

localdir = './'

win_list = [1,2,3,15,16,17,18] 
#win_list = [1] 
win_list = ['Win'+str(i).zfill(2) for i in win_list] 

downloadFlg = False
unzipFlg = True

years = range(2001,2018)

for win in win_list: 
    for yr in years:
        
        download_dir = os.path.join(localdir,str(yr))
        
        if os.path.isdir(download_dir):
            pass
        else:
            os.system('mkdir '+download_dir) 
            
        WinDir = os.path.join(baseDir,win,str(yr))
        
        if downloadFlg:
            try:
                ftp.cwd(WinDir)
                flist = ftp.nlst()
                Flg = True 
            except: 
                print 'No Directory: '+WinDir 
                Flg = False
            
            if Flg:
                for f in flist:
                    localfile = open(os.path.join(download_dir,f),'wb')
                    
                    if downloadFlg:
                        try:
                            ftp.retrbinary('RETR /'+os.path.join(WinDir,f),localfile.write)
                        except:
                            print 'ERROR: '+f
    
        if unzipFlg:
            tarFiles = [os.path.join(download_dir,x) for x in os.listdir(download_dir) if x.endswith('.tar.gz') and (win in x)] 
            
            for f in tarFiles:
                tar = tarfile.open(f) 
                path = f[:-7]
                tar.extractall(path=path) 
                tar.close() 
            
        ##os.system('mkdir archive')  
        ##os.system('mv *.tar.gz archive') 
    print 'Finished Region '+win 
    
                
                