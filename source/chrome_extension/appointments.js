function check_appointments() {
  var request = new XMLHttpRequest();
  request.open('GET', "https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)?openpage=&dt=&cat=Study&sbcat=All&typ=Renewal", true);

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!
      var data = JSON.parse(request.responseText);
      console.log(data);
      if (!(data.error === undefined || data.error === null)) {
          swal({
            title: 'ERROR',
            text: data.error,
            type: 'error'
          });
      } else if (!(data.empty === undefined || data.empty === null)) {
        swal({
            title: 'No appointments available',
            text: "could not find any free appointments at this time",
            type: 'info'
          });
      } else {
          var appointments = "";
          for (let appointment of data.slots) {
              appointments += appointment.time + "<br/>";
          }
          swal({
            title: 'Appointments available',
            html: appointments,
            type: 'info',
          });
      }
    } else {
      // We reached our target server, but it returned an error
      console.log('request error');
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
    console.log('error');
  };

  request.send();
};