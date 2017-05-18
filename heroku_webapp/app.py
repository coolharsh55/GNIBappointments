from os import environ as env
from bottle import route
from bottle import run
from bottle import template
from datetime import datetime
import arrow
import requests

# Add cipher for request
# Looked up using curl --verbose
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':DES-CBC3-SHA'
# disable SSL warning
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

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

gnib_appointments = None
visa_appointments = None
last_checked = None


@route('/')
def home():
    if last_checked is None:
        get_gnib_appointments()
        get_visa_appointments()
    else:
        now = datetime.now()
        diff = now - last_checked
        if diff.days > 0 or diff.seconds > 1800:
            get_gnib_appointments()
            get_visa_appointments()
    return template(
        'heroku_webapp/views/index',
        gnib_appointments=gnib_appointments,
        visa_appointments=visa_appointments,
        last_checked=last_checked)


def get_gnib_appointments():
    global gnib_appointments
    global last_checked

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

    # make the request
    # verify=False --> disable SSL verification
    response = requests.get(
        'https://burghquayregistrationoffice.inis.gov.ie/'
        + 'Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)',
        headers=headers, params=params, verify=False)

    # check if we have a good response
    if response.status_code != 200:
        gnib_appointments = None
        return

    # sanity checks
    data = response.json()
    last_checked = datetime.now()

    # error key is set
    if data.get('error', None) is not None:
        gnib_appointments = None
        return

    # If there are no gnib_appointments, then the empty key is set
    if data.get('empty', None) is not None:
        gnib_appointments = None
        return

    # There are gnib_appointments, and are in the key 'slots'
    data = data.get('slots', None)
    if data is None:
        gnib_appointments = None
        return

    # This should not happen, but a good idea to check it anyway
    if len(data) == 0:
        gnib_appointments = None
        return

    # print gnib_appointments
    # Format is:
    # {
    #   'id': 'str',
    #   'time': 'str'
    # }
    gnib_appointments = []
    now = datetime.now()
    for appointment in data:
        date = datetime.strptime(appointment['time'], '%d/%m/%Y %I:%M %p')
        if now < date:
            gnib_appointments.append(appointment['time'])


def get_visa_appointments():
    global last_checked
    global visa_appointments

    params = (
        ('openagent', ''),  # BLANK
        ('type', 'I')  # I signifies individual
    )

    # make the request
    # verify=False --> disable SSL verification
    response = requests.get(
        'https://reentryvisa.inis.gov.ie'
        + '/website/INISOA/IOA.nsf/(getDTAvail)',
        headers=headers, params=params, verify=False)

    # check if we have a good response
    if response.status_code != 200:
        visa_appointments = None
        return

    # sanity checks
    data = response.json()
    # error key is set
    if data.get('error', None) is not None:
        visa_appointments = None
        return

    # If there are no appointments, then the empty key is set
    if data.get('empty', None) is not None:
        visa_appointments = None
        return

    # There are appointments, and are in the key 'dates'
    data = data.get('dates', None)
    if data is None:
        visa_appointments = None
        return

    # This should not happen, but a good idea to check it anyway
    if len(data) == 0:
        visa_appointments = None
        return

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

        visa_appointments = []
        now = datetime.now()
        for appointment in data:
            date = datetime.strptime(appointment['time'], '%d/%m/%Y %I:%M %p')
            if now < date:
                visa_appointments.append(appointment['time'])


if __name__ == '__main__':
    run(
        debug=True,
        server='gunicorn', host='0.0.0.0', port=int(env.get("PORT", 5000)))
