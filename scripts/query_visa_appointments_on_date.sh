#!/usr/bin/env bash

# author: Harshvardhan Pandit
# email: me@harshp.com

# Script to parse appointment timings from GNIB website
# https://reentryvisa.inis.gov.ie
# Reason: because filling out the ENTIRE form just to check for 
# appointments is both silly and stupid. And on closer inspection, 
# it is not like ALL the information is required for getting the 
# appointments. Plus, it is never clear when the appointments will
# be available. Hence this script.

# GET Params
# openagent: ''  # BLANK
# type: I  # for individual
# dt: DD/MM/YYYY
# num: 1  # number of individuals in that appointment

# HEADERS
# user-agent: anything will do, as long as it is not a browser
# accept: */* everything, for CORS
# origin: null again, CORS

# curl options
# -k    disable SSL protection
# -L    follow redirects
# -s    do not show progress bars

curl \
    -k \
    -L \
    -s \
    -H "User-agent: script/python" \
    -H "Accept: */*" \
    -H "Accept-Language: en-US,en;q=0.5" \
    -H "Accept-Encoding: gzip, deflate, br" \
    -H "Origin: null" \
    -H "Connection: keep-alive" \
    "https://reentryvisa.inis.gov.ie/website/INISOA/IOA.nsf/(getApps4DT)?openagent&type=I&dt=${1}&num=1" | 
python -c '''
import json
import sys
data = json.load(sys.stdin)

if data.get("error", False):
    print("ERROR: %s" % data["error"])
    exit(0)
if data.get("empty", False):
    print("No appointments available")
    exit(0)
data = data.get("slots", None)
if data is None:
    print("Data is NULL")
    exit(0)
if len(data) == 0:
    print("No appointments available")
    exit(0)
for appointment in data:
    print(appointment["time"])
'''
