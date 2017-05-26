# GNIBappointments
Appointment finder for GNIB/VISA (Ireland)

Find the blog for this project at [harshp.com](https://harshp.com/dev/projects/gnib-appointments/).

## Using it

### Facebook Bot

There is a Facebook bot by the name **@GVisaBot** 
with a [Facebook Page](https://www.facebook.com/GVisaBot/). The bot replies with the available
appointments.

### Heroku webapp

There is a heroku webapp live at [https://gnibappt.herokuapp.com/](https://gnibappt.herokuapp.com/)
which essentially runs the `python` script in the background and displays
the results in a browser.

### Scripts

There are two scripts, `python` and `bash+python`. Since python
is installed pretty much by default everywhere (you suck Windows), that
one is more _nice_. The bash one pulls the request using `curl` and then
parses the json using python.

### Chrome Extension
The chrome extension can be loaded using developer tools -> unpacked extension. 
It should show a calendar icon on the bar. Clicking it will open a popup with a quick link to the appointment booking site.
Visiting the appointment page will trigger the extension, and it shows a bar on top with four options:

* **Check Appointments** - will show a popup with available appointments
* **Load Data** - will load stored form data from browser storage
* **Save Data** - will save current form data
* **Ask appointment** - once the form is filled, this will open the closest appointment to today

The ideal workflow is to save the form at some time (fill it completely) and then use the extension
to check whether there are any appointments available. If there are, click load data, and the form
should be filled completely. Then you can click on ask appointment and select one that suits.

At a basic level, it works using AJAX requests. 
There is another file - `query.html` that contains the jQuery code
to pull the appointments from within the browser. For it to work,
CORS needs to be _disabled_. If not, you can copy the jQuery bits
and execute them in the console of the GNIB appointments page. Beats
entering the form information.

## Why
The GNIB (Ireland) system uses an online application form to retrieve 
appointments, for which, one must first fill out a rather long form
to retrieve the available appointments. If there are no appointments
available, and this is the most likely scenario, well, tough luck.
The next time, fill out the entire form again and check if there are
any appointments.

Irritated by this procedure, and armed with a few crude skills around
websites and scripting, I created this script to pull the available
appointment dates. This script works as it is (for me) with the following
caveats:

 * The visa type is **Study**
 * The sub-type is **PhD** (this does not matter currently)

## How stuff works
The way this works is that the webpage sends some data based on the fields
in the form to a URI to get the available response. This can be retrieved
using the `form.onSubmit` field (basically what happens when you click
submit) and from there finding the javascript function that handles the
particular use case.

In this case, it is `allowLook4App` specified on `line 582` for button
`id=btLook4App`. This function is declared in the file 
[https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppForm.js](https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppForm.js).
It calls `get4DateAvailability()` which does the actual request to get
the appointment dates. 

Inside this function are the following lines:

```javascript
var sCat = "&cat=" + $('#Category').val();
var sSCat = "&sbcat=All" //+ $('#SubCategory').val();
var sTyp = "&typ=" + $('#ConfirmGNIB').val();
```
These get the category and the type of appointment.
In this case, they can be substituted with `Study` and `Renewal`.
The `subtype` is always `All`. 
The datastring is constructed as `var dataThis = sCat + sSCat + sTyp`
which is `category + subcategory + type`.
This is then sent as a GET request to the url `"/" + stPath + "/(getApps4DTAvailability)?openpage"`
where `stPath` is `'Website/AMSREG/AMSRegWeb.nsf'`.

The response from this is then checked for errors using `data.errors`.
If there are no appointments, there will be a non-null or defined key `data.empty`.
If there are appointments, they will be of the form:
```json
data = {
    slots: [
        {
            id: 'string',
            time: 'string'
        }
    ]
}
```

The server (or browser, I'm never sure) is _ficky_ about CORS, which is why
the requests need `Access-Control` and `Origin` headers. 

In the scripts, I've used the _get appointments nearest to today_ since that 
is more useful (to me) and is defined in `getEarliestApps()` with a differnt
URI as `"/" + stPath + "/(getAppsNear)?openpage"`.

The method for visa appointments is also quite similar. First, the dates are
requested, and then the appointments for each date are requested.