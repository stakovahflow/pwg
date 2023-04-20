#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
license = """
#  pwg -- the pseudo-random password generator by stak ovahflow
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
#  This software was tested on Slackware 14.2, Fedora 25 Raspbian, &
#  Mac OS X 10.11
#
"""

import string
import random
import sys
# first time using argparse library
import argparse
# wanted to change the formatting of the help menu a little bit, so used RawTextHelpFormatter directly
from argparse import RawTextHelpFormatter

typo = ''
c = 16
counter = 0
line = '-' * 40

# CREATE FUNCTION for PWG
def PWG(z, t):
    # EMPTY SET OF CHARACTERS
    charsset = ''
    # UPPERCASE -"O"
    U = 'ABCDEFGHIJKLMNPQRSTUVWXYZ'
    # lowercase -"l"
    L = 'abcdefghijkmnopqrstuvwxyz'
    N = '0123456789'
    S = '!@#$%^&*?<>'
   
    # make sure we're using an integer, not a char/string
    z = int(z)
    for type in t:
        if 'u' in t:
            charsset = charsset + U
        if 'l' in t:
            charsset = charsset + L
        if 'n' in t:
            charsset = charsset + N
        if 's' in t:
            charsset = charsset + S
        if 'a' == t:
            charsset = charsset + U + L + N + S
   
    return ''.join(random.choice(charsset) for _ in range(0, int(z)))

# GET ARGUMENTS using ARGPARSE
parser = argparse.ArgumentParser(description='\n Create a random password\n\
 Special characters, numbers, UPPERCASE -"Oscar",\n\
 and lowercase -"lima" to avoid confusion.\n\
 Default options (no arguments): -c 16 -a\n\
 \t\tEnjoy! --stakovahflow666@gmail.com', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-c", "--count", dest="count", action="store", help="password length")
parser.add_argument("-a", "--all", help="same as -l -n -s -u", action="store_true")
parser.add_argument("-l", "--lower", help="include lowercase characters", action="store_true")
parser.add_argument("-n", "--number", help="include 0-9", action="store_true")
parser.add_argument("-s", "--special", help="include special characters", action="store_true")
parser.add_argument("-u", "--upper", help="include uppercase characters", action="store_true")
parser.add_argument("-p", "--license", help="print license and exit", action="store_true")

# COLLECT ARGPARSE RESULTS
results = args = parser.parse_args()

# CHECK RESULTS
# Check that a length was given.
# If not, gripe and exit.
if args.count == '0':
    print ("Input error:\nCannot create a zero length password.\nExiting")
    exit (0)
# check character results and add to counter if
# selection is made.
if args.lower:
    typo = typo + 'l'
    counter = counter + 1
    #print "lower"
if args.number:
    typo = typo + 'n'
    counter = counter + 1
    #print "number"
if args.special:
    typo = typo + 's'
    counter = counter + 1
    #print "special"
if args.upper:
    typo = typo + 'u'
    counter = counter + 1
    #print "upper"
if args.all:
    typo = 'a'
    counter = counter + 1
    #print "all"
if args.license:
    print (license)
    exit (1)

# CHECK COUNTER
# Check our counter and see if we used any command line
# options. We don't want to error out.
# try it gracefully. If no arguments are given,
# use defaults and tell the user.
# args.count comes from argparse and by default requires
# an input to '-c'. We want to get around that for the
# sake of convenience.
# Without further adieu, here's our if statement:
if args.count:
    if counter == 0:
        typo = 'a'
        #print ("defaulting to '--all'")
    print (PWG(results.count,typo))
else:
    if counter == 0:
        typo = 'a'
        #print ("defaulting to '--count 16 --all'")
    print (PWG(c,typo))
