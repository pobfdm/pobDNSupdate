#!/usr/bin/env python3
import time,os,configparser,sys
import urllib3
 

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


 
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
 
 



class AppServerSvc (win32serviceutil.ServiceFramework):
	_svc_name_ = "PobDnsUpdate"
	_svc_display_name_ = "PobDNS update Service"
	stop=False
	

	def __init__(self,args):
		win32serviceutil.ServiceFramework.__init__(self,args)
		self.hWaitStop = win32event.CreateEvent(None,0,0,None)
		socket.setdefaulttimeout(60)

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		win32event.SetEvent(self.hWaitStop)
		self.stop=True

	def SvcDoRun(self):
		servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
			servicemanager.PYS_SERVICE_STARTED,	(self._svc_name_,''))
		self.main()

	def main(self):
		while(self.stop==False):
			update()
			time.sleep(60*5)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
