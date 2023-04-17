#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  cryptopass.py
#  
#  Copyright (c) 2023 StakOvahflow stakovahflow666@gmail.com
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
########################################################################
#  Objective:
#	Read a base64-encoded dictionary from local CSV file and:
#	  A. View or Copy to clipboard
#	  A.1. Password 
#	  A.2. Username
########################################################################

import pyperclip
import base64, os, argparse, csv, time
from sys import argv
from pathlib import Path
passFile=("%s/.cryptopass.csv" % Path.home())
try:
	searchSite=argv[1]
	copyPass=False
	lst = []
	tmppass=''

	def clear():
		try:
			pyperclip.copy('')
		except:
			print("error blanking clipboard")
	
	def clipper(searchSite,username,tmppass):
		# write to the clipboard
		try:
			pyperclip.copy(tmppass.decode('utf-8'))
			#print("Text copied to clipboard!")
			print("Password for '%s' copied to clipboard" %(searchSite))
		except:
			print("for *NIX systems, please ensure you have xsel installed:")
			print("	sudo apt install -y xsel")
			print("	sudo dnf install -y xsel")
	
	def check_if_exists(x):
		with open(passFile, 'r') as f:
			reader = csv.reader(f)
			for i, row in enumerate(reader):
				if x.lower() == row[0]:
				#for j, column in enumerate(row):
				#	if x in column:
					print("Found: %s\n\tusername: %s" % (row[0], row[1]))
					username=row[1]
					tmppass=base64.b64decode(row[2])
					clipper(searchSite,username,tmppass)
					copyPass=True
					time.sleep(10)
					clear()	
					break
				# else:
					# if copyPass == False:
						# print("Can't find %s in %s" % (searchSite,passFile))
	check_if_exists(searchSite)
except:
	print("""Usage: %s <site.tld>
Example: %s google.com""")
