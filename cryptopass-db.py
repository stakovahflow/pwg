#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  cryptopass.py
license = """
#  cryptopass -- the pseudo-random password generator by stak ovahflow
#
#  This software is distributed under the MIT license.
#   
#  The MIT License (MIT)
#
#  Copyright (c) 2023 StakOvahflow stakovahflow666@gmail.com
#  Permission is hereby granted, free of charge, to any
#  person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the
#  Software without restriction, including without
#  limitation the rights to use, copy, modify, merge,
#  publish, distribute, sublicense, and/or sell copies
#  of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following
#  conditions:
#
#  The above copyright notice and this permission notice
#  shall be included in all copies or substantial portions
#  of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
#  ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
#  TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
#  SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
# 
#  NOTE:
#  This software was tested on Slackware 15, Ubuntu 22.04
# (LTS), Debian 11.1, Fedora 28, & Raspbian
#
"""

import base64, sys, os, argparse, csv, time, random, sqlite3, getpass, datetime
from pyperclip import copy as clipper
from sys import argv
from pathlib import Path
dbname='.passwd.db'
verbose=False
passFile=("%s/.cryptopass.csv" % Path.home())
clearTime=15
typo = 'A'
counter = 0
line = '-' * 60
searchSite=''
copyPass=False
tmppass=''

def licensing():
	print(license)
	exit(0)

def verbosity(option):
	if verbose:
		print("Added %s characters to password" % option)

def PWG(passLength, typo):
	if typo == 'A':
		verbosity('Lowercase')
		verbosity('Numeric')
		verbosity('Special')
		verbosity('Uppercase')
	else:
		if 'L' in typo:
			verbosity('Lowercase')
		if 'N' in typo:
			verbosity('Numeric')
		if 'S' in typo:
			verbosity('Special')
		if 'U' in typo:
			verbosity('Uppercase')
	count=int(passLength)
	if verbose:
		print("Password Length Selected: %d" % count)
	charsset = ''
	U = 'ABCDEFGHIJKLMNPQRSTUVWXYZ'
	L = 'abcdefghijkmnopqrstuvwxyz'
	N = '0123456789'
	S = '!@#$%^&*?<>'
	for type in typo:
		if 'A' == typo:
			charsset = U + L + N + S
		else:
			if 'N' in typo:
				charsset = charsset + N
			if 'L' in typo:
				charsset = charsset + L
			if 'S' in typo:
				charsset = charsset + S
			if 'U' in typo:
				charsset = charsset + U
	return ''.join(random.choice(charsset) for _ in range(0, count))

#exit(0)
def blankClipper():
	try:
		clipper('')
	except:
		print("Error blanking clipboard")

def copyClipper(tmppass):
	# write to the clipboard
	decoded=base64.b64decode(tmppass)
	#print(decoded.decode('utf-8'))
	try:
		clipper(decoded.decode('utf-8'))
		print("Password copied to clipboard!")
	except:
		print("for *NIX systems, please ensure you have xsel installed:")
		print("	sudo apt install -y xsel")
		print("	sudo dnf install -y xsel")

def getPass():
	passwordsMatch=False
	while (passwordsMatch == False):
		try:
			NewPass = getpass.getpass(prompt="New Password: ")
		except Exception as error:
			print('ERROR', error)
		try:
			ConfPass = getpass.getpass(prompt="Confirm Password: ")
		except Exception as error:
			print('ERROR', error)
		if ConfPass != NewPass:
			print("Oops! Passwords don't match")
		else:
			print('Passwords match')
			return(NewPass)
def getUser():
	userName=''
	try:
		while (userName==''):
			userName=input("Username: ")
			return userName
	except:
		exit(0)
def getSite():
	siteName=''
	try:
		while (siteName==''):
			siteName=input("Site Name (or URL): ")
			return(siteName)
	except:
		if verbose:
			print("Error setting site name.")
		exit(0)

def getDescription():
	entryDescription=''
	try:
		entryDescription=input("Description: ")
		return(entryDescription)
	except:
		if verbose:
			print("No description provided.")
"""
try:
	getSite()
	getUser()
	getPass()
	getDescription()
	#copyClipper('MzIxRGlzY28jQnVubnlcIQ==')
	#time.sleep(5)
	#blankClipper()
	#exit(0)
except KeyboardInterrupt:
	print("\nOperation aborted by user\n")
except:
	print("\nNot sure if I fucked up or you fucked up, but something fucked up")
	exit(1)
"""
	
def initializedb():
	try:
		initializeDBChoice=input("Would you like to initialize the password database? (yes/no): ")
		if initializeDBChoice == "yes":
			if os.path.exists(dbname):
				try:
					os.remove(dbname)
				except:
					print("Unable to remove %s" % dbname)
			else:
				print("The file does not exist") 
			try:
				con = sqlite3.connect(dbname)
				cur = con.cursor()
				cur.execute("CREATE TABLE current(id INTEGER PRIMARY KEY autoincrement, site TEXT NOT NULL, username TEXT, password TEXT, description TEXT, created datetime DEFAULT CURRENT_TIMESTAMP, modified datetime DEFAULT CURRENT_TIMESTAMP)")
				con.close()
			except:
				print("Unable to open database.")
				exit(0)
		else:
			print("Password database initialization aborted.")
			exit
	except:
		print("Password database initialization operation aborted")
		exit
	sys.exit(0)

def accountAdd(site,username,password,description):
	if verbose==True:
		print("Adding account")
	currentDateTime = datetime.datetime.now()
	if verbose==True:
		print("Attempting to open database")
	con = sqlite3.connect(dbname)
	if verbose==True:
		print("Attempting to set cursor")
	cur = con.cursor()
	if verbose==True:
		print("Attempting to insert the following values into database:")
		#print("%s %s %s %s %s" % site,username,password,description,currentDateTime)
	insertcommand=("INSERT INTO current VALUES(NULL,'%s','%s','%s','%s','%s',NULL)" % (site,username,password,description,currentDateTime))
	if verbose == True:
		print("Insert Command: %s" % insertcommand)
	cur.execute(insertcommand)
	con.commit()
	cur.close()
	con.close()
	if verbose == True:
		print("Completed inserting that stuff...")

def accountAddOG():
	site=getSite()
	print ("Received: %s" % site)
	username=getUser()
	print("Received: %s" % username)
	password=getPass()
	print("Received: %s" % password)
	description=getDescription()
	print("Received: %s" % description)
	if verbose==True:
		print("Adding account")
	currentDateTime = datetime.datetime.now()
	if verbose==True:
		print("Attempting to open database")
	con = sqlite3.connect(dbname)
	if verbose==True:
		print("Attempting to set cursor")
	cur = con.cursor()
	if verbose==True:
		print("attempting to insert the following values into database:")
		print("%s %s %s %s %s" % site,username,password,description,currentDateTime)
	insertcommand=("INSERT INTO current VALUES(NULL,'%s','%s','%s','%s','%s',NULL)" % (site,username,password,description,currentDateTime))
	cur.execute(insertcommand)
	con.commit()
	cur.close()
	con.close()
	if verbose == True:
		print("Completed inserting that stuff...")
	if verbose==True:
		print("Current Timestamp: %s" % currentDateTime)
	#cur.execute(insertquery, (site, username, password, description, currentDateTime, "NULL"))
	#cur.execute("INSERT INTO current VALUES (NULL, 'test2.com', 'user2', 'pass2', 'desc 2', '2023-04-23 00:39:47.254554', '2023-04-23 00:39:47.254554');")
	if verbose==True:
		print("inserted values into database")
	#cur.execute("INSERT INTO current VALUES (NULL, site, username, password, description, currentDateTime, currentDateTime)")
	#cur.execute(insertquery)

def accountRemove():
	con = sqlite3.connect(dbname)
	cur = con.cursor()
	if verbose==True:
		print("Removing account")
	#cur.execute("INSERT into current (NULL, site TEXT NOT NULL, username, password, description, created, modified)")
	con.close()

def accountUpdate():
	con = sqlite3.connect(dbname)
	cur = con.cursor()
	if verbose==True:
		print("Updating account")
	#cur.execute("INSERT into current (NULL, site TEXT NOT NULL, username, password, description, created, modified)")
	con.close()

def accountView():
	try:
		con = sqlite3.connect(dbname)
		cur = con.cursor()
		temp=cur.execute("select * from current")
		for t in temp:
			print(t)
		#print(temp)
		cur.close()
		con.close()
	except:
		print("Unable to open database.")
		exit(0)
"""
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
				#clipper(searchSite,username,tmppass)
				copyPass=True
				time.sleep(clearTime)
				blankClipper()	
				break
			# else:
				# if copyPass == False:
					# print("Can't find %s in %s" % (searchSite,passFile))
"""
try:
	# GET ARGUMENTS using ARGPARSE
	parser = argparse.ArgumentParser(description=line+'\nCommand line password management tool\n written for shits and grins\n\
	\t\tEnjoy!\n'+line,formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("--initialize", "-i", action="store_true", help="Initialize password database")
	#parser.add_argument("--vault", "-s", dest="vault", action="store", help="Perform Add/Modify/Remove to vault")
	parser.add_argument("--add", "-a", action="store_true", help="Add a new account")
	parser.add_argument("--modify", "-m", action="store_true", help="Modify an existing account")
	parser.add_argument("--remove", "-r", action="store_true", help="Remove a password from the vault")
	parser.add_argument("--search", action="store_true", help="View passwords inside the vault")
	parser.add_argument("--site", "-s", type=str, dest='site', action="store", help="Site/URL")
	parser.add_argument("--username", "-u", type=str, dest='username', action="store", help="Username")
	parser.add_argument("--password", "-p", type=str, dest="password", action="store", help="Password")
	parser.add_argument("--description", "-d", type=str, dest="description", action="store", help="Add a password to the vault")
	parser.add_argument("--view", action="store_true", help="View a password for specified site")
	parser.add_argument("--generate", "-g", "-G", action="store_true", help="Generate a new random password")
	parser.add_argument("--count", "-c", "-C", type=int, dest="count", action="store", help="password length")
	parser.add_argument("--all", "-A", help="include all characters (overrides other options)", action="store_true")
	parser.add_argument("--lower", "-L", help="include lowercase characters", action="store_true")
	parser.add_argument("--number", "-N", help="include 0-9", action="store_true")
	parser.add_argument("--special", "-S", help="include special characters", action="store_true")
	parser.add_argument("--upper", "-U", help="include uppercase characters", action="store_true")
	parser.add_argument("--license", "-P", help="print license and exit", action="store_true")
	parser.add_argument("--verbose", "-v", action="store_true", help="Verbose mode")
	results = args = parser.parse_args()
	if args.verbose:
		verbose=True
		print("verbose mode")
		print("Received input: %s" % args)
	if args.initialize:
		if verbose==True:
			print("Initializing")
		initializedb()
	if args.license:
		if verbose==True:
			print("Licnese")
		licensing()
	elif args.generate:
		try:
			count=int(args.count)
		except:
			count=19
			if verbose == True:
				print("Setting default password length of %d" % int(count))
		if count < 0:
			print ("Input error:\nCannot create a negative length password.\nExiting")
			exit (0)
		if args.number:
			typo = typo + 'N'
		if args.lower:
			typo = typo + 'L'
		if args.special:
			typo = typo + 'S'
		if args.upper:
			typo = typo + 'U'
		if args.all:
			typo = 'A'
		tmppass=PWG(count,typo)
		print(tmppass)
		try:
			clipper(tmppass)
		except:
			print('Unable to copy generated password to clipboard')
	elif args.add:
		if verbose==True:
			print("Add")
	if args.site:
		site=args.site
		if verbose == True:
			print("Site: %s" % site)
	if args.username:
		username=args.username
		if verbose == True:
			print("Username: %s" % username)
	if args.password:
		password=args.password
		if verbose == True:
			print("Password: %s" % password)
	if args.description:
		description=args.description
		if verbose == True:
			print("Description: %s" % description)
		if verbose == True:
			print("accountAdd(site,username,password,description)")
		accountAdd(site,username,password,description)
	elif args.remove:
		if verbose==True:
			print("Remove")
		accountRemove()
	elif args.update:
		if verbose==True:
			print("Update")
		accountUpdate()
	elif args.view:
		if verbose==True:
			print("View")
		accountView()
	else:
		print("No input provided")
		parser.print_help(sys.stderr)
		exit(0)
except KeyboardInterrupt:
	print("")
	exit(0)
except:
	print("\n%s\nExamples:" % line)
"""	print("\n - Add new password: \n%s --add -s NewSite -u NewUser -d 'Description'" % argv[0])
	print("\n - Update password: \n%s --update <key>" % argv[0])
	print("\n - Remove password: \n%s -a NewSite NewUser NewNote" % argv[0])
	print("\n - Add new password: \n%s -a NewSite NewUser NewNote" % argv[0])
	print("\n - Retrieve current password: \n%s -s google.com" % argv[0])
	print("\n - Generate pseudorandom password: \n%s -gLUNS -c 33" % argv[0])
"""
"""
def insertdb(NewSite,NewUser,NewNote,NewPass):
	ClearPass=bytes(argv[4],'utf-8')
	NewPass=(base64.b64encode(ClearPass).decode('utf-8'))
	if verbose==True:
		print("NewSite: %s" % NewSite)
		print("NewUser: %s" % NewUser)
		print("NewNote: %s" % NewNote)
		print("ClearPass: %s" % ClearPass.decode('utf-8'))
		#print("CreateDate: %s" % CreateDate)
		print(NewPass)
	cur.execute("INSERT INTO current VALUES (NULL,'%s','%s','%s','%s',CURRENT_TIMESTAMP);" % (NewSite,NewUser,NewNote,NewPass))
	con.commit()
	for result in cur.execute("SELECT id,site,username,password,description,created from current order by created desc"):
		id,site,username,password,description,created=result
		print("%s: %s: %s: %s: %s: %s" % (id,site,username,password,description,created))
	exit(0)
		# CREATE FUNCTION for PWG

def dbsearch():
	try:
		for result in cur.execute("SELECT id,site,username,password,description,created from current order by created desc"):
			id,site,username,password,description,created=result
		print("%s: %s: %s: %s: %s: %s" % (id,site,username,password,description,created))
	except:
		print("unable to search database.")
	#NewPass=(base64.b64encode(ClearPass).decode('utf-8'))
	#for result in cur.execute("SELECT id,site,username,password,description,created from current order by created desc"):
	#	id,site,username,password,description,created=result
	#	print("%s: %s: %s: %s: %s: %s" % (id,site,username,password,description,created))
		exit(0)
"""

"""
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
				#clipper(searchSite,username,tmppass)
				copyPass=True
				time.sleep(clearTime)
				blankClipper()
				break
			# else:
				# if copyPass == False:
					# print("Can't find %s in %s" % (searchSite,passFile))
"""