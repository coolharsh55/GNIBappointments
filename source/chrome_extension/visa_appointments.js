var counter = 0;
var swal_appointments = "";

function check_appointments() {
    swal_appointments = "";
  var request = new XMLHttpRequest();
  request.open('GET', "https://reentryvisa.inis.gov.ie/website/INISOA/IOA.nsf/(getDTAvail)?openagent&type=I", true);

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
          for (let date of data.dates) {
              getAppointmentOnDate(date);
          }
          counter = data.dates.length;
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

function getAppointmentOnDate(date) {
  var request = new XMLHttpRequest();
  request.open('GET', "https://reentryvisa.inis.gov.ie/website/INISOA/IOA.nsf/(getApps4DT)?openagent&type=I&num=1&dt=" + date, true);

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!
      var data = JSON.parse(request.responseText);
      console.log(data);
      if (!(data.error === undefined || data.error === null)) {
          counter -= 1;
          return '';
      } else if (!(data.empty === undefined || data.empty === null)) {
          counter -= 1;
          return '';
      } else {
          var appointments = "";
          for (let appointment of data.slots) {
              appointments += appointment.time + '<br/>'; 
          }
          counter -= 1;
          swal_appointments += appointments;
          if (counter == 0) {
              swal({
                title: 'Appointments available',
                html: swal_appointments,
                type: 'info',
              });
          }
          return;
      }
    } else {
      // We reached our target server, but it returned an error
      console.log('request error');
        counter -= 1;
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
    console.log('error');
      counter -= 1;
  };

  request.send();
}
