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
# type: 'I'  # for individual

# HEADERS
# user-agent: anything will do, as long as it is not a browser
# accept: */* everything, for CORS
# origin: null again, CORS

# After getting the JSON response, it calls another script
# called query_visa_appointments_on_date.sh 
# that makes more requests for getting appointments on that particular
# day and prints them

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
    "https://reentryvisa.inis.gov.ie/website/INISOA/IOA.nsf/(getDTAvail)?openagent&type=I" | 
python -c '''
import json
import sys

data = json.load(sys.stdin)
if data.get("error", False):
    raise Exception("ERROR: %s" % data["error"])
if data.get("empty", False):
    raise Exception("No appointments available")
data = data.get("dates", None)
if data is None:
    raise Exception("Data is NULL")
if len(data) == 0:
    raise Exception("No appointments available")
for date in data:
    print(date)
''' |
xargs -L1 ./query_visa_appointments_on_date.sh 
