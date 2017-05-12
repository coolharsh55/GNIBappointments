#!/usr/bin/env python

# author: Harshvardhan Pandit
# email: me@harshp.com

# Script to parse appointment timings from GNIB website
# https://burghquayregistrationoffice.inis.gov.ie/
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
# https://burghquayregistrationoffice.inis.gov.ie
# /Website/AMSREG/AMSRegWeb.nsf/AppForm.js
params = (
    ('openpage', ''),  # BLANK
    ('dt', ''),  # PARSED, but is always blank
    ('cat', 'Study'),  # Category
    ('sbcat', 'All'),  # Sub-Category
    ('typ', 'Renewal'),  # Type
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
    'https://burghquayregistrationoffice.inis.gov.ie/'
    + 'Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)',
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

# There are appointments, and are in the key 'slots'
data = data.get('slots', None)
if data is None:
    raise Exception('Data is NULL')

# This should not happen, but a good idea to check it anyway
if len(data) == 0:
    print('No appointments available')
    sys.exit(0)

# print appointments
# Format is:
# {
#   'id': 'str',
#   'time': 'str'
# }
for appointment in data:
    print(appointment['time'])
