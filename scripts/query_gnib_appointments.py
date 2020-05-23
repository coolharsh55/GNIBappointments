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

from bs4 import BeautifulSoup as bs4

from datetime import datetime
print(datetime.now())

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

# Add cipher for request
# Looked up using curl --verbose
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':DES-CBC3-SHA'
# disable SSL warning
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

r = requests.get("https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm", verify=False)
html_bytes = r.text
soup = bs4(html_bytes, 'lxml')
secret_k = soup.find('input', {'id': 'k'})['value']
secret_p = soup.find('input', {'id': 'p'})['value']

session = requests.Session()
session.headers.update({'referrer': 'https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm'})


def get_appointments(appointment_type, renewal):
    params = (
        # ('openpage', ''),  # BLANK
        # ('dt', ''),  # PARSED, but is always blank
        ('cat', appointment_type),  # Category
        ('sbcat', 'All'),  # Sub-Category
        ('typ', renewal),  # Type
        ('k', secret_k),
        ('p', secret_p),
        ('readform', '')
    )
    # make the request
    # verify=False --> disable SSL verification
    response = session.get(
        'https://burghquayregistrationoffice.inis.gov.ie/'
        + 'Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)',
        headers=headers, params=params, verify=False)

    # check if we have a good response
    print(response.json())
    if response.status_code != 200:
        print(response)
        print('error')
        return

    # sanity checks
    data = response.json()
    # error key is set
    if data.get('error', None) is not None:
        raise Exception('ERROR: %s' % data['error'])

    # If there are no appointments, then the empty key is set
    if data.get('empty', None) is not None:
        # print('No appointments available')
        return

    # There are appointments, and are in the key 'slots'
    data = data.get('slots', None)
    if data is None:
        print('Data is NULL')
        return

    # This should not happen, but a good idea to check it anyway
    if len(data) == 0:
        print('No appointments available')
        return

    # print appointments
    # Format is:
    # {
    #   'id': 'str',
    #   'time': 'str'
    # }
    print('{} appointments:'.format(appointment_type))
    for appointment in data:
        print(appointment['time'])


for appointment_type in ('All'):
    for renewal in ('New', 'Renewal'):
        # print(appointment_type, renewal)
        get_appointments(appointment_type, renewal)
