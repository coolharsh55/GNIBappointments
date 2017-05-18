#!/usr/bin/env bash

# author: Harshvardhan Pandit
# email: me@harshp.com

# Script to parse appointment timings from GNIB website
# https://burghquayregistrationoffice.inis.gov.ie/
# Reason: because filling out the ENTIRE form just to check for 
# appointments is both silly and stupid. And on closer inspection, 
# it is not like ALL the information is required for getting the 
# appointments. Plus, it is never clear when the appointments will
# be available. Hence this script.

# GET Params
# openpage: ''  # BLANK
# dt: ''  # PARSED, but is always blank
# cat: 'Study'  # Category
# sbcat: 'All'  # Sub-Category
# typ: 'Renewal'  # Type

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
    "http://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)?openpage=&dt=&cat=Study&sbcat=All&typ=Renewal" | 
    \
python -c '''
import sys
import json

data = json.load(sys.stdin)

if data.get("error", None) is not None:
    raise Exception("ERROR: %s" % data["error"])

# If there are no appointments, then the empty key is set
if data.get("empty", None) is not None:
    print("No appointments available")
    sys.exit(0)

# There are appointments, and are in the key "slots"
data = data.get("slots", None)
if data is None:
    raise Exception("Data is NULL")

# This should not happen, but a good idea to check it anyway
if len(data) == 0:
    print("No appointments available")
    sys.exit(0)

# print appointments
# Format is:
# {
#   "id": "str",
#   "time": "str"
# }
for appointment in data:
    print(appointment["time"])
'''
