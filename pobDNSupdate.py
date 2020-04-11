#!/usr/bin/env python3
import time,os,configparser,sys
import urllib3
 
 
currentIP=''
urlUpdate=''
user=''
password=''
hostname=''
 

def getPrefs():
	global urlUpdate 
	global user
	global password
	global hostname
	 
	if  sys.platform == 'linux':
		try:
			iniFile=os.path.join('/etc/pobDNSupdate/prefs.conf')
			config = configparser.ConfigParser()
			config.read(iniFile)
			urlUpdate=config['DEFAULT']['urlUpdate']
			user=config['DEFAULT']['user']
			password=config['DEFAULT']['password']
			hostname=config['DEFAULT']['hostname']
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
			return True
		except Exception as e:
			print (e.message)
			return False
 
 
def getPublicIpRaw():
	url = "https://api.ipify.org/?format=raw"
	http = urllib3.PoolManager()
	r = http.request('GET', url)
	return r.data
 
 
def update():
	global urlUpdate 
	global user
	global password
	global hostname
	
	if (getPrefs() == True):
		
		global currentIP
		fmlIP=getPublicIpRaw()
		if (currentIP!=fmlIP):
			http = urllib3.PoolManager()
			headers = urllib3.util.make_headers(basic_auth=user+':'+password)
			r = http.request('GET', urlUpdate + hostname ,headers=headers)
			currentIP=fmlIP
			print(str(r.data))
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
			
			cmd="schtasks /create /tn PobDynDNS /tr \"'%s'\" /sc onstart /RU SYSTEM " % binfile
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
 
while(True):
	update()
	time.sleep(60*5)
