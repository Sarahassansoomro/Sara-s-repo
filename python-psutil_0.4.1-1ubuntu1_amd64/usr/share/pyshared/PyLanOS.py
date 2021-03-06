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
import json 

import psutil
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


def main():
 
        
	hosts=[]
	win = 0
	lin = 0
	app = 0
	other = 0
	prit = 0
	unk = 0
	forti = 0
        HOST="192.168.0.102"
	try:
    		IP(HOST)
	except ValueError:
    		print "Invalid host address."
    		exit(1)

	if "/" in HOST:
		ips = HOST
		for ip in IP(HOST):
			hosts.append(str(ip))
		del hosts[0]

	else:
		hosts.append(HOST)

        hostIP={}
	for HOST in hosts:
                stringg = psutil.cpu_times()
 		print stringg   
 		
                print "Scanning %s with nmap ..." % HOST
        	scanv = subprocess.Popen(["nmap", "-PE", str(HOST)],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
           
                if "down" in scanv:
   		        print " %s is down :( " %HOST
       		else: 
			print " %s is up :)" %HOST
                        print  json.dumps({'IP':HOST,'State':'UP'})      
                        return json.dumps({'IP':HOST,'State':'UP'})
			
                     



if __name__=="__main__":
    main()

