"""
Heroku app for GNIB and VISA appointments
Also handles Facebook Messenger bot GVisaBot (same page)

Author: Harshvardhan Pandit
See blog posts at https://harshp.com/dev/projects/gnib-appointments/

The framework used here is bottle.
It is small, it is light, it gets the job done.

There are two parts being handled here.
get_gnib_appointments(), get_visa_appointments() are used to populate the 
appointment lists.
home() is used to handle the heroku-based webpage
verification(), handle_messages(), and bot() are used to handle the FB bot.
FB bot verifies the URL, then sends JSON POST messages, whose response
is another request made containing the response.
"""

from os import environ as env
from bottle import route
from bottle import get, post, request
from bottle import run
from bottle import template
from datetime import datetime

import json
import pytz
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

# initially set them as empty
# load them at runtime
gnib_appointments = [] 
visa_appointments = []
# used to keep track of when the appointment was last checked
# refresh it roughly ever 30 mins
last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
# get Facebook Messenger tokens from environment
PAGE_ACCESS_TOKEN = env.get('GNIB_FACEBOOK_PAGE_ACCESS_TOKEN', None)
VERIFICATION_TOKEN = env.get('GNIB_FACEBOOK_VERIFICATION_TOKEN', None)
if PAGE_ACCESS_TOKEN is None or VERIFICATION_TOKEN is None:
    raise Exception('env tokens not loaded')


@route('/privacy_policy')
def privacy_policy():
    return template('heroku_webapp/views/privacy_policy.tpl')


def update_appointments():
    now = datetime.now(pytz.timezone('Europe/Dublin'))
    diff = now - last_checked
    if diff.days > 0 or diff.seconds > 1800:
        get_gnib_appointments()
        get_visa_appointments()
    return diff


@route('/')
def home():
    """handles heroku webpage"""
    diff = update_appointments()
    return template(
        'heroku_webapp/views/index',
        gnib_appointments=gnib_appointments,
        visa_appointments=visa_appointments,
        last_checked=diff.seconds // 60)


def get_gnib_appointments():
    """retrieves GNIB appointments"""
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
        gnib_appointments = []
        return

    # sanity checks
    data = response.json()

    # error key is set
    if data.get('error', None) is not None:
        gnib_appointments = []
        return

    # If there are no gnib_appointments, then the empty key is set
    if data.get('empty', None) is not None:
        gnib_appointments = []
        last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
        return

    # There are gnib_appointments, and are in the key 'slots'
    data = data.get('slots', None)
    if data is None:
        gnib_appointments = []
        last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
        return

    # This should not happen, but a good idea to check it anyway
    if len(data) == 0:
        gnib_appointments = []
        last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
        return

    # Format is:
    # {
    #   'id': 'str',
    #   'time': 'str'
    # }
    gnib_appointments = []
    now = datetime.now()
    last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
    for appointment in data:
        date = datetime.strptime(appointment['time'], '%d %B %Y - %H:%M')
        if now < date:
            gnib_appointments.append(appointment['time'])


def get_visa_appointments():
    """retrieves VISA appointments"""
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
        visa_appointments = []
        return

    # sanity checks
    data = response.json()
    # error key is set
    if data.get('error', None) is not None:
        visa_appointments = []
        return

    # If there are no appointments, then the empty key is set
    if data.get('empty', None) is not None:
        visa_appointments = []
        last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
        return

    # There are appointments, and are in the key 'dates'
    data = data.get('dates', None)
    if data is None:
        visa_appointments = []
        last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
        return

    # This should not happen, but a good idea to check it anyway
    if not data:
        visa_appointments = []
        last_checked = datetime.now(pytz.timezone('Europe/Dublin'))
        return

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
        if data.get('empty', False):
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
                date = date.strftime('%d %B %Y %H:%M')
                visa_appointments.append(date)
    last_checked = datetime.now(pytz.timezone('Europe/Dublin'))


@get('/bot')
def verification():
    """verification protocol for Facebook bot"""
    if request.query.get('hub.verify_token', None) is None:
        return
    if request.query.get('hub.challenge', None) is None:
        return
    token = request.query['hub.verify_token']
    if token == VERIFICATION_TOKEN:
        return request.query['hub.challenge']


@post('/bot')
def handle_messages():
    """handles messages for Facebook bot"""
    global last_checked
    global gnib_appointments
    global visa_appointments

    # this is how to get POST data in bottle
    data = str(request.body.read(), 'utf-8')
    data = json.loads(data)
    # json contains object with entry as list containing messaging as list
    events = data['entry'][0]['messaging']
    # iterate each item in list as 'event'
    for event in events:
        # sender is sender.id
        sender = event['sender']['id']
        # is message is not present, we don't handle it
        if event.get('message', None) is None:
            continue
        message = event['message']
        # if there is no text, we don't handle it
        if message.get('text', None) is None:
            continue
        # let's start handling the text responses
        text = message['text']
        update_appointments()
        # the user wants GNIB appointments
        if text in ('gnib', 'GNIB', 'g', 'G'):
            now = datetime.now(pytz.timezone('Europe/Dublin'))
            diff = now - last_checked
            response = '  \n'.join((
                'GNIB appointments',
                'checked ' + str(diff.seconds // 60) + 'mins ago',
                *gnib_appointments))
            if len(gnib_appointments) == 0:
                response += '. No GNIB appointments available.'
        # the user wants VISA appointments
        elif text in ('visa', 'VISA', 'v', 'V'):
            now = datetime.now(pytz.timezone('Europe/Dublin'))
            diff = now - last_checked
            response = '  \n'.join((
                'VISA appointments',
                'checked ' + str(diff.seconds // 60) + 'mins ago',
                *visa_appointments))
            if len(visa_appointments) == 0:
                response += '. No VISA appointments available.'
        elif text in ('help', 'h', 'HELP', '?'):
            response = '  \n'.join((
                'Use g/G/gnib/GNIB to get GNIB appointments',
                'Use v/H/visa/VISA to get VISA appointments'))
        # something else, ignore it
        else:
            response = '  \n'.join((
                'Try again.',
                'Use g/G/gnib/GNIB to get GNIB appointments',
                'Use v/H/visa/VISA to get VISA appointments'))
        # send the response back
        data = requests.post(
            "https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": PAGE_ACCESS_TOKEN},
            data=json.dumps({
                "recipient": {"id": sender},
                "message": {"text": response}
            }),
            headers={'Content-type': 'application/json'})
    return


@route('/bot')
def bot():
    """ handles this as a RESPONSE for Facebook bot"""
    return verification()


# get appointment when the app first loads
get_gnib_appointments()
get_visa_appointments()


if __name__ == '__main__':
    run(
        debug=True,
        server='gunicorn', host='0.0.0.0', port=int(env.get("PORT", 5000)))
