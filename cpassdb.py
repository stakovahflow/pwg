#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Modified: 2023-05-05
#  cpassdb.py
license = """
#  cpassdb -- the pseudo-random password generator & sqlite3 password manager by stak ovahflow
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
#dbname='.passwd.db'
dbname=("%s/.passwd.db" % Path.home())
verbose=False
#passFile=("%s/.cryptopass.csv" % Path.home())
clearTime=15
typo = 'A'
counter = 0
line = '-' * 60
copyPass=False
tmppass=''

def licensing():
	print(license)
	exit(0)

def passVerb(option):
	if verbose:
		print("Added %s characters to password" % option)

def passGen(passLength, typo):
	if typo == 'A':
		passVerb('Lowercase')
		passVerb('Numeric')
		passVerb('Special')
		passVerb('Uppercase')
	else:
		if 'L' in typo:
			passVerb('Lowercase')
		if 'N' in typo:
			passVerb('Numeric')
		if 'S' in typo:
			passVerb('Special')
		if 'U' in typo:
			passVerb('Uppercase')
	count=int(passLength)
	if verbose:
		print("Password Length Selected: %d" % count)
	charsset = ''
	U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	L = 'abcdefghijklmnopqrstuvwxyz'
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
		try:
			clipper(tmppass)
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

def accountPass(password):
	if verbose:
		print("Setting Password")

def accountAdd(site,username,NewPass,description):
	currentDateTime = datetime.datetime.now()
	if verbose:
		print("Setting currentDateTime value to: %s" % currentDateTime)
	if verbose:
		print("Adding account")
	if verbose:
		print("Attempting to open database")
	try:
		con = sqlite3.connect(dbname)
		if verbose:
			print("Attempting to set cursor")
		cur = con.cursor()
		if verbose:
			print("Attempting to insert the following values into database:")
			#print("%s %s %s %s %s" % site,username,password,description,currentDateTime)
		insertcommand=("INSERT INTO current VALUES(NULL,'%s','%s','%s','%s','%s',NULL)" % (site,username,NewPass,description,currentDateTime))
		if verbose:
			print("Insert Command: %s" % insertcommand)
		cur.execute(insertcommand)
		con.commit()
		cur.close()
		con.close()
		if verbose:
			print("Completed inserting that stuff...")
	except Exception as e:
		print(e)

def accountRemove():
	con = sqlite3.connect(dbname)
	cur = con.cursor()
	if verbose:
		print("Removing account")
	#cur.execute("INSERT into current (NULL, site TEXT NOT NULL, username, password, description, created, modified)")
	con.close()

def accountUpdate():
	con = sqlite3.connect(dbname)
	cur = con.cursor()
	if verbose:
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
		cur.close()
		con.close()
	except:
		print("Unable to open database.")
		exit(0)

"""
def copyPassword(site):
	if verbose:
		print("Searching for site: %s" % site)
	try:
		con = sqlite3.connect(dbname)
		cur = con.cursor()
		query=("select id,site,username,password,created,description from current where site like '%s%%';" % site)
		for temp in cur.execute(query):
			print(base64.b64decode(temp[3]).decode('utf-8'))
		cur.close()
		con.close()
	except:
		print("Unable to open database.")
		exit(0)	
"""

def accountSearch(site):
	if verbose:
		print("Searching for site: %s" % site)
	try:
		con = sqlite3.connect(dbname)
		cur = con.cursor()
		query=("select id,site,username,password,created,description from current where site like '%s%%';" % site)
		for temp in cur.execute(query):
			#print(base64.b64decode(temp[3]).decode('utf-8'))
			id,site,username,password,created,description=temp
			#print(temp)
			if verbose:
				print("ID: %s" % id)
				print("Site: %s" % site)
				print("User: %s" % username)
				print("Created: %s" % created)
				print("Description: %s" % description)
				clearPass=base64.b64decode(password).decode('utf-8')
				print(clearPass)
		cur.close()
		con.close()
	except:
		print("Unable to open database.")
		exit(0)

def copyPass(site):
	if verbose:
		print("Attempting to copy password for site: %s" % site)
	try:
		con = sqlite3.connect(dbname)
		cur = con.cursor()
		query=("select id,site,username,password,created,description from current where site like '%s%%';" % site)
		for temp in cur.execute(query):
			#print(base64.b64decode(temp[3]).decode('utf-8'))
			id,site,username,password,created,description=temp
			#print(temp)
			if verbose:
				print("ID: %s" % id)
				print("Site: %s" % site)
				print("User: %s" % username)
				print("Created: %s" % created)
				print("Description: %s" % description)
				clearPass=base64.b64decode(password).decode('utf-8')
			try:
				copyClipper(clearPass)
			except:
				print("Unable to copy password to clipboard")
		cur.close()
		con.close()
	except:
		print("Unable to open database.")
		exit(0)

###############################################################################
# Main Functions:
###############################################################################
# try:
# 	con = sqlite3.connect(dbname)
# 	cur = con.cursor()
# 	#query=("select * from current;")
# 	query=("PRAGMA table_info(current);")
# 	temp=cur.execute(query)
# 	for t in temp:
# 		print(t)
# 	cur.close()
# 	con.close()
# except:
# 	print("oopsie!")

try:
	# GET ARGUMENTS using ARGPARSE
	parser = argparse.ArgumentParser(description=line+'\nCommand line password management tool\n written for shits and grins\n\
	\t\tEnjoy!\n'+line,formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("--initialize", "-i", action="store_true", help="Initialize password database")
	parser.add_argument("--add", "-a", action="store_true", help="Add a new account")
	parser.add_argument("--modify", "-m", action="store_true", help="Modify an existing account")
	parser.add_argument("--remove", "-r", action="store_true", help="Remove a password from the vault")
	parser.add_argument("--search", type=str, dest="search", action="store", help="View passwords inside the vault")
	parser.add_argument("--copy", "-c", type=str, dest='copy', action="store", help="Site/URL")
	parser.add_argument("--site", "-s", type=str, dest='site', action="store", help="Site/URL")
	parser.add_argument("--username", "-u", type=str, dest='username', action="store", help="Username")
	parser.add_argument("--password", "-p", type=str, dest="password", action="store", help="Password")
	parser.add_argument("--description", "-d", type=str, dest="description", action="store", help="Add a password to the vault")
	parser.add_argument("--viewall", action="store_true", help="View all encoded passwords for all sites")
	parser.add_argument("--generate", "-g", "-G", action="store_true", help="Generate a new random password")
	parser.add_argument("--count", "-C", type=int, dest="count", action="store", help="password length")
	parser.add_argument("--all", "-A", help="include all characters (overrides other options)", action="store_true")
	parser.add_argument("--lower", "-L", help="include lowercase characters", action="store_true")
	parser.add_argument("--number", "-N", help="include 0-9", action="store_true")
	parser.add_argument("--special", "-S", help="include special characters", action="store_true")
	parser.add_argument("--upper", "-U", help="include uppercase characters", action="store_true")
	parser.add_argument("--license", "-P", help="print license and exit", action="store_true")
	parser.add_argument("--verbose", "-v", action="store_true", help="Verbose mode")
	#subparsers = parser.add_subparsers(help='sub-command help', dest='password_help')
	#generate = subparsers.add_parser('generate', help = "generate help")

	results = args = parser.parse_args()
	if args.verbose:
		verbose=True
		print("Verbose mode")
		print(args)
	if verbose:
		print("Using password database: %s" % dbname)
	if args.initialize:
		if verbose:
			print("Initializing")
		initializedb()
	if args.license:
		if verbose:
			print("Licnese")
		licensing()
	elif args.generate:
		try:
			count=int(args.count)
		except:
			count=19
			if verbose:
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
		tmppass=passGen(count,typo)
		if verbose:
			print("Cleartext Password: %s" % tmppass)
		else:
			print(tmppass)
		try:
			clipper(tmppass)
		except:
			print('Unable to copy generated password to clipboard')
	elif args.add:
		try:
			if args.site:
				site=args.site
			else:
				site=getSite()
			username=getUser()
			password=getPass().encode('utf-8')
			#my_bytes = my_string.encode('utf-8')
			NewPass=(base64.b64encode(password))
			NewPass=NewPass.decode('utf-8')
			if verbose:
				print("Encoded Password: %s" % base64.b64decode(NewPass))
			if verbose:
				print("NewPass: %s" % NewPass)
			description=getDescription()
			accountAdd(site,username,NewPass,description)
		except Exception as e:
			print(e)
			print("Unable to add a new account")
	elif args.viewall:
		if verbose:
			print("Viewing all accounts")
		accountView()
	elif args.search:
		if verbose:
			print("Searching accounts")
		accountSearch(args.search)
	elif args.copy:
		if verbose:
			print("Attempting to copy account password")
		copyPass(args.copy)
	else:
		print("No input provided")
		parser.print_help(sys.stderr)
		exit(0)
except KeyboardInterrupt:
	print("")
	exit(0)
except Exception as e:
	print(e)
	print("\n%s\nExamples:" % line)

