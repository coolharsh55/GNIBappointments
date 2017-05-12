from os import environ as env
from bottle import app
from bottle import route
from bottle import run
from bottle import static_file
from bottle import template
from datetime import datetime
import requests

appointments = None
last_checked = None


@route('/')
def home():
	if last_checked is None:
		get_appointments()
	else:
		now = datetime.now()
		diff = now - last_checked
		if diff.days > 0 or diff.seconds > 1800:
			get_appointments()
	return template(
    	'index', appointments=appointments, last_checked=last_checked)


def get_appointments():
	
	global appointments
	global last_checked

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
	    appointments = None
	    print('BAD response')
	    return

	# sanity checks
	data = response.json()
	last_checked = datetime.now()

	# error key is set
	if data.get('error', None) is not None:
	    appointments = None
	    print('data error')
	    return

	# If there are no appointments, then the empty key is set
	if data.get('empty', None) is not None:
	    appointments = None
	    print('data empty')
	    return

	# There are appointments, and are in the key 'slots'
	data = data.get('slots', None)
	if data is None:
	    appointments = None
	    print('data empty')
	    return

	# This should not happen, but a good idea to check it anyway
	if len(data) == 0:
	    appointments = None
	    print('data empty')
	    return

	# print appointments
	# Format is:
	# {
	#   'id': 'str',
	#   'time': 'str'
	# }
	appointments = [appointment['time'] for appointment in data]
	print(appointments)


if __name__ == '__main__':
    run(debug=True, server='gunicorn', host='0.0.0.0', port=int(env.get("PORT", 5000)))