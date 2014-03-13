#!/usr/bin/python
# -*- coding: utf-8 -*-

__license__="""

PyLanOS, a simple script to detect LAN OS detection, using nmap -A option.


Author:
        c0r3dump | coredump<@>autistici.org

PyLanOS project site: https://github.com/c0r3dump3d/pylanos 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

The authors disclaims all responsibility in the use of this tool.

"""

import time
import os,sys
import argparse
import subprocess
try:
    from IPy import IP
except ImportError:
    print "You need to install IPy module: apt-get install python-ipy"
    exit(1)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
            self.HEADER = ''
            self.OKBLUE = ''
            self.OKGREEN = ''
            self.WARNING = ''
            self.FAIL = ''
            self.ENDC = ''


def replace_all(text, dic):
    for i, j in dic.iteritems():
    	text = text.replace(i, j)
    return text

def nmapScan(host,hup,hdown,option,verbose):

	

    reps = {";":""," ":"","0":"","1":""}
    try:
	    if option == 'lan':
		    scanv = subprocess.Popen(["nmap", "-PR", "-O", str(host)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
	    else:
		    scanv = subprocess.Popen(["nmap", "-PE","-PP","-PS21,22,23,25,80,443,3306,3389,8080","-O", str(host)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    except OSError:
        print "Install nmap: sudo apt-get install nmap"  

    scanlist=scanv.split()
    print scanv
    if verbose == 'yes':
    	print scanlist
    
    if "down" in scanv:
	    print '|___ ' +'it\'s down.'
	    osres = 'down'
	    hdown = hdown + 1
	    return osres,hup,hdown
    
    print '|___' + ' it\'s up ...',
    hup = hup + 1
    scanlist=scanv.split()
	
    if 'printer' in scanlist:
	    osres = 'Printer'
	    print bcolors.OKBLUE + osres + ' system.' + bcolors.ENDC
    elif 'Fortinet' in scanlist:
	    osres = 'Fortinet'
	    print bcolors.OKBLUE + osres + ' system.' + bcolors.ENDC
    elif 'Linux' in scanlist:
	    osres = 'Linux'
	    print bcolors.OKGREEN + osres + ' system.' + bcolors.ENDC
    elif 'Windows' in scanlist:
	    osres = 'Windows'
	    print bcolors.OKGREEN + osres+ ' system.' + bcolors.ENDC
    elif 'Apple' in scanlist:
	    osres = 'Apple'
	    print bcolors.OKGREEN + osres+ ' system.' + bcolors.ENDC
    elif 'IOS' in scanlist:
	    osres = 'IOS'
	    print bcolors.OKBLUE + osres+ ' system.' + bcolors.ENDC
    else:
	    osres = 'Unknow' 
	    print bcolors.FAIL + osres  + ' system. Unable to determine the OS type.' + bcolors.ENDC
	    
    
    return osres,hup,hdown 

def hello():
	print bcolors.OKGREEN
	print """
	  ____        _                 ___  ____  
	 |  _ \ _   _| |    __ _ _ __  / _ \/ ___| 
	 | |_) | | | | |   / _` | '_ \| | | \___ \ 
	 |  __/| |_| | |__| (_| | | | | |_| |___) |
	 |_|    \__, |_____\__,_|_| |_|\___/|____/ 
	        |___/                              

	A little Python script for LAN OS detection using nmap -O.
	 """
	print bcolors.ENDC
def main():
 
    parse = argparse.ArgumentParser(description='A little Python script for LAN OS detection (nmap -O)')
    parse.add_argument('-H', action='store', dest='host', help='A single host or CIDR notation.')
    parse.add_argument('-f', action='store', dest='file', help='A host list in a file.')
    parse.add_argument('-o', action='store', dest='output', help='The output write to a file.')
    parse.add_argument('-l', action='store', dest='nolan', default='no', help='No LAN host discover. Default no.')
    parse.add_argument('-v', action='store', dest='verbose', default='no', help='Verbose option to see the result of nmap -O, for each host. Default no.')

    hello()
    argus=parse.parse_args()

    if not os.geteuid()==0:
	  sys.exit("Only root can run this script.\n")

    if argus.host == None and argus.file == None:
        parse.print_help()
        exit(1)
    if argus.nolan != 'yes' and argus.nolan != 'no':
        parse.print_help()
	exit(1)
    if argus.verbose != 'yes' and argus.verbose != 'no':
        parse.print_help()
	exit(1)
    	

    else:
	hosts=[]
	osm=[]
	nuhost = 0
    	hup=0
    	hdown=0
	win = 0
	lin = 0
	app = 0
	ios = 0
	other = 0
	prit = 0
	unk = 0
	forti = 0

	verbose = argus.verbose

	if argus.nolan == 'yes':
		option = 'nolan'
	else:
		option = 'lan'

	if argus.file != None:
		hostFile = open (argus.file, 'r')
		for line in hostFile.readlines():
			line = line.split('\n')
			hosts.append(line[0])
			nuhost = nuhost + 1
			
	else:

        	try:
            		IP(argus.host)
        	except ValueError:
            		print "Invalid host address."
            		exit(1)

		if "/" in argus.host:
			ips = argus.host
			for ip in IP(argus.host):
				hosts.append(str(ip))
				nuhost = nuhost + 1
			del hosts[0]

		else:
        		hosts.append(argus.host)
			nuhost = nuhost + 1

	timeStart = int(time.time())
	for host in hosts:
    		print "Scanning %s with nmap ..." % host
        	os1,hup,hdown = nmapScan(host,hup,hdown,option,verbose)
		osm.append(os1)
	timeDone = int(time.time())
	timeRes = timeDone-timeStart
	
	for oss in osm:
		if oss == "Windows":
			win = win + 1
		elif oss == "Linux":
			lin = lin + 1
		elif oss == "Apple":
			app = app + 1
		elif oss == "Unknow":
			unk = unk + 1
		elif oss == "IOS":
			ios = ios + 1
		elif oss == "Printer":
			prit = prit + 1
		elif oss == "Fortinet":
			forti = forti + 1
		elif oss != "down":
			other = other + 1


	print
	print bcolors.HEADER + '++++++++++++++++++++++++++++++++++++++++'
	print bcolors.HEADER + '++++++++++++++++++++++++++++++++++++++++'
	print bcolors.HEADER + '++           SOME STATISTICS          ++'
	print bcolors.HEADER + '++++++++++++++++++++++++++++++++++++++++'
	print bcolors.HEADER + '++++++++++++++++++++++++++++++++++++++++'
	print bcolors.OKBLUE
	print 'Scan time (s): ' + str(timeRes)
	print 'Number of host: ' + str(nuhost) 
	print 'Host Alive: ' + str(hup)
	print 'Host Down: ' + str(hdown)
	print
	if hup == 0:
		exit(0)

	if win != 0:
		print ('[+] Number of Windows systems detected: %d (%d %%)' %(win,win*100/hup))
	if lin != 0:	
		print ('[+] Number of GNU/Linux systems detected: %d (%d %%)' %(lin,lin*100/hup))
	if app != 0:
		print ('[+] Number of Apple systems detected: %d (%d %%)' %(app,app*100/hup)) 
	if prit != 0:
		print ('[+] Number of Printer systems detected: %d (%d %%)' %(prit,prit*100/hup)) 
	if ios != 0:
		print ('[+] Number of Cisco systems detected: %d (%d %%)' %(ios,ios*100/hup)) 
	if forti != 0:
		print ('[+] Number of Fortinet systems detected: %d (%d %%)' %(forti,forti*100/hup)) 
	if other != 0:	
		print ('[+] Number of others systems detected: %d (%d %%)' %(other,other*100/hup)) 
	if unk != 0:
		print ('[+] Number of Unknow systems detected: %d (%d %%)' %(unk,unk*100/hup)) 

	print bcolors.ENDC

	hostos={}

	for i,host in enumerate(hosts):
	    hostos[host]=osm[i]

	if argus.output != None:
		fileout = argus.output
		fout = open(fileout,'w')
		for key in hostos: 
			if hostos[key] == 'down':
				fout.write( key + ' ==> ' + hostos[key]+'\n')
			else:
				fout.write( key + ' ==> ' + hostos[key] + ' system\n')
			



if __name__=="__main__":
    main()

