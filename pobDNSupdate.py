#!/usr/bin/env python3
import time,os,configparser,sys
import urllib3
import shutil
 
 
currentIP=''
urlUpdate=''
user=''
password=''
hostname=''
etcHostsUrl='' 

def getPrefs():
	global urlUpdate 
	global user
	global password
	global hostname
	global etcHostsUrl
	 
	if  sys.platform == 'linux':
		try:
			iniFile=os.path.join('/etc/pobDNSupdate/prefs.conf')
			config = configparser.ConfigParser()
			config.read(iniFile)
			urlUpdate=config['DEFAULT']['urlUpdate']
			user=config['DEFAULT']['user']
			password=config['DEFAULT']['password']
			hostname=config['DEFAULT']['hostname']
			etcHostsUrl=config['DEFAULT']['etcHostsUrl'] 
			return True
		except Exception as e:
			print (e.message)
			return False
	
	if sys.platform=="win32":
		try:
			if getattr(sys, 'frozen', False):
				# frozen
				iniFile= os.path.join(os.path.dirname(sys.executable),"prefs.conf")
			else:
				# unfrozen
				iniFile=os.path.join(os.path.dirname(os.path.realpath(__file__)),"prefs.conf")
			
			config = configparser.ConfigParser()
			config.read(iniFile)
			urlUpdate=config['DEFAULT']['urlUpdate']
			user=config['DEFAULT']['user']
			password=config['DEFAULT']['password']
			hostname=config['DEFAULT']['hostname']
			etcHostsUrl=config['DEFAULT']['etcHostsUrl'] 
			return True
		except Exception as e:
			print (e.message)
			return False
			
			
		
	if sys.platform=="darwin":
		try:
			iniFile=os.path.join('/etc/pobDNSupdate/prefs.conf')
			config = configparser.ConfigParser()
			config.read(iniFile)
			urlUpdate=config['DEFAULT']['urlUpdate']
			user=config['DEFAULT']['user']
			password=config['DEFAULT']['password']
			hostname=config['DEFAULT']['hostname']
			etcHostsUrl=config['DEFAULT']['etcHostsUrl'] 
			return True
		except Exception as e:
			print (e.message)
			return False
 
 
def getPublicIpRaw():
    url = "http://www.freemedialab.org/myip/rawip.php"
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', url)
        return r.data
    except urllib3.exceptions.NewConnectionError:
        print("Public IP failed")
        return currentIP    
 
 
def update():
	global urlUpdate 
	global user
	global password
	global hostname
	
	if (getPrefs() == True):
		
            global currentIP
            fmlIP=getPublicIpRaw()
            if (currentIP!=fmlIP):
                http = urllib3.PoolManager(cert_reqs='CERT_NONE')
                headers = urllib3.util.make_headers(basic_auth="'"+user+":"+password+"'")
                try:
                    r = http.request('POST', 
                                    urlUpdate + hostname ,
                                    fields={'user': user, 'password': password},
                                    headers=headers)
                    currentIP=fmlIP
                    print(str(r.data))
                except urllib3.exceptions.NewConnectionError:
                    print("Connection to provider failed!")    
            else:
                print("Nothing to update.")
 
try :
    
    if (str(sys.argv[1])=="install"):
        if sys.platform=="win32":

            if getattr(sys, 'frozen', False):
                # frozen
                binfile= os.path.join(os.path.dirname(sys.executable),"pobDNSupdate.exe")
            else:
                # unfrozen
                binfile=os.path.join(os.path.dirname(os.path.realpath(__file__)),"pobDNSupdate.exe")

        cmd="schtasks /create /tn PobDynDNS /tr \"'%s'\" /sc minute /mo 5 /RU SYSTEM " % binfile
        print(cmd)
        os.system(cmd)
        os.system("schtasks /run /tn PobDynDNS")
        input("Press any key to continue...")
        sys.exit()	
	
    if (str(sys.argv[1])=="remove"):
        if sys.platform=="win32":
            cmd="schtasks /delete /tn PobDynDNS /f"
            print(cmd)
            os.system(cmd)
            input("Press any key to continue...")
            sys.exit()	


        
				
except  IndexError:
	print("No Parameter")	

def updateHostsFile():
    if  sys.platform == 'linux':
        hostsFile='/etc/hosts'
    elif sys.platform == 'win32':
        hostsFile='C:\Windows\System32\drivers\etc\hosts'
    elif sys.platform == 'darwin':
        hostsFile='/etc/hosts'
    
    if (getPrefs() == True):
        if(etcHostsUrl is None):
            return
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        with open(hostsFile, 'wb') as out:
            try:
                r = http.request('GET', etcHostsUrl, preload_content=False)
                shutil.copyfileobj(r, out)
                print("%s hosts updated." % hostsFile)
            except Exception as e:
                print ("Error on update %s : %s" % (hostsFile, e))
    
   
#while(True):
#    update()
#    updateHostsFile()
#    time.sleep(60*5)
    
update()
updateHostsFile() 
