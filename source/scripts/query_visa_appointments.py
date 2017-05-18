#!/usr/bin/env python

# author: Harshvardhan Pandit
# email: me@harshp.com

# Script to parse appointment timings from GNIB VISA appointments website
# https://reentryvisa.inis.gov.ie/
# Reason: because filling out the ENTIRE form just to check for
# appointments is both silly and stupid. And on closer inspection,
# it is not like ALL the information is required for getting the
# appointments. Plus, it is never clear when the appointments will
# be available. Hence this script.

# It assumes the request module is installed
import requests
# sys is used to exit, I've read this is 'graceful'
import sys

# headers to send
# They don't really matter, except for the CORS bits
headers = {
    'User-agent': 'script/python',
    'Accept': '*/*',  # CORS
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'null',  # CORS
    'Connection': 'keep-alive',
}

# Parameters from the js script at
# https://reentryvisa.inis.gov.ie
# /website/INISOA/IOA.nsf/AppForm.js
params = (
    ('openagent', ''),  # BLANK
    ('type', 'I')  #  I signifies individual
)

# Add cipher for request
# Looked up using curl --verbose
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':DES-CBC3-SHA'
# disable SSL warning
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

# make the request
# verify=False --> disable SSL verification
response = requests.get(
    'https://reentryvisa.inis.gov.ie'
    + '/website/INISOA/IOA.nsf/(getDTAvail)',
    headers=headers, params=params, verify=False)

# check if we have a good response
if response.status_code != 200:
    print('error')
    sys.exit(1)

# sanity checks
data = response.json()
# error key is set
if data.get('error', None) is not None:
    raise Exception('ERROR: %s' % data['error'])

# If there are no appointments, then the empty key is set
if data.get('empty', None) is not None:
    print('No appointments available')
    sys.exit(0)

# There are appointments, and are in the key 'dates'
data = data.get('dates', None)
if data is None:
    raise Exception('Data is NULL')

# This should not happen, but a good idea to check it anyway
if len(data) == 0:
    print('No appointments available')
    sys.exit(0)

# print appointments
# Format is:
# {'dates': ['DD-MM-YYYY', ...]}
url = 'https://reentryvisa.inis.gov.ie/website/inisoa/ioa.nsf/(getapps4dt)'

for date in data:
    params = (
        ('openagent', ''),  # BLANK
        ('dt', '%s' % date),
        ('type', 'I'),
        ('num', 1)
    )
    response = requests.get(
            url, headers=headers, verify=False,
            # parameters need to be specified this way to prevent
            # escaping them
            # This really shows the bad design on part of website devs
            params='openagent=&dt=' + date + '&type=I&num=1')
    data = response.json()
    if (data.get('empty', False)):
        # if there are no appointments on that day, do nothing
        continue
    if data.get('error', False):
        # if there is an error, do nothing, move on to next date
        continue
    if data.get('slots', None) is None:
        # this is an error, but lets move along
        continue
    data = data['slots']
    for appointment in data:
        print(appointment['time'])

